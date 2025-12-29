from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200

def test_ping_db():
    r = client.get("/ping/db")
    assert r.status_code == 200
    assert "status" in r.json()
