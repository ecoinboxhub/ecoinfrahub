from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.backend.embeddings import EmbeddingEngine


def test_singleton():
    e1 = EmbeddingEngine()
    e2 = EmbeddingEngine()
    assert e1 is e2


def test_cache_key():
    engine = EmbeddingEngine()
    key1 = engine._cache_key("hello world")
    key2 = engine._cache_key("hello world")
    key3 = engine._cache_key("different text")
    assert key1 == key2
    assert key1 != key3


def test_embed_returns_vector():
    engine = EmbeddingEngine()
    if engine.load():
        embedding = engine.embed("test text")
        assert isinstance(embedding, list)
        assert len(embedding) > 0


def test_embed_batch():
    engine = EmbeddingEngine()
    if engine.load():
        embeddings = engine.embed_batch(["text1", "text2", "text3"])
        assert isinstance(embeddings, list)
        assert len(embeddings) == 3
        assert all(isinstance(e, list) for e in embeddings)


def test_run():
    test_singleton()
    test_cache_key()
    test_embed_returns_vector()
    test_embed_batch()
    print("All embedding tests passed!")


if __name__ == "__main__":
    test_run()
