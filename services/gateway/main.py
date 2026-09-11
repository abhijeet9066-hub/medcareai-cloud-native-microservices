import os
import httpx
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="MedCareAI API Gateway", version="1.0.0")
PATIENT_SERVICE = os.getenv("PATIENT_SERVICE_URL", "http://patient-service:8000")
APPOINTMENT_SERVICE = os.getenv("APPOINTMENT_SERVICE_URL", "http://appointment-service:8000")
UPSTREAM_ERRORS = Counter("gateway_upstream_errors_total", "Gateway upstream failures", ["service"])

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"ready": True}

@app.get("/api/patients/{patient_id}")
def patient(patient_id: str):
    try:
        response = httpx.get(f"{PATIENT_SERVICE}/patients/{patient_id}", timeout=2.0)
    except httpx.HTTPError as exc:
        UPSTREAM_ERRORS.labels(service="patient").inc()
        raise HTTPException(status_code=503, detail="patient service unavailable") from exc
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="patient not found")
    response.raise_for_status()
    return response.json()

@app.post("/api/appointments", status_code=201)
def create_appointment(payload: dict):
    try:
        response = httpx.post(f"{APPOINTMENT_SERVICE}/appointments", json=payload, timeout=2.0)
    except httpx.HTTPError as exc:
        UPSTREAM_ERRORS.labels(service="appointment").inc()
        raise HTTPException(status_code=503, detail="appointment service unavailable") from exc
    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
