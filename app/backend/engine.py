from pathlib import Path
from typing import Generator, Optional
from llama_cpp import Llama
from config.settings import settings
from utils.logger import logger
from utils.monitor import get_ram_usage_gb


class LLMEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._model: Llama | None = None
        self._model_path: Path = settings.model_path
        self._initialized = True

    def load(self) -> bool:
        if self._model is not None:
            return True
        if not self._model_path.exists():
            logger.error(f"Model not found at {self._model_path}")
            return False
        try:
            logger.info(f"Loading model from {self._model_path}")
            ram_before = get_ram_usage_gb()
            self._model = Llama(
                model_path=str(self._model_path),
                n_ctx=settings.n_ctx,
                n_threads=settings.n_threads,
                n_batch=settings.n_batch,
                verbose=False,
                seed=42,
                use_mmap=False,
                use_mlock=False,
            )
            ram_after = get_ram_usage_gb()
            logger.info(f"Model loaded. RAM: {ram_before:.2f}GB -> {ram_after:.2f}GB")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def unload(self) -> None:
        if self._model is not None:
            del self._model
            self._model = None
            logger.info("Model unloaded")

    def generate(self, messages: list[dict], stream: bool = False) -> Generator[str, None, None] | str:
        if self._model is None:
            if not self.load():
                yield "Error: Model not loaded."
                return

        kwargs = dict(
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            top_p=settings.top_p,
            top_k=settings.top_k if not settings.do_sample else None,
            repeat_penalty=settings.repeat_penalty,
            stop=["<|im_end|>", "<|endoftext|>"],
        )

        if stream:
            for chunk in self._model.create_chat_completion(
                messages=messages,
                **{k: v for k, v in kwargs.items() if v is not None},
                stream=True,
            ):
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    delta = chunk["choices"][0].get("delta", {})
                    text = delta.get("content", "")
                    if text:
                        yield text
        else:
            result = self._model.create_chat_completion(
                messages=messages,
                **{k: v for k, v in kwargs.items() if v is not None},
                stream=False,
            )
            if "choices" in result and len(result["choices"]) > 0:
                text = result["choices"][0].get("message", {}).get("content", "")
                if text:
                    yield text

    def count_tokens(self, text: str) -> int:
        return len(text) // 4


llm_engine = LLMEngine()
