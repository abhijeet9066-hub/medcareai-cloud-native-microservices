# Security Notes

- non-root containers
- `allowPrivilegeEscalation: false`
- read-only root filesystems
- dropped Linux capabilities
- default-deny ingress policy with explicit service communication
- no secrets committed to Git
- synthetic demo records only

For production, use signed images, pinned digests, image/SBOM scanning, workload identity, external secret management, TLS/mTLS where appropriate, admission policies and centralized audit retention.
