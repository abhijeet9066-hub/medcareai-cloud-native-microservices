# Five-Minute Project Story

I created this project to show that I understand Kubernetes beyond a single Deployment YAML. I separated a synthetic healthcare workflow into a gateway, patient service, appointment service and audit worker. The gateway handles north-south traffic while the domain services remain internal. Appointment creation can publish an event to Redis Streams so audit processing is decoupled from the request path.

Each HTTP workload has health and readiness probes, resource requests and limits, a non-root security context and a read-only root filesystem. The gateway has a PodDisruptionBudget and HorizontalPodAutoscaler. NetworkPolicies start from default-deny ingress and then permit only the intended gateway-to-service and service-to-Redis paths.

I also documented where this design is intentionally simplified. The lab uses in-memory domain state so it is easy to run and review. Production microservices would own persistent databases and need durable event delivery, authentication/authorization, secrets management, encryption, backups, observability and compliance controls.

The main lesson is that cloud-native architecture is not just splitting code into containers. It requires thinking about service boundaries, failure modes, scaling, networking, security and operational evidence.
