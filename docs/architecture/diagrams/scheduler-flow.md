# ⏱️ Scheduler Flow
CronJob → Worker-Service → DB / Analytics / Reports
```
┌──────────────┐
│   CronJob    │
└───────┬──────┘
        ▼
┌──────────────┐
│ Worker Tasks │
└───────┬──────┘
        ▼
┌──────────────┐
│   Database   │
└──────────────┘
```
