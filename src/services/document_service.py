import os
import json
from sqlalchemy.orm import Session
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from src.models.document import Document
from src.utils.logging_utils import LoggingUtils
from src.utils.file_utils import FileUtils

logger = LoggingUtils.get_logger(__name__)

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.user_selected_documents = {}


    async def ingest_document(self, file):
        logger.info(f"Extracting content from file: {file.filename}")

        # Determine file extension
        _, file_extension = os.path.splitext(file.filename)
        if file_extension.lower() not in ['.txt', '.pdf']:
            raise ValueError("Unsupported file type. Only .txt and .pdf files are supported.")

        # Save the uploaded file to a temporary location
        temp_file_path = FileUtils.save_to_temp_file(file, suffix=file_extension)

        try:
            # Load file content
            content = self._load_content(temp_file_path)

            # Split the content into chunks
            chunks = self._split_content(content)

            # Generate embeddings
            embeddings = self._generate_embeddings(chunks)

            # Store document in the database
            document = self._store_document(file.filename, content, embeddings)

            logger.info(f"Document stored in database: {file.filename}")
            return document
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)

    def _load_content(self, file_path: str) -> str:
        logger.info(f"Loading content from document: {file_path}")
        return FileUtils.load_file_content(file_path)

    def _split_content(self, content: str) -> list:
        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=2000, chunk_overlap=200)
        logger.info(f"Splitting text")
        return text_splitter.split_text(content)

    def _generate_embeddings(self, chunks: list) -> bytes:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        embeddings = embedding_model.embed_documents(chunks)
        logger.info(f"Generated embeddings: {embeddings}")
        return json.dumps(embeddings).encode('utf-8')

    def _store_document(self, filename: str, content: str, embeddings: bytes) -> Document:
        document = Document(name=filename, embedding=embeddings)
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        logger.info(f"Stored document in database: {filename}")
        return document


    def store_selected_documents(self, user_id: str, document_names: list[str]):
        # Store the selected document names in a dictionary for simplicity
        self.user_selected_documents[user_id] = document_names
        logger.info(f"Stored selected documents for user {user_id}: {document_names}")

    def get_selected_document_embeddings(self, user_id: str):
        # Retrieve the selected document names for the user
        document_names = self.user_selected_documents.get(user_id, [])
        if not document_names:
            logger.warning(f"No documents selected for user {user_id}")
            return []

        # Query the database for the embeddings of the selected documents
        stmt = select(Document).where(Document.name.in_(document_names))
        documents = self.db.execute(stmt).scalars().all()

        embeddings = [doc.embedding for doc in documents]
        logger.info(f"Retrieved embeddings for user {user_id}: {embeddings}")
        return embeddings