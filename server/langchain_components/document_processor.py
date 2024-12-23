from langchain.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Optional
import os


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )

        self.supported_extensions = {
            ".txt": TextLoader,
            ".pdf": PyPDFLoader,
            ".csv": CSVLoader,
        }

    async def process_document(self, file_path: str) -> List[dict]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.supported_extensions:
            raise ValueError(f"Extensão não suportada: {ext}")

        loader_class = self.supported_extensions[ext]
        loader = loader_class(file_path)

        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)

        return [
            {"content": doc.page_content, "metadata": doc.metadata} for doc in chunks
        ]
