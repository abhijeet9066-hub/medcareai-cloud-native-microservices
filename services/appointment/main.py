import json
import os
import uuid
from datetime import datetime, timezone
from fastapi import FastAPI
from pydantic import BaseModel, Field
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

try:
    import redis
except ImportError:
    redis = None

app = FastAPI(title="MedCareAI Appointment Service", version="1.0.0")
CREATED = Counter("appointment_created_total", "Appointments created")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
APPOINTMENTS = {}

class AppointmentIn(BaseModel):
    patient_id: str = Field(pattern=r"^PT-[0-9]{4,}$")
    appointment_type: str = Field(min_length=2, max_length=50)


def publish_event(event: dict) -> bool:
    if redis is None:
        return False
    try:
        client = redis.from_url(REDIS_URL, socket_connect_timeout=0.2, socket_timeout=0.2)
        client.xadd("medcareai.audit", {"payload": json.dumps(event)})
        return True
    except Exception:
        return False

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    return {"ready": True}

@app.post("/appointments", status_code=201)
def create_appointment(payload: AppointmentIn):
    appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
    item = {
        "appointment_id": appointment_id,
        "patient_id": payload.patient_id,
        "appointment_type": payload.appointment_type,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "scheduled",
    }
    APPOINTMENTS[appointment_id] = item
    CREATED.inc()
    event = {"event": "appointment.created", **item}
    item["event_published"] = publish_event(event)
    return item

@app.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: str):
    from fastapi import HTTPException
    if appointment_id not in APPOINTMENTS:
        raise HTTPException(status_code=404, detail="appointment not found")
    return APPOINTMENTS[appointment_id]

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
