# Fraud Detection API (Backend)

**Tech:** **Python / FastAPI.**  
**Role:** ML inference API for fraud detection. Exposes `POST /predict` (and `/api/v1/utils/health-check/`). This is the **backend** microservice: its own container, deployment on EKS, and **own load balancer** (see [ARCHITECTURE.md](../ARCHITECTURE.md)).

Minimal FastAPI app stripped from [full-stack-fastapi-template](https://github.com/tiangolo/full-stack-fastapi-template). The frontend is a separate **Next.js** service that calls this API over its public URL.

## What’s included

- FastAPI app with `/api/v1/utils/health-check/` and **`POST /api/v1/predict`** (fraud detection)
- ML: scikit-learn RandomForest, joblib-serialized model in `app/model/model.joblib`
- Pydantic settings, CORS, optional Sentry
- `pyproject.toml` + `uv` for dependencies
- Dockerfile (slim image, non-root user, health check)
- Scripts: `lint.sh`, `format.sh`, `test.sh`, `train_model.py`, `download_data.py`
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

## ML model (Step 2)

- **Train (synthetic):** `uv run python scripts/train_model.py --synthetic --output app/model/model.joblib`
- **Train (Kaggle data):** place `creditcard.csv` in `data/`, then `uv run python scripts/train_model.py`
- **Download data:** `uv run python scripts/download_data.py` (requires Kaggle CLI and `~/.kaggle/kaggle.json`)
- **Predict:** `POST /api/v1/predict` with JSON body `{ "V1".."V28", "Amount" }`; response `{ "fraud_probability", "is_fraud" }`
- OpenAPI: `http://localhost:8000/api/v1/docs`

## Next (Execution Guide)

- **Step 3:** Build the Next.js frontend.
