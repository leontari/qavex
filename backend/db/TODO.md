# TODO — DB Service (Postgres / Timescale / ClickHouse)

## 🎯 Objectives
- [ ] Store historical market data (candles, orderbook snapshots, trades)
- [ ] Store user data (profiles, auth, settings)
- [ ] Store analytics results (indicators, signals, patterns)
- [ ] Deploy as StatefulSet with PVCs in k3s

---

## 🗄️ Database Setup
- [ ] Choose primary database engine:
  - [ ] Postgres
  - [ ] TimescaleDB (for time-series)
  - [ ] ClickHouse (for high-volume analytics)
- [ ] Configure database schemas
- [ ] Configure retention policies (if using Timescale)
- [ ] Configure partitions (if using ClickHouse)
- [ ] Set up indexes for fast queries
- [ ] Add migrations system (Alembic or SQL files)

---

## 🔌 Interface
- [ ] Provide access for internal services:
  - [ ] API-service (read/write)
  - [ ] analytics-service (read/write)
  - [ ] market-data service (write)
- [ ] Define connection pooling strategy
- [ ] Add read/write separation (optional)
- [ ] Add caching layer (Redis) if needed

---

## 🔄 Interactions

### 📥 Data Input
- [ ] Receive candle data from market-data service
- [ ] Store candles in `candles` table
- [ ] Store orderbook snapshots (optional)
- [ ] Store trades (optional)

### ⚙️ Processing Support
- [ ] Provide fast reads for analytics-service:
  - [ ] candles → indicators
  - [ ] indicators → signals
- [ ] Provide fast reads for API-service:
  - [ ] `/candles`
  - [ ] `/indicators`
  - [ ] `/signals`
  - [ ] `/stats`

### 📤 Data Output
- [ ] Optimize queries for frontend/API-service
- [ ] Add materialized views (optional)
- [ ] Add caching for heavy queries

---

## 🧪 Testing
- [ ] Load testing for candle inserts
- [ ] Benchmark read performance for indicators/signals
- [ ] Test migrations
- [ ] Test failover behavior in k3s StatefulSet

---

## ☸️ Deployment (k3s)
- [ ] Create StatefulSet manifest
- [ ] Create PVC templates
- [ ] Configure storage class
- [ ] Add liveness/readiness probes
- [ ] Configure backup/restore strategy
- [ ] Add monitoring (Prometheus exporter)

---

## 📚 Documentation
- [ ] Document database schema in `docs/db-schema.md`
- [ ] Document retention policies
- [ ] Document table relationships
- [ ] Add ERD diagram
