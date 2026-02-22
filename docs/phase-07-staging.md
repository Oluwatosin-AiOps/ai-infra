# Phase 7 — Staging Environment

**Full checklist:** [EXECUTION-GUIDE.md — Phase 7](../EXECUTION-GUIDE.md#phase-7--staging-environment) (Step 16)

---

## Summary

Add a staging environment that mirrors production so you can deploy from PRs to staging and promote to production after approval.

- **Step 16:** Create `staging` namespace; separate Terraform workspace (or module) for staging; separate load balancers for backend and frontend; deploy both services to staging; CI: PR → staging deploy, manual approval (or tag) → production; document parity and promotion.

Every sub-item is in the execution guide; complete all checkboxes for this phase.
