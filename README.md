# MedCareAI Cloud-Native Microservices

A portfolio-grade **Kubernetes + Docker + FastAPI microservices** project that demonstrates cloud-native architecture using synthetic healthcare workflow data. It is a software-engineering demo, **not a clinical decision system**.

## Architecture

```text
Client
  │
  ▼
Ingress / API Gateway
  ├──> Patient Service ──> synthetic patient registry
  └──> Appointment Service ──> Redis Stream ──> Audit Worker

Platform controls
  ├── ConfigMaps / Secrets
  ├── readiness + liveness probes
  ├── resource requests / limits
  ├── HPA
  ├── PodDisruptionBudget
  ├── NetworkPolicies
  └── Prometheus-ready /metrics endpoints
```

## What this project proves

- Dockerized Python/FastAPI services
- service-to-service communication inside Kubernetes
- API gateway / aggregation pattern
- asynchronous Redis Streams eventing
- health and readiness probes
- Kubernetes Deployments, Services, Ingress, HPA and PDB
- security contexts and NetworkPolicies
- configuration through environment variables and Secrets
- CI tests and YAML validation
- production trade-offs, runbook and interview documentation

## Services

### Gateway
Public API facade. It calls internal services through Kubernetes DNS and keeps internal topology out of the client contract.

### Patient service
Read-only synthetic registry used to demonstrate service boundaries. No real patient data is included.

### Appointment service
Creates synthetic appointment workflow records and publishes `appointment.created` events to a Redis Stream when Redis is available.

### Audit worker
Consumes the Redis Stream and writes structured audit events to stdout, where a production logging stack could collect them.

## Quick start

Local Docker Compose:

```bash
docker compose up --build
```

Kubernetes:

```bash
make deploy
make verify
```

Generate sample requests:

```bash
python scripts/smoke_test.py
```

## Safety / portfolio scope

All names and identifiers in the demo are synthetic. There is no diagnosis, prescribing, treatment recommendation or medical-device claim. Production healthcare systems would additionally require strong identity/access controls, encryption, immutable audit trails, consent/privacy controls, data residency review and jurisdiction-specific compliance.

## License
MIT
