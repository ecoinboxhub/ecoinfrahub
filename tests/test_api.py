from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_root():
    # With a built frontend (frontend/dist), "/" serves the SPA index.html.
    # Otherwise it falls back to the API-info JSON.
    r = client.get("/")
    assert r.status_code == 200
    if "text/html" in r.headers.get("content-type", ""):
        assert "<!doctype html" in r.text.lower()
    else:
        data = r.json()
        assert "app" in data
        assert "version" in data


def test_health():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data
    assert "cpu_percent" in data
    assert "ram_gb" in data


def test_metrics():
    r = client.get("/api/v1/metrics")
    assert r.status_code == 200
    data = r.json()
    assert "cpu_percent" in data
    assert "ram_gb" in data
    assert "model_loaded" in data
    assert "knowledge_stats" in data


def test_experts_list():
    r = client.get("/api/v1/experts")
    assert r.status_code == 200
    data = r.json()
    assert "experts" in data
    assert len(data["experts"]) >= 4


def test_knowledge_stats():
    r = client.get("/api/v1/knowledge/stats")
    assert r.status_code == 200
    data = r.json()
    assert "total_chunks" in data
    assert "status" in data


def test_calculator_concrete():
    r = client.post("/api/v1/calculator", json={
        "calculator": "concrete_mix",
        "params": {"cement": 350, "sand": 700, "aggregate": 1400, "water": 175}
    })
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert data["result"]["water_cement_ratio"] == 0.5
    assert "formula" in data["result"]
    assert data["result"]["working"]


def test_calculator_drainage():
    r = client.post("/api/v1/calculator", json={
        "calculator": "drainage",
        "params": {"area_ha": 50, "runoff_coefficient": 0.6, "rainfall_intensity_mm_hr": 50}
    })
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert data["result"]["peak_flow_m3_s"] > 0


def test_calculator_unknown():
    r = client.post("/api/v1/calculator", json={
        "calculator": "nonexistent_calc",
        "params": {}
    })
    assert r.status_code == 400


def test_chat_validation():
    r = client.post("/api/v1/chat", json={})
    assert r.status_code == 422


def test_upload_unsupported():
    import io
    r = client.post("/api/v1/upload", files={"file": ("test.exe", io.BytesIO(b"test"), "application/octet-stream")})
    assert r.status_code == 400


def test_run():
    test_root()
    test_health()
    test_metrics()
    test_experts_list()
    test_knowledge_stats()
    test_calculator_concrete()
    test_calculator_drainage()
    test_calculator_unknown()
    test_chat_validation()
    test_upload_unsupported()
    print("All API integration tests passed!")


if __name__ == "__main__":
    test_run()
