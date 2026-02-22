# Phase 3 — Infrastructure as Code with Terraform

**Full checklist:** [EXECUTION-GUIDE.md — Phase 3](../EXECUTION-GUIDE.md#phase-3--infrastructure-as-code-with-terraform) (Steps 6–7)

---

## Summary

Provision AWS core networking and the EKS cluster with Terraform so infrastructure is declarative and reproducible.

- **Step 6:** VPC, 3 AZs, public and private subnets, Internet Gateway, NAT Gateway, route tables, security groups, IAM roles; then `terraform plan` / `apply`.
- **Step 7:** EKS cluster, node groups with autoscaling, OIDC provider, IRSA for pod IAM; verify `kubectl` and node readiness.

All items are in the execution guide; tick each off as you complete it.
