# MedCareAI Cloud-Native Microservices

A portfolio-grade **Kubernetes + Docker + FastAPI microservices** project demonstrating a cloud-native healthcare workflow reference architecture using synthetic data.

**This is a software-engineering reference implementation, not a functioning clinical decision system.**

## Portfolio positioning

> Built a four-service cloud-native healthcare workflow reference platform supporting the broader MedCareAI product architecture.

The project demonstrates **Kubernetes deployment configurations, Redis Streams event processing and GitHub Actions CI validation** without claiming a verified live production Kubernetes deployment.

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

## What this project demonstrates

- Dockerized Python/FastAPI services
- service-to-service communication design for Kubernetes
- API gateway / aggregation pattern
- Redis Streams event processing
- health and readiness probes
- Kubernetes deployment configurations: Deployments, Services, Ingress, HPA and PDB
- security contexts and NetworkPolicies
- configuration through environment variables and Secrets
- GitHub Actions CI validation and YAML checks
- production trade-offs, runbook and interview documentation

## Services

### Gateway
Public API facade. It calls internal services through Kubernetes DNS conventions and keeps internal topology out of the client contract.

### Patient service
Read-only synthetic registry used to demonstrate service boundaries. No real patient data is included.

### Appointment service
Creates synthetic appointment workflow records and can publish `appointment.created` events to a Redis Stream when Redis is available.

### Audit worker
Consumes the Redis Stream and writes structured audit events to stdout, where a production logging stack could collect them.

## Quick start

Local Docker Compose:

```bash
docker compose up --build
```

Kubernetes manifest/lab reference:

```bash
make deploy
make verify
```

These commands demonstrate the intended deployment workflow; the public repository does not claim a verified live production cluster deployment.

Generate sample requests:

```bash
python scripts/smoke_test.py
```

## Safety / portfolio scope

All names and identifiers in the demo are synthetic. There is no diagnosis, prescribing, treatment recommendation or medical-device claim. Production healthcare systems would additionally require strong identity/access controls, encryption, immutable audit trails, consent/privacy controls, data residency review and jurisdiction-specific compliance.

## CV-ready summary

Built a four-service cloud-native healthcare workflow reference platform supporting the broader MedCareAI product architecture, with Kubernetes deployment configurations, Redis Streams event processing and GitHub Actions CI validation.

## License

MIT
