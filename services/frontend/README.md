<<<<<<< feature/structure
frontend (Vue or Svelte + lightweight-charts)

objective:
  - UI
  - charts
  - routing
  - authorisation
  - settings
  
interface:
  - interacts only with ```backend-api```

layers:
 - lightweght-charts -> candles
 - overlays -> indicators
 - markers -> signals
=======
api-gateway / backend-api (FastAPI)

objective:
  - authorisation/authentication (if in need)
  - REST API for the fronend:
    - /candles, /orderbook, /signals, /stats, etc. 
  
interface:
  - reads from database/cache
  - can go to market-data/analytics via inner HTTP/gRPC
>>>>>>> main
