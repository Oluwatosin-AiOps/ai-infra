# Tech stack

Canonical choices for the Kubernetes-First AI Fraud Detection Platform. No steps in the execution guide are skipped; these are the technologies used to implement them.

---

## Application layer

| Component | Technology | Role |
|-----------|------------|------|
| **Frontend** | **Vite + React** (TypeScript) | Lightweight UI: transaction JSON form, calls ML API via `VITE_API_URL`, displays fraud probability and label. Deployed as its own container and has its own load balancer (microservice boundary). |
| **Backend (ML API)** | **Python 3.10+ / FastAPI** | Inference service: `POST /predict` plus `/api/v1/utils/health-check/`. Scikit-learn or XGBoost model, joblib-serialized. Deployed as its own container and its own load balancer. |

So: **two services** — **Vite + React frontend** and **Python/FastAPI ML backend** — each independently deployable and load-balanced.

---

## Infrastructure and orchestration

| Layer | Technology |
|-------|------------|
| **IaC** | Terraform (AWS: VPC, subnets, NAT, IGW, security groups, IAM, EKS, ECR). |
| **Containers** | Docker; images in Amazon ECR (`fraud-backend`, `fraud-frontend`). |
| **Orchestration** | Kubernetes (EKS); separate Deployments, Services, HPAs, and Ingress/LoadBalancer per service. |
| **Entry** | One AWS Application Load Balancer per service (no shared ALB). |

---

## CI/CD and security

| Area | Technology |
|------|------------|
| **CI/CD** | GitHub Actions: lint, unit tests, container build, Trivy scan, push to ECR, Terraform plan/apply, Helm upgrade. |
| **Policy** | OPA Gatekeeper, Kubernetes Pod Security Standards; optional image signing (e.g. cosign). |

---

## Observability

| Area | Technology |
|------|------------|
| **Metrics** | Prometheus; Golden Signals (latency, traffic, errors, saturation) + availability. |
| **Dashboards** | Grafana (availability, latency percentiles, error budget burn, saturation). |
| **Logs** | Loki. |
| **Traces** | Jaeger. |
| **SLOs** | Prometheus recording rules, Alertmanager, Grafana SLO dashboards. |

---

## Environments

- **Staging**: Separate namespace and Terraform workspace; own ALBs; PR → deploy to staging.
- **Production**: Manual approval (or tag) → deploy to production.

---

## References

- Full checklist: [EXECUTION-GUIDE.md](EXECUTION-GUIDE.md)
- Architecture and diagrams: [ARCHITECTURE.md](ARCHITECTURE.md)
- Phase summaries: [docs/README.md](docs/README.md)
