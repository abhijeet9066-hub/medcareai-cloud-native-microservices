from fastapi.testclient import TestClient
from services.gateway.main import app

def test_gateway_health():
    with TestClient(app) as c:
        r=c.get('/healthz')
        assert r.status_code == 200
        assert r.json()['status']=='ok'
