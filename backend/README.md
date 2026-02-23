# Backend — Fraud Detection API

FastAPI service that serves ML inference for fraud detection. Intentionally a separate microservice: its own container, deployment, and load balancer (see [ARCHITECTURE.md](../ARCHITECTURE.md)). The UI runs elsewhere and calls this API over HTTP using an env-configured base URL.

---

## What’s in here

- **Endpoints:** `GET /api/v1/utils/health-check/`, `POST /api/v1/predict` (transaction → fraud probability + label).
- **Model:** Scikit-learn RandomForest, serialized with joblib under `app/model/`. Configurable via `MODEL_PATH`.
- **Stack:** FastAPI, Pydantic, optional Sentry. CORS is configurable; required when the frontend is on another origin (e.g. production). No DB in this service.

---

## Run locally

```bash
cp .env.example .env   # optional; add BACKEND_CORS_ORIGINS if frontend hits this directly
uv sync
uv run fastapi dev app/main.py
```

- API: `http://127.0.0.1:8000`
- OpenAPI: `http://127.0.0.1:8000/api/v1/docs`

---

## Tests and lint

```bash
uv run pytest tests/ -v
uv run ruff check app tests
uv run ruff format app tests
```

---

## Model training

- **Synthetic (no dataset):**  
  `uv run python scripts/train_model.py --synthetic --output app/model/model.joblib`
- **Kaggle Credit Card Fraud:**  
  Put `creditcard.csv` in `data/`, then:  
  `uv run python scripts/train_model.py`
- **Download dataset:**  
  `uv run python scripts/download_data.py` (requires Kaggle CLI and `~/.kaggle/kaggle.json`)

Predict request: JSON with `V1`–`V28` and `Amount`. Response: `fraud_probability` (0–1) and `is_fraud` (boolean). See OpenAPI for schema.

---

## Docker

From repo root:

```bash
docker build -f backend/Dockerfile backend/
docker run -p 8000:8000 <image-id>
```

Health: `GET http://localhost:8000/api/v1/utils/health-check/`

---

## Env (`.env`)

- `BACKEND_CORS_ORIGINS` — Comma-separated origins (e.g. `http://localhost:5173`) or JSON array. Required when the frontend is on another origin; not needed when using the frontend dev proxy.
- `MODEL_PATH` — Path to the joblib model (default `app/model/model.joblib`).
- Optional: `SENTRY_DSN`, `ENVIRONMENT`, `PROJECT_NAME`. See `.env.example`.
