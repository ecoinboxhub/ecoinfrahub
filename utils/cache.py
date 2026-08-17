import time
import hashlib
import json
from typing import Any


class ResponseCache:
    def __init__(self, ttl: int = 3600, max_size: int = 200):
        self._cache: dict[str, tuple[Any, float]] = {}
        self.ttl = ttl
        self.max_size = max_size

    def _make_key(self, query: str, **kwargs) -> str:
        raw = query + json.dumps(kwargs, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, query: str, **kwargs) -> Any | None:
        key = self._make_key(query, **kwargs)
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self._cache[key]
        return None

    def set(self, query: str, value: Any, **kwargs) -> None:
        key = self._make_key(query, **kwargs)
        if len(self._cache) >= self.max_size:
            oldest = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            del self._cache[oldest]
        self._cache[key] = (value, time.time())

    def clear(self) -> None:
        self._cache.clear()

    @property
    def size(self) -> int:
        return len(self._cache)
