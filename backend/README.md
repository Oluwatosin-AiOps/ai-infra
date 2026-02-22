# Fraud Detection API (Backend)

**Tech:** **Python / FastAPI.**  
**Role:** ML inference API for fraud detection. Exposes `POST /predict` (and `/api/v1/utils/health-check/`). This is the **backend** microservice: its own container, deployment on EKS, and **own load balancer** (see [ARCHITECTURE.md](../ARCHITECTURE.md)).

Minimal FastAPI app stripped from [full-stack-fastapi-template](https://github.com/tiangolo/full-stack-fastapi-template). The frontend is a separate **Next.js** service that calls this API over its public URL.

## What’s included

- FastAPI app with `/api/v1/utils/health-check/`
- Pydantic settings, CORS, optional Sentry
- `pyproject.toml` + `uv` for dependencies
- Dockerfile (slim image, non-root user, health check)
- Scripts: `lint.sh`, `format.sh`, `test.sh`
- Pytest and Ruff

## Run locally

```bash
# From backend/
cp .env.example .env   # optional
uv sync
uv run fastapi dev app/main.py
# API: http://localhost:8000
# Docs: http://localhost:8000/api/v1/docs
```

## Tests and lint

```bash
uv run pytest tests/ -v
uv run ruff check app tests
uv run ruff format app tests
```

## Docker

Build (from repo root):

```bash
docker build -f backend/Dockerfile backend/
```

Run:

```bash
docker run -p 8000:8000 <image-id>
# Health: http://localhost:8000/api/v1/utils/health-check/
```

## Next (Execution Guide)

- **Step 2:** Add ML model and `POST /predict` for fraud detection.
