# System Architecture Overview

This document provides a high-level overview of the entire system, including all services, their responsibilities, interactions, and data flow.  
Each service has its own dedicated README.md, TODO.md and the architecture diagram file, but this index serves as the central reference point.

# 🧩 System Components

## 1. Frontend (Vue or Svelte + Lightweight Charts)

**Responsibilities:**
- UI rendering
- Charting (candles, indicators, signals)
- Routing
- Authorization
- User settings

**Interactions:**
- Communicates only with `backend-api` via REST

## 2. API Gateway / Backend API (FastAPI)

**Responsibilities:**
- Authentication / authorization
- REST API for frontend
- Aggregates data from internal services
- Reads from database/cache

**Interactions:**
- Reads from DB (`candles`, `indicators`, `signals`)
- Calls analytics-service and market-data service via HTTP/gRPC

## 3. Market Data Service

**Responsibilities:**
- Connect to external REST/WebSocket sources
- Normalize incoming data
- Publish to queue or write directly to DB

**Interactions:**
- Writes to `candles` and `trades` tables
- Provides internal API for last N candles/trades

## 4. Analytics Service

**Responsibilities:**
- Calculate indicators
- Generate signals
- Detect patterns
- Produce alerts (optional)

**Interactions:**
- Reads `candles`
- Writes `indicators` and `signals`
- Provides REST/gRPC for API-service

## 5. Alert Service

**Responsibilities:**
- Evaluate alert rules
- Trigger alerts based on indicators/signals
- Send notifications (email/webhook/Telegram)

**Interactions:**
- Reads indicators/signals
- Writes to `alerts` table
- Sends notifications externally

## 6. Worker Service (Optional)

**Responsibilities:**
- Heavy tasks (tests, reports, periodic calculations)
- Triggered by queue or CronJob

**Interactions:**
- Writes results to DB
- Triggers analytics or alert tasks

## 7. Scheduler / Cron System

**Responsibilities:**
- Periodic tasks (daily indicators, cleanup, reports)
- Managed via Kubernetes CronJobs

**Interactions:**
- Triggers worker-service or analytics-service

## 8. DB Service (Postgres / Timescale / ClickHouse)

**Responsibilities:**
- Store candles, trades, indicators, signals, alerts
- Store users and settings
- Provide fast reads for analytics and API-service

**Interactions:**
- Written by market-data, analytics, alert, worker services
- Read by API-service and analytics-service

# 🔗 Data Flow Overview

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

## Shared components:

- shared-proto  →  protobuf contracts for all services
- shared-libs   →  common infrastructure code (logging, config, db, utils)

## Deployment flow:

- deploy/helm → Argo CD → Kubernetes cluster → Traefik ingress

## 📦 Services

- [Frontend](/ui/README.md)
- [Database](/db/README.md)
- [API Gateway](/backend/api-gateway/README.md)
- [Market Data Service](/backend/market-data/README.md)
- [Analytics Service](/backend/analytics/README.md)
- [Alert Service](/backend/alert-service/README.md)
- [Worker Service](/backend/worker-service/README.md)
- [Scheduler](/backend/scheduler/README.md)

## 📚 Diagrams

- [Alert Flow](diagrams/alert-flow.md)
- [Entity Relationship Diagram (ERD)](diagrams/erd.md)
- [DFD](diagrams/dfd.md)
- [Scheduler Flow](diagrams/scheduler-flow.md)
- [Sequence Diagrams](diagrams/sequence-diagrams.md)
- [System Data Flow Overview](diagrams/system-data-flow-overview.md)

## 🗺 Roadmap

- [Full System Roadmap](/docs/roadmap/full-system-roadmap.md)

## 🧱 Core Architecture Principles

- Microservice structure
- Event‑Driven communication
- Clear domain separation
- Kubernetes-oriented infrastructure
- Monorepo for development convenience
