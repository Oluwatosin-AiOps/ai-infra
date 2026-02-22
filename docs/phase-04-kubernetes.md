# Phase 4 — Kubernetes Deployment

**Full checklist:** [EXECUTION-GUIDE.md — Phase 4](../EXECUTION-GUIDE.md#phase-4--kubernetes-deployment) (Steps 8–9)

---

## Summary

Deploy the **backend** (Python/FastAPI) and **frontend** (Next.js) to EKS as separate microservices, each with its own Deployment, Service, HPA, and external entry (ALB). No shared load balancer.

- **Step 8:** Backend: Deployment, ClusterIP Service, HPA, Ingress or LoadBalancer; dedicated ALB; verify `/predict` and health.
- **Step 9:** Frontend: separate Deployment, Service, LoadBalancer/Ingress; own ALB; frontend config points to backend API URL; confirm independent scaling and traffic.

Use the execution guide for the full checkbox list; complete every item.
