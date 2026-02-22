# Phase 2 — Containerization Strategy

**Full checklist:** [EXECUTION-GUIDE.md — Phase 2](../EXECUTION-GUIDE.md#phase-2--containerization-strategy) (Steps 4–5)

---

## Summary

Containerize both services and push images to Amazon ECR so deployment and CI/CD can use immutable artifacts.

- **Step 4:** Add `backend/Dockerfile` and `frontend/Dockerfile`: slim base images, non-root user, health checks (and multi-stage if useful).
- **Step 5:** Create ECR repos `fraud-backend` and `fraud-frontend`; build, tag, and push both images (and later integrate push into CI).

Every sub-step is listed in the execution guide; complete all checkboxes for this phase.
