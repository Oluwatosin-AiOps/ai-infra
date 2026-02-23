# Frontend — Fraud Detection UI

Vite + React (TypeScript) SPA. Single responsibility: accept transaction JSON, call the backend `POST /api/v1/predict`, show fraud probability and label. Deployed as its own service with its own load balancer; backend URL is always from environment, never hardcoded.

---

## Env: backend URL

| Variable | Purpose |
|----------|---------|
| `VITE_API_URL` | Backend API base URL (no trailing slash). Inlined at build time. |

- **Local dev:** Leave unset (or empty) to use the Vite proxy: requests to `/api` are proxied to `http://127.0.0.1:8000`. No CORS needed.
- **Production / CI:** Set to the Backend ALB (e.g. `https://api.example.com`) at build time so the same artifact works across environments.

Never hardcode the API host in source. That breaks staging/prod and is a common cause of “works on my machine” in CI/CD.

---

## Prerequisites

- Node.js LTS and npm (or pnpm/yarn).  
  If `npm` is missing: install Node via [nodejs.org](https://nodejs.org/), Homebrew (`brew install node`), or nvm. Restart the terminal after installing.

---

## Run locally

```bash
npm install
npm run dev
```

Open `http://localhost:5173`. With the default proxy, the backend should be running at `http://127.0.0.1:8000`; the app will send requests to `/api/v1/predict` and the dev server will proxy them.

---

## Build

```bash
npm run build
```

Output: `dist/`. For production, set `VITE_API_URL` before building (e.g. in CI or via Docker build-arg).

---

## How it talks to the backend

- **Request:** `POST ${base}/api/v1/predict` with JSON body `{ "V1", "V2", … "V28", "Amount" }`.
- **Response:** `{ "fraud_probability": number, "is_fraud": boolean }`.
- In dev with proxy, `base` is the dev server origin so `/api` is proxied; in production, `base` is `VITE_API_URL`.

---

## Further

- Execution guide: [EXECUTION-GUIDE.md](../EXECUTION-GUIDE.md) (Phase 2 Step 4: Dockerfile; Phase 4 Step 9: deploy to EKS).
- Architecture: [ARCHITECTURE.md](../ARCHITECTURE.md).  
- Tech choices: [TECH-STACK.md](../TECH-STACK.md).
