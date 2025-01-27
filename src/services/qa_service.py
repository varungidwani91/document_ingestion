from sqlalchemy.orm import Session
from src.services.document_service import DocumentService
from src.utils.logging_utils import LoggingUtils
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_rag import RAG

logger = LoggingUtils.get_logger(__name__)

class QAService:
    def __init__(self, db: Session):
        self.db = db
        self.document_service = DocumentService(db)
        self.rag_model = RAG(model_name="facebook/dpr-reader-single-nq-base")

    def answer_question(self, user_id: str, question: str) -> str:
        # Retrieve selected document embeddings for the user
        embeddings = self.document_service.get_selected_document_embeddings(user_id)
        if not embeddings:
            return "No documents selected or available for answering the question."

        # Use RAG to generate an answer based on the embeddings and the question
        answer = self.rag_model.generate_answer(question, embeddings)
        logger.info(f"Generated answer for user {user_id}: {answer}")
        return answer
