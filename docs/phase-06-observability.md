# Phase 6 — Observability and SLO Engineering

**Full checklist:** [EXECUTION-GUIDE.md — Phase 6](../EXECUTION-GUIDE.md#phase-6--observability-and-slo-engineering) (Steps 12–15)

---

## Summary

Deploy the monitoring stack, instrument Golden Signals, define SLIs/SLOs, and build Grafana dashboards that map to those SLOs.

- **Step 12:** Deploy Prometheus, Grafana, Loki, Jaeger (e.g. Helm); configure scrape and data sources; confirm metrics, logs, traces.
- **Step 13:** Golden Signals for both services: latency, traffic, errors, saturation, availability; request duration, 5xx rate, CPU, memory, pod restarts, ALB response time.
- **Step 14:** Define SLIs (e.g. success ratio) and SLOs (e.g. 99.5% availability, p95 &lt; 200 ms); Prometheus recording rules, Alertmanager, Grafana SLO dashboards.
- **Step 15:** Grafana: availability, latency percentiles, error budget burn rate, traffic growth, saturation heatmaps; each dashboard tied to an SLO.

All items are listed in the execution guide; complete each checkbox.
