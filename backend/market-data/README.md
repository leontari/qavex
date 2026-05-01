# Market-data service responsibilities:
- Establish a stable connection to the Bybit WebSocket API
- Receive real‑time market data
- Normalize incoming data into a unified OHLCV format
- Expose normalized data through REST and WebSocket endpoints
- Maintain a minimal in‑memory cache of the latest candles
- Provide a clean, minimal, production‑ready architecture suitable for integration into a microservices environment
