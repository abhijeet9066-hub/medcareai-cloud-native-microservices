# Architecture

The gateway is the only intended north-south entry point. Patient and appointment services are internal ClusterIP services. Redis provides asynchronous event transport between the appointment service and audit worker. The lab keeps business state in memory to make the repository portable; a production implementation would use service-owned persistent databases and an outbox/event delivery pattern.

## Why microservices?
The purpose is to demonstrate independently deployable bounded services, different scaling needs and fault isolation. In a small product this architecture may be unnecessary; a modular monolith could be operationally simpler. The repository documents that trade-off rather than claiming microservices are always better.

## Data safety
Only synthetic data is present. No PHI/PII, diagnostic logic or treatment advice belongs in this demo repository.
