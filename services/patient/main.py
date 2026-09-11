from fastapi import FastAPI, HTTPException, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="MedCareAI Patient Service", version="1.0.0")
REQUESTS = Counter("patient_service_requests_total", "Patient service requests", ["endpoint"])

PATIENTS = {
    "PT-1001": {"patient_id": "PT-1001", "display_name": "Synthetic Patient A", "age_band": "40-49", "city": "Demo City"},
    "PT-1002": {"patient_id": "PT-1002", "display_name": "Synthetic Patient B", "age_band": "60-69", "city": "Demo City"},
}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"ready": True}

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    REQUESTS.labels(endpoint="get_patient").inc()
    patient = PATIENTS.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="patient not found")
    return patient

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
