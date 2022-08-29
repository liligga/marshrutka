from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

def test_drivers():
    resp = client.get('/drivers')
    assert resp.status_code == 200