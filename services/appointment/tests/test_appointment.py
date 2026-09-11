from fastapi.testclient import TestClient
import services.appointment.main as module

module.publish_event=lambda event: False

def test_create_and_get_appointment():
    with TestClient(module.app) as c:
        r=c.post('/appointments', json={'patient_id':'PT-1001','appointment_type':'follow-up'})
        assert r.status_code == 201
        body=r.json()
        assert body['status']=='scheduled'
        fetched=c.get('/appointments/'+body['appointment_id'])
        assert fetched.status_code == 200
