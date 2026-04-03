# Data Flow Diagram
```
Frontend ──REST──▶ API Gateway
                     │
                     ├──▶ DB (read candles/indicators/signals)
                     │
                     ├──gRPC/HTTP──▶ Analytics Service
                     │
                     └──gRPC/HTTP──▶ Market Data Service

External Market Data ──WS/REST──▶ Market Data Service
Market Data Service ──writes──▶ DB (candles, trades)
Market Data Service ──provides──▶ API (last N candles)

Analytics Service ──reads──▶ DB (candles)
Analytics Service ──writes──▶ DB (indicators, signals)

Analytics Service ──events──▶ Alert Service
Alert Service ──reads──▶ DB (rules)
Alert Service ──writes──▶ DB (alerts)
Alert Service ──notifies──▶ Notification Channels

CronJobs ──triggers──▶ Worker Service
Worker Service ──periodic tasks──▶ Analytics
Worker Service ──cleanup/reports──▶ DB
```
