from typing import Dict, Any
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def process_text(self, text: str) -> Dict[str, Any]:
        try:
            chunks = self.text_splitter.split_text(text)
            return {"success": True, "chunks": chunks}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def process_file(self, file_path: str) -> Dict[str, Any]:
        try:
            loader = TextLoader(file_path)
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            return {"success": True, "chunks": chunks}
        except Exception as e:
            return {"success": False, "error": str(e)}
