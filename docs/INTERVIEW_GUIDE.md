# Interview Guide

## 60-second explanation
I built a healthcare-themed cloud-native demo using FastAPI microservices on Kubernetes. A gateway exposes a stable client API, internal patient and appointment services communicate over Kubernetes Services, and appointment creation publishes an asynchronous event to Redis Streams for an audit worker. I added readiness/liveness probes, resources, HPA, PDB, restrictive NetworkPolicies and non-root containers. The data is fully synthetic and the project intentionally avoids clinical decision claims.

## Questions

### Why an API gateway?
It centralizes the public contract and hides internal service topology. In production it is also a natural place for authentication, rate limiting and request correlation, though those controls should not all be hand-built in application code.

### Why asynchronous eventing?
Audit/event processing should not make the appointment request depend on a secondary consumer. Redis Streams demonstrates decoupling; Kafka or a managed event service may be preferable at larger scale.

### Why readiness and liveness separately?
Readiness controls whether traffic should reach a pod. Liveness decides whether Kubernetes should restart it.

### Why HPA requires resource requests?
CPU utilization targets are calculated against requested CPU. Without meaningful requests the scaling signal can be unusable.

### Why NetworkPolicy?
Kubernetes networking is permissive by default in many setups. NetworkPolicies document and enforce intended service communication when the CNI supports them.

### What would change for production healthcare?
OIDC/OAuth2, fine-grained authorization, mTLS/service mesh if justified, external secrets/KMS, encrypted persistent service-owned databases, immutable audit storage, backups/DR, consent/privacy controls, retention policies, vulnerability/SBOM scanning and jurisdiction-specific compliance review.
