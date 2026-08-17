from __future__ import annotations
import re
from pathlib import Path
from typing import List, Generator
from config.settings import settings
from utils.logger import logger


SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".txt": "txt",
    ".md": "md",
}


class DocumentProcessor:
    def __init__(self):
        self.chunk_size: int = settings.chunk_size
        self.chunk_overlap: int = settings.chunk_overlap

    def extract_text(self, file_path: Path) -> str:
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            return self._extract_pdf(file_path)
        elif ext == ".docx":
            return self._extract_docx(file_path)
        elif ext == ".txt":
            return self._extract_txt(file_path)
        elif ext == ".md":
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _extract_pdf(self, path: Path) -> str:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return self._clean_text(text)
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return ""

    def _extract_docx(self, path: Path) -> str:
        try:
            from docx import Document
            doc = Document(str(path))
            text = "\n".join(p.text for p in doc.paragraphs)
            return self._clean_text(text)
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            return ""

    def _extract_txt(self, path: Path) -> str:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            return self._clean_text(text)
        except Exception as e:
            logger.error(f"TXT extraction error: {e}")
            return ""

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()
        return text

    def chunk_text(self, text: str) -> List[str]:
        if not text:
            return []
        chunks = []
        start = 0
        text_len = len(text)
        prev_start = -1
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            if end < text_len:
                last_period = text.rfind(". ", start, end)
                last_newline = text.rfind("\n", start, end)
                split_at = max(last_period, last_newline)
                if split_at > start:
                    end = split_at + 1
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end >= text_len:
                break
            new_start = end - self.chunk_overlap
            if new_start <= start and prev_start == new_start:
                new_start = end
            prev_start = start
            start = new_start
            if start >= text_len:
                break
        logger.info(f"Split text into {len(chunks)} chunks (size={self.chunk_size}, overlap={self.chunk_overlap})")
        return chunks

    def process_file(self, file_path: Path) -> List[dict]:
        text = self.extract_text(file_path)
        if not text:
            logger.warning(f"No text extracted from {file_path.name}")
            return []
        chunks = self.chunk_text(text)
        result = []
        for i, chunk in enumerate(chunks):
            result.append({
                "chunk_id": f"{file_path.stem}_{i}",
                "source": file_path.name,
                "text": chunk,
                "chunk_index": i,
            })
        logger.info(f"Processed {file_path.name}: {len(chunks)} chunks")
        return result

    def scan_knowledge_base(self) -> Generator[Path, None, None]:
        kb_path = settings.knowledge_dir
        if not kb_path.exists():
            logger.warning(f"Knowledge base directory not found: {kb_path}")
            return
        for ext in SUPPORTED_EXTENSIONS:
            yield from kb_path.rglob(f"*{ext}")


document_processor = DocumentProcessor()
