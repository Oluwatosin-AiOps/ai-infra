# Kubernetes-First AI Fraud Detection Platform

Production-oriented stack: ML inference API (FastAPI), separate UI (Vite + React), independent load balancers per service, EKS, Terraform, and SLO-driven observability. Built to demonstrate real microservice boundaries and operational maturity, not a single-stack demo.

---

## Stack

| Layer | Choice | Notes |
|-------|--------|--------|
| **Frontend** | Vite + React (TS) | Thin client; backend URL from `VITE_API_URL` (never hardcoded). Own container and ALB. |
| **Backend** | Python 3.10+ / FastAPI | `POST /api/v1/predict` (fraud), health at `/api/v1/utils/health-check/`. Own container and ALB. |
| **Infra** | Terraform, EKS, ECR | VPC (3 AZs), separate ALBs per app. |
| **CI/CD** | GitHub Actions | Lint, test, build, Trivy, ECR, Terraform, Helm. |
| **Observability** | Prometheus, Grafana, Loki, Jaeger | Golden Signals and SLOs. |

Two services by design—frontend and ML API—each with its own deployment and load balancer. See [ARCHITECTURE.md](ARCHITECTURE.md) for diagrams.

---

## Repo layout

```
├── backend/          # FastAPI app, ML model, train/download scripts
├── frontend/         # Vite + React UI; calls backend via env-configured URL
├── docs/             # Phase summaries + links to execution guide
├── ARCHITECTURE.md   # Diagrams, request flow, infra
├── EXECUTION-GUIDE.md # Full checklist (local; not committed)
├── TECH-STACK.md     # Canonical tech list
└── README.md
```

- [backend/README.md](backend/README.md) — Run, test, train model, Docker.
- [frontend/README.md](frontend/README.md) — Run, build, env vars, proxy for local dev.

---

## Docs

| Doc | Use |
|-----|-----|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System context, AWS layout, CI/CD and observability flow. |
| [EXECUTION-GUIDE.md](EXECUTION-GUIDE.md) | Step-by-step checklist (all phases). Kept local; update checkboxes as you go. |
| [TECH-STACK.md](TECH-STACK.md) | Canonical technologies per layer. |
| [docs/README.md](docs/README.md) | Phase index and links into the execution guide. |

Execute phases in order (1 → 8). Use the execution guide as the single source of truth.

---

## Local run

**Backend**

```bash
cd backend
cp .env.example .env   # set BACKEND_CORS_ORIGINS if needed
uv sync
uv run fastapi dev app/main.py
```

API: `http://127.0.0.1:8000` · Docs: `http://127.0.0.1:8000/api/v1/docs`

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

App: `http://localhost:5173`. In dev, `/api` is proxied to the backend (see frontend README); no CORS setup required for local use.
