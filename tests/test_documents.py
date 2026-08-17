from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.backend.documents import document_processor


def test_clean_text():
    text = "Hello   World\n\n\nThis is   a test."
    cleaned = document_processor._clean_text(text)
    assert "  " not in cleaned


def test_chunk_text():
    text = "A. " * 200
    chunks = document_processor.chunk_text(text)
    assert len(chunks) > 0
    assert all(len(c) <= document_processor.chunk_size + document_processor.chunk_overlap for c in chunks)


def test_chunk_text_empty():
    chunks = document_processor.chunk_text("")
    assert chunks == []


def test_chunk_text_short():
    text = "Short text."
    chunks = document_processor.chunk_text(text)
    assert len(chunks) == 1


def test_run():
    test_clean_text()
    test_chunk_text()
    test_chunk_text_empty()
    test_chunk_text_short()
    print("All document tests passed!")


if __name__ == "__main__":
    test_run()
