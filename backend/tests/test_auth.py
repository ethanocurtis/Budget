from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
