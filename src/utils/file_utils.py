import os
import tempfile
from langchain.document_loaders import PyPDFLoader

class FileUtils:
    @staticmethod
    def save_to_temp_file(file, suffix):
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(file.file.read())
            return temp_file.name

    @staticmethod
    def load_file_content(file_path: str) -> str:
        _, file_extension = os.path.splitext(file_path)
        
        if file_extension.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        elif file_extension.lower() == '.pdf':
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            return "\n".join(doc.page_content for doc in docs)
        else:
            raise ValueError("Unsupported file type. Only .txt and .pdf files are supported.")