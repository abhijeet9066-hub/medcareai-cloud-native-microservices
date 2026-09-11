from fastapi.testclient import TestClient
from services.patient.main import app

def test_health():
    with TestClient(app) as c:
        assert c.get('/healthz').status_code == 200

def test_known_patient():
    with TestClient(app) as c:
        r=c.get('/patients/PT-1001')
        assert r.status_code == 200
        assert r.json()['patient_id']=='PT-1001'

def test_unknown_patient():
    with TestClient(app) as c:
        assert c.get('/patients/PT-9999').status_code == 404
