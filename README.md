# Kubernetes-First AI Fraud Detection Platform on AWS

A production-grade, full-stack DevSecOps and observability implementation: ML inference API for fraud detection, separate UI microservice, independent load balancers, EKS, Terraform, CI/CD with security scanning, and SLO-driven observability.

---

## Tech stack

| Layer        | Technology |
|-------------|------------|
| **Frontend** | **Next.js** (Node.js) — lightweight UI; own container and load balancer |
| **Backend**  | **Python / FastAPI** — ML inference API (`POST /predict`); own container and load balancer |
| **Infra**    | Terraform, AWS (VPC, EKS, ECR, ALB), Kubernetes |
| **CI/CD**    | GitHub Actions (lint, test, Trivy, Terraform, Helm) |
| **Security** | OPA Gatekeeper, Pod Security Standards |
| **Observability** | Prometheus, Grafana, Loki, Jaeger; Golden Signals + SLOs |

Two separate backends by design: **frontend** (Next.js) and **ML API** (Python/FastAPI), each with its own deployment and ALB.

---

## Repo structure

```
ai-infra/
├── backend/          # Python FastAPI — ML inference API (fraud detection)
├── frontend/         # Next.js — UI; calls backend API via its public URL
├── docs/             # Phase summaries and links to execution guide
├── ARCHITECTURE.md   # Diagrams and architecture description
├── EXECUTION-GUIDE.md # Step-by-step checklist (nothing skipped)
├── README.md         # This file
└── .gitignore
```

- **Backend**: FastAPI app, `/api/v1/utils/health-check/`, later `POST /predict`. See [backend/README.md](backend/README.md).
- **Frontend**: Next.js app (Phase 1 Step 3), form → call backend → show fraud score. See [frontend/README.md](frontend/README.md).

---

## Documentation

| Document | Purpose |
|----------|---------|
| [**ARCHITECTURE.md**](ARCHITECTURE.md) | System and AWS diagrams, request flow, CI/CD, observability, staging vs prod. |
| [**EXECUTION-GUIDE.md**](EXECUTION-GUIDE.md) | Full step-by-step checklist; update checkboxes as you complete items. **Nothing is omitted; every phase and step is listed.** |
| [**TECH-STACK.md**](TECH-STACK.md) | Canonical tech choices (Next.js, Python/FastAPI, Terraform, EKS, etc.). |
| [**docs/README.md**](docs/README.md) | Phase overview with short summaries and links into the execution guide. |
| [**docs/phase-01-foundation.md**](docs/phase-01-foundation.md) … **phase-08** | Per-phase summary and link to the relevant section of the execution guide. |

---

## Execution (in order)

1. Use **[EXECUTION-GUIDE.md](EXECUTION-GUIDE.md)** as the single source of steps; complete every item and checkbox.
2. Before each phase, read the corresponding **docs/phase-XX-…** summary and **[ARCHITECTURE.md](ARCHITECTURE.md)** for context.
3. Run phases in order: **Phase 1** (application foundation) → **Phase 2** (containers) → … → **Phase 8** (autoscaling and load testing).

---

## Quick start (development)

- **Backend (Python):** `cd backend && uv sync && uv run fastapi dev app/main.py` → http://localhost:8000
- **Frontend (Next.js):** after Phase 1 Step 3, `cd frontend && pnpm install && pnpm dev` → http://localhost:3000
