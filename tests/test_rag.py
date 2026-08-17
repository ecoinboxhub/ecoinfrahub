from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.backend.rag import RAGEngine, _normalize, _strip_think


def test_normalize():
    assert _normalize("  Hello   World  ") == "hello world"
    assert _normalize("Line1\nLine2") == "line1 line2"


def test_strip_think():
    text = "think_start some reasoning think_end Actual answer here"
    clean = text.replace("think_start", "<think>").replace("think_end", "</think>")
    result = _strip_think(clean)
    assert "<think>" not in result
    assert "Actual answer here" in result

    text2 = "No think tags here"
    result2 = _strip_think(text2)
    assert result2 == "No think tags here"

    text3 = "<think>reasoning1</think> middle <think>reasoning2</think> end"
    result3 = _strip_think(text3)
    assert "<think>" not in result3
    assert "</think>" not in result3


def test_rag_engine_init():
    rag = RAGEngine()
    assert rag.cache is not None
    assert rag._collection is None


def test_build_context_empty():
    rag = RAGEngine()
    context = rag.build_context([])
    assert context == ""


def test_build_context_with_docs():
    rag = RAGEngine()
    docs = [
        {"text": "Highway pavement design standards", "source": "manual.pdf", "chunk_index": 0, "similarity": 0.85},
        {"text": "Drainage flow calculations", "source": "guide.pdf", "chunk_index": 1, "similarity": 0.72},
    ]
    context = rag.build_context(docs)
    assert "[1]" in context
    assert "[2]" in context
    assert "Highway pavement" in context
    assert "Drainage flow" in context


def test_assess_retrieval_quality():
    rag = RAGEngine()
    assert rag._assess_retrieval_quality([]) == "none"
    docs_low = [{"similarity": 0.1}]
    assert rag._assess_retrieval_quality(docs_low) == "minimal"
    docs_mid = [{"similarity": 0.3}]
    assert rag._assess_retrieval_quality(docs_mid) == "weak"
    docs_high = [{"similarity": 0.8}]
    assert rag._assess_retrieval_quality(docs_high) == "strong"


def test_run():
    test_normalize()
    test_strip_think()
    test_rag_engine_init()
    test_build_context_empty()
    test_build_context_with_docs()
    test_assess_retrieval_quality()
    print("All RAG tests passed!")


if __name__ == "__main__":
    test_run()
