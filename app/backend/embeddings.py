import hashlib
import pickle
from pathlib import Path
from typing import List
from sentence_transformers import SentenceTransformer
from config.settings import settings
from utils.logger import logger
from utils.monitor import get_ram_usage_gb


class EmbeddingEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._model: SentenceTransformer | None = None
        self._model_name: str = settings.embedding_model
        self._cache_dir: Path = settings.embeddings_dir
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._initialized = True

    def load(self) -> bool:
        if self._model is not None:
            return True
        try:
            logger.info(f"Loading embedding model: {self._model_name}")
            ram_before = get_ram_usage_gb()
            self._model = SentenceTransformer(
                self._model_name,
                cache_folder=str(self._cache_dir),
                device="cpu",
                model_kwargs={"trust_remote_code": True} if "nomic" in self._model_name else {},
            )
            ram_after = get_ram_usage_gb()
            logger.info(f"Embedding model loaded. RAM: {ram_before:.2f}GB -> {ram_after:.2f}GB")
            return True
        except Exception as e:
            logger.error(f"Failed to load embedding model '{self._model_name}': {e}")
            logger.info(f"Trying fallback model: {settings.embedding_model_fallback}")
            try:
                self._model_name = settings.embedding_model_fallback
                self._model = SentenceTransformer(
                    settings.embedding_model_fallback,
                    cache_folder=str(self._cache_dir),
                    device="cpu",
                )
                return True
            except Exception as e2:
                logger.error(f"Fallback model also failed: {e2}")
                return False

    def _cache_key(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def _get_cached(self, key: str) -> list[float] | None:
        cache_file = self._cache_dir / f"{key}.pkl"
        if cache_file.exists():
            with open(cache_file, "rb") as f:
                return pickle.load(f)
        return None

    def _set_cache(self, key: str, embedding: list[float]) -> None:
        cache_file = self._cache_dir / f"{key}.pkl"
        with open(cache_file, "wb") as f:
            pickle.dump(embedding, f)

    def embed(self, text: str) -> list[float]:
        if self._model is None:
            if not self.load():
                return [0.0] * 768
        key = self._cache_key(text)
        cached = self._get_cached(key)
        if cached is not None:
            return cached
        embedding = self._model.encode(text, normalize_embeddings=True).tolist()
        self._set_cache(key, embedding)
        return embedding

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if self._model is None:
            if not self.load():
                return [[0.0] * 768 for _ in texts]
        uncached: dict[int, str] = {}
        results: list[list[float] | None] = [None] * len(texts)
        for i, text in enumerate(texts):
            key = self._cache_key(text)
            cached = self._get_cached(key)
            if cached is not None:
                results[i] = cached
            else:
                uncached[i] = text
        if uncached:
            indices = list(uncached.keys())
            texts_to_embed = [uncached[i] for i in indices]
            embeddings = self._model.encode(texts_to_embed, normalize_embeddings=True, show_progress_bar=False)
            for idx, emb in zip(indices, embeddings):
                emb_list = emb.tolist()
                results[idx] = emb_list
                self._set_cache(self._cache_key(uncached[idx]), emb_list)
        return [r for r in results if r is not None]

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    def unload(self) -> None:
        if self._model is not None:
            del self._model
            self._model = None
            logger.info("Embedding model unloaded")


embedding_engine = EmbeddingEngine()
