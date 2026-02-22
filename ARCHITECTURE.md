# Kubernetes-First AI Fraud Detection Platform — Architecture

This document describes the target architecture and provides diagrams you can use during execution. Render the Mermaid diagrams in GitHub, VS Code (with a Mermaid extension), or at [mermaid.live](https://mermaid.live).

**Visual overview:** See `assets/architecture-diagram.png` for a single-page diagram of the system.

---

## 1. High-Level System Context

Users hit the **frontend** via its own load balancer; the frontend calls the **backend** inference API via the backend’s own load balancer. No shared ALB — true microservice boundaries.

```mermaid
flowchart LR
    subgraph Users
        U[User / Browser]
    end

    subgraph AWS["AWS Cloud"]
        subgraph FrontendBoundary["Frontend Microservice"]
            ALB_F[Frontend ALB]
            FE[Frontend Pods]
            ALB_F --> FE
        end
        subgraph BackendBoundary["Backend Microservice"]
            ALB_B[Backend ALB]
            BE[Backend API Pods]
            ALB_B --> BE
        end
    end

    U -->|HTTPS| ALB_F
    FE -->|POST /predict| ALB_B
    BE -->|Fraud probability| FE
```

---

## 2. AWS Infrastructure (Terraform)

VPC with public and private subnets across 3 AZs, EKS in private subnets, NAT for egress, and ECR for images.

```mermaid
flowchart TB
    subgraph Internet["Internet"]
        Users[Users]
    end

    subgraph AWS["AWS Account"]
        subgraph VPC["VPC"]
            subgraph AZ1["AZ 1"]
                Pub1[Public Subnet]
                Priv1[Private Subnet]
            end
            subgraph AZ2["AZ 2"]
                Pub2[Public Subnet]
                Priv2[Private Subnet]
            end
            subgraph AZ3["AZ 3"]
                Pub3[Public Subnet]
                Priv3[Private Subnet]
            end

            IGW[Internet Gateway]
            NAT[NAT Gateway]
        end

        subgraph EKS["EKS Cluster"]
            CP[Control Plane]
            NG[Node Group]
        end

        ECR[ECR: fraud-backend\nfraud-frontend]
    end

    Users --> IGW
    IGW --> Pub1
    IGW --> Pub2
    IGW --> Pub3
    Priv1 --> NAT
    Priv2 --> NAT
    Priv3 --> NAT
    NAT --> IGW
    NG --> Priv1
    NG --> Priv2
    NG --> Priv3
    EKS -.->|pull images| ECR
```

---

## 3. EKS Deployment — Services and Load Balancers

Each app has its own Deployment, Service, HPA, and external entry (ALB). OPA Gatekeeper and observability run in the same cluster.

```mermaid
flowchart TB
    subgraph External["External"]
        User[User]
    end

    subgraph ALBs["Application Load Balancers"]
        ALB_FE[Frontend ALB]
        ALB_BE[Backend ALB]
    end

    subgraph EKS["EKS Cluster"]
        subgraph NS_Default["default / production namespace"]
            subgraph Frontend["Frontend Microservice"]
                SVC_FE[Service: ClusterIP]
                DP_FE[Deployment]
                HPA_FE[HPA]
                SVC_FE --> DP_FE
                HPA_FE -.->|scales| DP_FE
            end
            subgraph Backend["Backend Microservice"]
                SVC_BE[Service: ClusterIP]
                DP_BE[Deployment]
                HPA_BE[HPA]
                SVC_BE --> DP_BE
                HPA_BE -.->|scales| DP_BE
            end
        end

        subgraph Observability["Observability Stack"]
            Prom[Prometheus]
            Graf[Grafana]
            Loki[Loki]
            Jaeger[Jaeger]
        end

        subgraph Policy["DevSecOps"]
            OPA[OPA Gatekeeper]
        end
    end

    User --> ALB_FE
    ALB_FE --> SVC_FE
    SVC_FE -->|calls API| ALB_BE
    ALB_BE --> SVC_BE
    DP_FE -->|metrics, logs, traces| Prom
    DP_BE -->|metrics, logs, traces| Prom
    Prom --> Graf
    Loki --> Graf
    Jaeger --> Graf
    OPA -.->|validates| DP_FE
    OPA -.->|validates| DP_BE
```

---

## 4. Request Flow — Fraud Check

End-to-end path from browser to ML inference and back.

```mermaid
sequenceDiagram
    participant U as User
    participant ALB_F as Frontend ALB
    participant FE as Frontend Pod
    participant ALB_B as Backend ALB
    participant BE as Backend Pod
    participant Model as ML Model

    U->>ALB_F: HTTPS (form load)
    ALB_F->>FE: Request
    FE->>U: UI (form)

    U->>ALB_F: Submit transaction
    ALB_F->>FE: POST form
    FE->>ALB_B: POST /predict (JSON)
    ALB_B->>BE: POST /predict
    BE->>Model: inference
    Model->>BE: fraud probability
    BE->>ALB_B: 200 + probability
    ALB_B->>FE: Response
    FE->>ALB_F: Render result
    ALB_F->>U: Result (fraud score)
```

---

## 5. CI/CD and Security Pipeline

GitHub Actions: lint → test → build → scan → push ECR → Terraform → Helm. OPA enforces policy at deploy time.

```mermaid
flowchart LR
    subgraph GH["GitHub"]
        Code[Source Code]
        PR[Pull Request]
    end

    subgraph Actions["GitHub Actions"]
        Lint[Lint]
        Test[Unit Tests]
        Build[Build Images]
        Trivy[Trivy Scan]
        Push[Push ECR]
        TF[Terraform Plan/Apply]
        Helm[Helm Upgrade]
    end

    subgraph AWS["AWS"]
        ECR[ECR]
        EKS[EKS]
    end

    subgraph EKS_Detail["EKS"]
        OPA[OPA Gatekeeper]
        Pods[Pods]
    end

    Code --> PR
    PR --> Lint --> Test --> Build --> Trivy --> Push
    Push --> ECR
    ECR --> TF --> Helm
    Helm --> EKS
    OPA -.->|admission| Pods
```

---

## 6. Observability and SLOs

Golden Signals and SLOs are derived from Prometheus metrics; Grafana and Alertmanager consume them.

```mermaid
flowchart TB
    subgraph Workloads["Workloads"]
        FE[Frontend]
        BE[Backend]
    end

    subgraph Metrics["Metrics & Logs & Traces"]
        Prom[Prometheus]
        Loki[Loki]
        Jaeger[Jaeger]
    end

    subgraph SLO["SLI / SLO"]
        Recording[Recording Rules]
        Avail[Availability 99.5%]
        Latency[p95 < 200ms]
        Burn[Error Budget Burn]
    end

    subgraph Consumption["Consumption"]
        Grafana[Grafana Dashboards]
        AM[Alertmanager]
    end

    FE --> Prom
    BE --> Prom
    FE --> Loki
    BE --> Loki
    FE --> Jaeger
    BE --> Jaeger
    Prom --> Recording
    Recording --> Avail
    Recording --> Latency
    Recording --> Burn
    Avail --> Grafana
    Latency --> Grafana
    Burn --> Grafana
    Recording --> AM
```

---

## 7. Staging vs Production (Environments)

Staging mirrors production (separate namespace, own ALBs, same code path). Promotion is PR → staging, approval → production.

```mermaid
flowchart LR
    subgraph CI["CI/CD"]
        PR[Pull Request]
        StagingDeploy[Deploy to Staging]
        Approval[Manual Approval]
        ProdDeploy[Deploy to Production]
    end

    subgraph Staging["Staging (EKS)"]
        NS_S[namespace: staging]
        ALB_FE_S[Frontend ALB]
        ALB_BE_S[Backend ALB]
    end

    subgraph Production["Production (EKS)"]
        NS_P[namespace: default/prod]
        ALB_FE_P[Frontend ALB]
        ALB_BE_P[Backend ALB]
    end

    PR --> StagingDeploy --> NS_S
    StagingDeploy --> ALB_FE_S
    StagingDeploy --> ALB_BE_S
    Approval --> ProdDeploy --> NS_P
    ProdDeploy --> ALB_FE_P
    ProdDeploy --> ALB_BE_P
```

---

## 8. Component Summary

| Layer            | Components |
|------------------|------------|
| **Applications** | FastAPI backend (ML inference), React/Next.js frontend |
| **Containers**   | Backend + Frontend images in ECR |
| **Orchestration**| EKS, separate Deployments/Services/HPAs per app |
| **Entry**        | One ALB per service (frontend ALB, backend ALB) |
| **Infrastructure** | Terraform: VPC, 3 AZs, public/private subnets, NAT, IGW, EKS, IRSA |
| **CI/CD**        | GitHub Actions: lint, test, build, Trivy, ECR, Terraform, Helm |
| **Security**     | OPA Gatekeeper, Pod Security Standards, Trivy |
| **Observability**| Prometheus, Grafana, Loki, Jaeger; Golden Signals + SLO dashboards |
| **Environments** | Staging + Production with separate namespaces and ALBs |

Use this document alongside **EXECUTION-GUIDE.md** and tick off phases step by step.

image.png


