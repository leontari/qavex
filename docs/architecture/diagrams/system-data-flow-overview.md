## System Overview

```
                ┌──────────────────────┐
                │      Frontend        │
                │  (Vue/Svelte + LWC)  │
                └──────────┬───────────┘
                           │ REST
                           ▼
                ┌──────────────────────┐
                │     API Gateway      │
                │       FastAPI        │
                └───────┬─────┬────────┘
                        │     │
        gRPC/HTTP       │     │ DB Reads
                        │     ▼
                ┌──────────────────────┐
                │   Analytics Service  │
                └───────┬──────────────┘
                        │
                        │ DB Writes
                        ▼
                ┌──────────────────────┐
                │     DB Service       │
                │ Postgres/Timescale   │
                └───────┬─────┬────────┘
                        │     │
                        │     │
                        │     │
        WebSocket/REST  │     │
                        ▼     │
                ┌──────────────────────┐
                │  Market Data Service │
                └──────────────────────┘
```
