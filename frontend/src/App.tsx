import { useState } from "react";

// In dev with Vite proxy: use "" or same origin so /api is proxied to backend (no CORS).
// In production: set VITE_API_URL to your Backend ALB URL.
const API_BASE =
  import.meta.env.VITE_API_URL === ""
    ? ""
    : (import.meta.env.VITE_API_URL ?? "");
if (!API_BASE && import.meta.env.DEV) {
  // Dev with proxy: requests go to same origin, then proxied to backend.
  // No need to set VITE_API_URL for local dev.
}
if (!API_BASE && !import.meta.env.DEV) {
  console.warn("VITE_API_URL is not set; predict requests will fail.");
}

type PredictResponse = {
  fraud_probability: number;
  is_fraud: boolean;
};

const SAMPLE_JSON = `{
  "V1": -1.0, "V2": 0.5, "V3": -0.2, "V4": 0.1, "V5": -0.5,
  "V6": 0.3, "V7": 0.0, "V8": -0.1, "V9": 0.2, "V10": -0.3,
  "V11": 0.1, "V12": 0.0, "V13": -0.2, "V14": 0.1, "V15": 0.0,
  "V16": -0.1, "V17": 0.0, "V18": 0.1, "V19": -0.1, "V20": 0.0,
  "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0,
  "V26": 0.0, "V27": 0.0, "V28": 0.0, "Amount": 10.0
}`;

export default function App() {
  const [json, setJson] = useState(SAMPLE_JSON);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    if (!API_BASE && !import.meta.env.DEV) {
      setError("VITE_API_URL is not set. Add it to .env (see .env.example).");
      return;
    }
    let body: unknown;
    try {
      body = JSON.parse(json);
    } catch {
      setError("Invalid JSON. Paste a single transaction object with V1–V28 and Amount.");
      return;
    }
    setLoading(true);
    try {
      const base = API_BASE.replace(/\/$/, "");
      const url = base ? `${base}/api/v1/predict` : "/api/v1/predict";
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail ?? `HTTP ${res.status}`);
        return;
      }
      setResult(data as PredictResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 560, margin: "0 auto" }}>
      <h1 style={{ marginBottom: "0.25rem" }}>Fraud Detection</h1>
      <p style={{ color: "#94a3b8", marginBottom: "1.5rem" }}>
        Paste transaction JSON (V1–V28, Amount) and submit to the backend API.
      </p>
      <form onSubmit={handleSubmit}>
        <label style={{ display: "block", marginBottom: "0.5rem", fontWeight: 500 }}>
          Transaction (JSON)
        </label>
        <textarea
          value={json}
          onChange={(e) => setJson(e.target.value)}
          rows={8}
          style={{
            width: "100%",
            padding: "0.75rem",
            fontFamily: "monospace",
            fontSize: "0.875rem",
            background: "#1e293b",
            border: "1px solid #334155",
            borderRadius: 6,
            color: "#e2e8f0",
          }}
          spellCheck={false}
        />
        <div style={{ display: "flex", gap: "0.75rem", marginTop: "0.75rem" }}>
          <button
            type="button"
            onClick={() => setJson(SAMPLE_JSON)}
            style={btnStyle}
          >
            Use sample
          </button>
          <button type="submit" disabled={loading} style={{ ...btnStyle, ...primaryBtnStyle }}>
            {loading ? "Submitting…" : "Predict"}
          </button>
        </div>
      </form>
      {error && (
        <div style={{ marginTop: "1rem", padding: "0.75rem", background: "#7f1d1d", borderRadius: 6 }}>
          {error}
        </div>
      )}
      {result && (
        <div style={{ marginTop: "1rem", padding: "1rem", background: "#1e293b", borderRadius: 8 }}>
          <div style={{ fontWeight: 600, marginBottom: "0.5rem" }}>Result</div>
          <div>
            <strong>Fraud probability:</strong> {(result.fraud_probability * 100).toFixed(2)}%
          </div>
          <div>
            <strong>Label:</strong>{" "}
            <span style={{ color: result.is_fraud ? "#f87171" : "#86efac" }}>
              {result.is_fraud ? "Fraud" : "Not fraud"}
            </span>
          </div>
        </div>
      )}
      <p style={{ marginTop: "1.5rem", fontSize: "0.75rem", color: "#64748b" }}>
        API base: {API_BASE || "(dev: proxied from /api)"}
      </p>
    </div>
  );
}

const btnStyle: React.CSSProperties = {
  padding: "0.5rem 1rem",
  borderRadius: 6,
  border: "1px solid #475569",
  background: "#334155",
  color: "#e2e8f0",
  cursor: "pointer",
  fontSize: "0.875rem",
};

const primaryBtnStyle: React.CSSProperties = {
  background: "#2563eb",
  borderColor: "#2563eb",
};
