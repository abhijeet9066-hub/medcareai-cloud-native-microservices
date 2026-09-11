import httpx
BASE='http://localhost:8080'
with httpx.Client(timeout=5.0) as c:
    print(c.get(BASE+'/healthz').json())
    print(c.get(BASE+'/api/patients/PT-1001').json())
    print(c.post(BASE+'/api/appointments', json={'patient_id':'PT-1001','appointment_type':'follow-up'}).json())
