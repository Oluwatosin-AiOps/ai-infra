# Phase 8 — Autoscaling and Resilience Testing

**Full checklist:** [EXECUTION-GUIDE.md — Phase 8](../EXECUTION-GUIDE.md#phase-8--autoscaling-and-resilience-testing) (Steps 17–18)

---

## Summary

Confirm autoscaling (HPA and Cluster Autoscaler) and validate behavior under load with k6.

- **Step 17:** HPA for backend (CPU and/or request rate) and frontend (traffic/CPU); Cluster Autoscaler for EKS node groups; set min/max replicas and node limits; document scaling behavior.
- **Step 18:** k6 load tests: traffic spikes; observe HPA, error rate, saturation, error budget burn; document findings and tuning; optionally add k6 to CI.

All steps and sub-items are in the execution guide; nothing is omitted.
