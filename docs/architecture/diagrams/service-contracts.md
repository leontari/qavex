# Service Contracts

```
API Gateway:
    GET /candles
    GET /indicators
    GET /signals
    GET /stats
    POST /auth/login
    POST /settings

Market Data Service:
    GET /last-candles
    GET /last-trades

Analytics Service:
    POST /recalculate
    GET /indicators
    GET /signals

Alert Service:
    POST /rules
    GET /rules
    GET /alerts

Worker Service:
    no public API (queue/cron triggered)
```
