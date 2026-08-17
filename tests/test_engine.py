from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.backend.engine import LLMEngine


def test_singleton():
    e1 = LLMEngine()
    e2 = LLMEngine()
    assert e1 is e2


def test_not_loaded_initially():
    engine = LLMEngine()
    assert not engine.is_loaded


def test_model_path_exists():
    from config.settings import settings
    assert settings.model_path.name == "ecoinframind-ai-model.gguf"


def test_count_tokens():
    engine = LLMEngine()
    tokens = engine.count_tokens("Hello world, this is a test")
    assert tokens > 0
    assert isinstance(tokens, int)


def test_run():
    test_singleton()
    test_not_loaded_initially()
    test_model_path_exists()
    test_count_tokens()
    print("All engine tests passed!")


if __name__ == "__main__":
    test_run()
