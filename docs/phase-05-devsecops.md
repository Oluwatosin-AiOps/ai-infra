# Phase 5 — DevSecOps Integration

**Full checklist:** [EXECUTION-GUIDE.md — Phase 5](../EXECUTION-GUIDE.md#phase-5--devsecops-integration) (Steps 10–11)

---

## Summary

Add CI/CD with security scanning and policy enforcement so deployments are repeatable and secure.

- **Step 10:** GitHub Actions: lint, unit tests, container build (backend + frontend), Trivy scan, push to ECR, Terraform plan/apply, Helm upgrade; use secrets for ECR/AWS/kubeconfig; document branch/tag strategy (e.g. PR → staging, main → prod).
- **Step 11:** OPA Gatekeeper, ConstraintTemplates/Constraints (e.g. labels, no `latest` tag), Pod Security Standards, optional image signing; verify policies block non-compliant workloads; document policy set.

Every sub-step is in the execution guide; do not skip any.
