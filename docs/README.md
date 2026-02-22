# Phase summaries

Short summary of each phase and where to find the full checklist. **Every step is in [EXECUTION-GUIDE.md](../EXECUTION-GUIDE.md)** — nothing is omitted; use the guide as the single source of truth and update the checkboxes as you complete items.

---

| Phase | Summary | Doc | Execution guide section |
|-------|---------|-----|--------------------------|
| **1** | Application foundation: clone template, strip to backend core; add ML fraud model; build Next.js UI. | [phase-01-foundation.md](phase-01-foundation.md) | Phase 1 — Steps 1–3 |
| **2** | Containerization: Dockerfiles for backend and frontend; push images to ECR. | [phase-02-containerization.md](phase-02-containerization.md) | Phase 2 — Steps 4–5 |
| **3** | Infrastructure as Code: Terraform for VPC (3 AZs), subnets, NAT, IGW, SGs, IAM; then EKS cluster, node groups, IRSA. | [phase-03-terraform.md](phase-03-terraform.md) | Phase 3 — Steps 6–7 |
| **4** | Kubernetes deployment: deploy backend and frontend to EKS; separate Deployment, Service, HPA, and ALB per service. | [phase-04-kubernetes.md](phase-04-kubernetes.md) | Phase 4 — Steps 8–9 |
| **5** | DevSecOps: GitHub Actions (lint, test, build, Trivy, ECR, Terraform, Helm); OPA Gatekeeper and Pod Security. | [phase-05-devsecops.md](phase-05-devsecops.md) | Phase 5 — Steps 10–11 |
| **6** | Observability and SLOs: Prometheus, Grafana, Loki, Jaeger; Golden Signals; SLI/SLO definitions and SLO dashboards. | [phase-06-observability.md](phase-06-observability.md) | Phase 6 — Steps 12–15 |
| **7** | Staging: staging namespace, Terraform workspace, separate ALBs; PR → staging, approval → production. | [phase-07-staging.md](phase-07-staging.md) | Phase 7 — Step 16 |
| **8** | Autoscaling and resilience: HPA and Cluster Autoscaler; k6 load tests and validation. | [phase-08-autoscaling.md](phase-08-autoscaling.md) | Phase 8 — Steps 17–18 |

---

**Execution order:** Phase 1 → 2 → … → 8. Always follow [EXECUTION-GUIDE.md](../EXECUTION-GUIDE.md) and tick off each item.
