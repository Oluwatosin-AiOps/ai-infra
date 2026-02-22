# Phase 1 — Application Foundation

**Full checklist:** [EXECUTION-GUIDE.md — Phase 1](../EXECUTION-GUIDE.md#phase-1--application-foundation) (Steps 1–3)

---

## Summary

Set up the application layer: a minimal **Python/FastAPI** backend (from the full-stack-fastapi-template, stripped) and a **Next.js** frontend. The backend will get an ML fraud model and a `POST /predict` endpoint; the frontend will be a separate microservice that calls that API over its public URL.

- **Step 1:** Clone full-stack-fastapi-template; strip to backend API core, dependency management, and container scaffolding; remove default frontend, auth, email, admin.
- **Step 2:** Add fraud detection: Kaggle Credit Card Fraud dataset, train model (e.g. scikit-learn/XGBoost), joblib serialize; expose `POST /predict` with validation and docs.
- **Step 3:** Build lightweight **Next.js** UI: form → call inference API → show fraud probability; deployable as its own container; no shared infra with backend.

Nothing in this phase is skipped; every sub-item is in the execution guide with a checkbox.
