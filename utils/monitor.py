import psutil
import time
from functools import wraps
from typing import Callable


def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=0.1)


def get_ram_usage_gb() -> float:
    return psutil.Process().memory_info().rss / (1024 ** 3)


def get_ram_percent() -> float:
    return psutil.virtual_memory().percent


def get_system_ram_gb() -> float:
    return psutil.virtual_memory().total / (1024 ** 3)


def get_available_ram_gb() -> float:
    return psutil.virtual_memory().available / (1024 ** 3)


class Timer:
    def __init__(self):
        self.start = 0.0
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start

    def __str__(self):
        return f"{self.elapsed:.3f}s"


def measure_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed
    return wrapper
