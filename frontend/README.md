# Fraud Detection UI (Frontend)

**Tech:** **Next.js** (Node.js).  
**Role:** Lightweight UI for the fraud detection platform. Users enter transaction data; the app calls the **Python/FastAPI ML backend** (its own service and load balancer) and displays fraud probability.

This frontend is a **separate microservice**: its own container, own deployment on EKS, and **own load balancer**. It does not share infrastructure with the backend (see [ARCHITECTURE.md](../ARCHITECTURE.md)).

---

## Status

- **Phase 1 Step 3** in [EXECUTION-GUIDE.md](../EXECUTION-GUIDE.md): build the Next.js app here (form → call inference API → show result).
- Until then, this directory only contains this README.

---

## Planned structure (after Step 3)

- Next.js app (e.g. `src/`, `package.json`, `next.config.js`).
- Form for transaction features → `POST /predict` to backend API URL (env config).
- Display fraud probability (and optional label).
- Dockerfile for containerization (Phase 2 Step 4).

---

## Docs

- Full checklist: [EXECUTION-GUIDE.md](../EXECUTION-GUIDE.md) — Phase 1 Step 3, Phase 2 Step 4, Phase 4 Step 9.
- Phase summary: [docs/phase-01-foundation.md](../docs/phase-01-foundation.md).
- Tech stack: [TECH-STACK.md](../TECH-STACK.md).
