# Phase summaries

One-line summary per phase and where the full checklist lives. The authoritative list of steps is [EXECUTION-GUIDE.md](../EXECUTION-GUIDE.md); use it as the single source of truth and tick items off as you complete them.

| Phase | Summary | Doc | Execution guide |
|-------|---------|-----|-----------------|
| **1** | App foundation: stripped backend, ML model + `/predict`, Vite + React UI. | [phase-01-foundation.md](phase-01-foundation.md) | Phase 1 — Steps 1–3 |
| **2** | Containerization: Dockerfiles for backend and frontend; push to ECR. | [phase-02-containerization.md](phase-02-containerization.md) | Phase 2 — Steps 4–5 |
| **3** | IaC: Terraform VPC (3 AZs), subnets, NAT, IGW, SGs, IAM; then EKS, node groups, IRSA. | [phase-03-terraform.md](phase-03-terraform.md) | Phase 3 — Steps 6–7 |
| **4** | K8s: deploy backend and frontend to EKS; separate Deployment, Service, HPA, ALB per service. | [phase-04-kubernetes.md](phase-04-kubernetes.md) | Phase 4 — Steps 8–9 |
| **5** | DevSecOps: GitHub Actions (lint, test, build, Trivy, ECR, Terraform, Helm); OPA Gatekeeper, Pod Security. | [phase-05-devsecops.md](phase-05-devsecops.md) | Phase 5 — Steps 10–11 |
| **6** | Observability: Prometheus, Grafana, Loki, Jaeger; Golden Signals; SLI/SLO and dashboards. | [phase-06-observability.md](phase-06-observability.md) | Phase 6 — Steps 12–15 |
| **7** | Staging: separate namespace and Terraform workspace; PR → staging, approval → production. | [phase-07-staging.md](phase-07-staging.md) | Phase 7 — Step 16 |
| **8** | Autoscaling: HPA and Cluster Autoscaler; k6 load tests. | [phase-08-autoscaling.md](phase-08-autoscaling.md) | Phase 8 — Steps 17–18 |

Run phases in order (1 → 8). Always work from the execution guide.
