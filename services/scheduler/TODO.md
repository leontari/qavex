# TODO — Scheduler / Cron System

## 🎯 Objectives
- [ ] Trigger periodic tasks across services
- [ ] Manage cron-based workflows
- [ ] Provide reliable scheduling in k8s

---

## 🔌 Interface
- [ ] Use Kubernetes CronJobs
- [ ] Trigger worker-service tasks
- [ ] Trigger analytics-service recalculations
- [ ] Trigger cleanup/maintenance tasks

---

## 🔄 Scheduled Tasks

### 📊 Analytics
- [ ] Recalculate daily indicators
- [ ] Rebuild aggregated stats
- [ ] Generate daily/weekly reports

### 🧹 Maintenance
- [ ] Cleanup old logs
- [ ] Cleanup old alerts
- [ ] Cleanup old candles (if retention enabled)

### 🔔 Alerts
- [ ] Periodic alert rule evaluation (if not event-driven)

---

## 🧪 Testing
- [ ] Validate CronJob schedules
- [ ] Test idempotency of scheduled tasks
- [ ] Test failure recovery
- [ ] Test logging and monitoring

---

## 📚 Documentation
- [ ] Create `docs/scheduler.md`
- [ ] Document all CronJobs and their schedules
