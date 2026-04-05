# Full System Roadmap

## Phase 1 — Core Infrastructure
- [ ] Set up repository structure
- [ ] Configure k3s cluster
- [ ] Deploy database (Postgres/Timescale/ClickHouse)
- [ ] Deploy Redis (optional caching)
- [ ] Set up CI/CD pipeline

---

## Phase 2 — Market Data Layer
- [ ] Implement market-data service
- [ ] Connect to external REST/WebSocket sources
- [ ] Normalize and store candles/trades
- [ ] Provide internal API for last N candles

---

## Phase 3 — Analytics Layer
- [ ] Implement analytics-service
- [ ] Calculate indicators
- [ ] Generate signals
- [ ] Detect patterns
- [ ] Write results to database

---

## Phase 4 — API Gateway
- [ ] Implement backend-api (FastAPI)
- [ ] Expose REST endpoints for frontend
- [ ] Integrate with analytics and market-data services
- [ ] Add authentication

---

## Phase 5 — Frontend
- [ ] Implement UI (Vue or Svelte)
- [ ] Integrate lightweight-charts
- [ ] Display candles, indicators, signals
- [ ] Add routing and settings
- [ ] Add authentication UI

---

## Phase 6 — Alerts & Worker Layer
- [ ] Implement alert-service
- [ ] Implement worker-service (optional)
- [ ] Add notification channels
- [ ] Add scheduled tasks

---

## Phase 7 — Observability & Optimization
- [ ] Add Prometheus/Grafana monitoring
- [ ] Add centralized logging
- [ ] Optimize database queries
- [ ] Add caching where needed

---

## Phase 8 — Production Hardening
- [ ] Load testing
- [ ] Failover testing
- [ ] Backup/restore procedures
- [ ] Security hardening

---

# 🗺️ Summary

## Phase 1 — Infrastructure
- k3s cluster, DB, CI/CD

## Phase 2 — Market Data Layer
- ingestion, normalization, storage

## Phase 3 — Analytics Layer
- indicators, signals, patterns

## Phase 4 — API Gateway
- REST API for frontend

## Phase 5 — Frontend
- charts, UI, auth

## Phase 6 — Alerts & Workers
- alert-service, worker-service, notifications

## Phase 7 — Observability
- monitoring, logging, optimization

## Phase 8 — Production Hardening
- load testing, failover, backups, security

---

# 📚 Related Documents

- [Frontend TODO](/ui/TODO.md)
- [DB TODO](/db/TODO.md)
- [Api-Gateway TODO](/services/api-gateway/TODO.md)
- [Market-Data-Service TODO](/services/market-data/TODO.md)
- [Analytics-Service TODO](/services/analytics/TODO.md)
- [Alert-Service TODO](/services/alert-service/TODO.md)
- [Worker-Service TODO](/services/worker-service/TODO.md)
- [Scheduler TODO](/services/scheduler/TODO.md)
