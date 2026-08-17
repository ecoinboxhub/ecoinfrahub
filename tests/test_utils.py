from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.cache import ResponseCache
from utils.monitor import Timer, get_cpu_usage, get_ram_usage_gb
import time


def test_cache():
    cache = ResponseCache(ttl=3600, max_size=10)
    assert cache.get("test") is None
    cache.set("test", "value")
    assert cache.get("test") == "value"
    assert cache.size == 1
    cache.clear()
    assert cache.size == 0


def test_cache_max_size():
    cache = ResponseCache(ttl=3600, max_size=2)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    assert cache.size <= 2


def test_cache_ttl():
    cache = ResponseCache(ttl=0.1, max_size=10)
    cache.set("test", "value")
    time.sleep(0.15)
    assert cache.get("test") is None


def test_timer():
    timer = Timer()
    with timer:
        time.sleep(0.05)
    assert timer.elapsed >= 0.05


def test_system_metrics():
    cpu = get_cpu_usage()
    ram = get_ram_usage_gb()
    assert isinstance(cpu, float)
    assert isinstance(ram, float)
    assert 0 <= cpu <= 100
    assert ram > 0


def test_run():
    test_cache()
    test_cache_max_size()
    test_cache_ttl()
    test_timer()
    test_system_metrics()
    print("All util tests passed!")


if __name__ == "__main__":
    test_run()
