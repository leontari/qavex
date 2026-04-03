# TODO — Market Data Service

## 🎯 Objectives
- [ ] Connect to external market data sources via REST and/or WebSocket
- [ ] Normalize incoming data (candles, trades, orderbook snapshots)
- [ ] Publish normalized data into a queue or write directly into the database

---

## 🔌 Interface
- [ ] Provide gRPC/HTTP API for internal services:
  - [ ] Get last N candles
  - [ ] Get latest trades
  - [ ] Get current orderbook snapshot (optional)
- [ ] Write normalized data directly into database tables:
  - [ ] `candles`
  - [ ] `trades`
- [ ] Add schema validation for incoming data
- [ ] Add retry/backoff logic for unstable data sources

---

## 🔄 Interactions

### 📥 Data Ingestion
- [ ] Connect to external REST endpoints
- [ ] Connect to external WebSocket streams
- [ ] Reconnect automatically on disconnect
- [ ] Buffer incoming data (optional)
- [ ] Normalize raw data into internal format

### 🗄️ Data Storage
- [ ] Write candles into `candles` table
- [ ] Write trades into `trades` table
- [ ] Add batching for high‑frequency data (optional)
- [ ] Add deduplication logic (optional)

### 📤 Data Serving
- [ ] Implement endpoint: `get_last_candles(symbol, limit)`
- [ ] Implement endpoint: `get_last_trades(symbol, limit)`
- [ ] Add caching layer for frequently requested symbols/timeframes
- [ ] Add metrics for data throughput and latency

---

## 🧪 Testing
- [ ] Mock external REST/WebSocket sources
- [ ] Test normalization logic
- [ ] Test database writes under load
- [ ] Test gRPC/HTTP endpoints
- [ ] Benchmark ingestion performance

---

## ☸️ Deployment (optional)
- [ ] Add k3s Deployment manifest
- [ ] Add liveness/readiness probes
- [ ] Add autoscaling rules (HPA)
- [ ] Add logging and monitoring (Prometheus/Grafana)

---

## 📚 Documentation
- [ ] Create `docs/market-data-service.md`
- [ ] Document supported data sources
- [ ] Document normalization rules
- [ ] Document API endpoints
- [ ] Add examples of raw vs normalized data
