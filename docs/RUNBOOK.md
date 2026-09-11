# Operations Runbook

## Gateway returns 503
1. Check gateway logs.
2. Confirm service DNS and endpoints.
3. Check patient/appointment pod readiness.
4. Inspect NetworkPolicies.
5. Compare service latency and error metrics.

## Appointments succeed but audit events are missing
1. Check Redis pod readiness.
2. Check appointment logs for `event_published` behavior.
3. Check audit-worker logs.
4. Inspect Redis stream/group state.

## HPA does not scale
- confirm Metrics Server is installed
- confirm CPU requests are defined
- inspect `kubectl describe hpa api-gateway -n medcareai`
