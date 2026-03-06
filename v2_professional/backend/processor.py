import os
from pypdf import PdfReader
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def extract_text(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return self._extract_pdf(file_path)
        elif ext == ".docx":
            return self._extract_docx(file_path)
        elif ext == ".txt":
            return self._extract_txt(file_path)
        return ""

    def _extract_pdf(self, path):
        text = ""
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def _extract_docx(self, path):
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])

    def _extract_txt(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def create_chunks(self, text, source_name):
        chunks = self.text_splitter.split_text(text)
        metadatas = [{"source": source_name} for _ in chunks]
        return chunks, metadatas
