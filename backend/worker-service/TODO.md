# TODO — Worker Service (Optional)

## 🎯 Objectives
- [ ] Execute heavy or long‑running tasks
- [ ] Run backend test jobs
- [ ] Generate reports
- [ ] Perform periodic or scheduled calculations

---

## 🔌 Interface
- [ ] Trigger tasks via message queue:
  - [ ] RabbitMQ
  - [ ] Kafka
  - [ ] Redis Streams
- [ ] Support Kubernetes CronJobs as an alternative trigger
- [ ] Define task payload formats
- [ ] Add logging and error reporting for each task

---

## 🔄 Task Types

### 🧪 Backend Tests
- [ ] Implement job runner for backend test suites
- [ ] Add reporting of test results
- [ ] Add notifications on failures (optional)

### 📊 Reports
- [ ] Generate periodic analytics reports
- [ ] Export results to database or storage
- [ ] Provide summary data for API-service (optional)

### ⏱️ Periodic Calculations
- [ ] Run scheduled recalculations (e.g., daily indicators)
- [ ] Trigger analytics-service tasks if needed
- [ ] Write results back to database

---

## 🧪 Testing
- [ ] Test queue consumers
- [ ] Test CronJob execution flow
- [ ] Test long-running task stability
- [ ] Test retry/backoff logic

---

## ☸️ Deployment (optional)
- [ ] Add Deployment manifest for worker pods
- [ ] Add CronJob manifests for scheduled tasks
- [ ] Configure resource limits for heavy workloads
- [ ] Add monitoring (Prometheus metrics)
- [ ] Add centralized logging

---

## 📚 Documentation
- [ ] Create `docs/worker-service.md`
- [ ] Document supported task types
- [ ] Document queue message formats
- [ ] Document CronJob schedules
