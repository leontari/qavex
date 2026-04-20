# Market-data service responsibilities:
- Establish a stable connection to the Bybit WebSocket API
- Receive real‑time market data
- Normalize incoming data into a unified OHLCV format
- Expose normalized data through REST and WebSocket endpoints
- Maintain a minimal in‑memory cache of the latest candles
- Provide a clean, minimal, production‑ready architecture suitable for integration into a microservices environment

## Structure
```text
services/market-data/
│
├── src/
│   └── market_data/
│       │
│       ├── main.py                # entrypoint
│       │
│       ├── modules/
│       │   └── ticks/             # domain market data
│       │       ├── api.py         # REST (optional)
│       │       ├── ws.py          # WebSocket endpoint
│       │       ├── service.py     # business-logic
│       │       ├── stream.py      # Redis pub/sub logic
│       │       ├── schemas.py     # DTO
│       │       └── models.py      # (optional for storage)
│       │
│       ├── infrastructure/
│       │   └── redis/
│       │       ├── client.py      # connection
│       │       └── pubsub.py      # Redis client wrapper
│       │
│       ├── core/
│       │   ├── config.py         # settings
│       │   ├── logger.py
│       │   └── lifecycle.py      # startup/shutdown
│       │
│       └── common/
│           └── utils.py
│
├── pyproject.toml
├── Dockerfile
└── README.md
```

## Data flow

``` Redis → stream.py → service.py → ws.py → client```
