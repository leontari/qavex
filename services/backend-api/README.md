<<<<<<< feature/structure
api-gateway / backend-api (FastAPI)

objective:
  - authorisation/authentication (if in need)
  - REST API for the fronend:
    - /candles, /orderbook, /signals, /stats, etc. 
  
interface:
  - reads from database/cache
  - can go to market-data/analytics via inner HTTP/gRPC

interactions:
  - returns to the frontend:
    - /candles?symbol=C98USDT&tf=1h
    - /indicators?symbol=C98USDT
    - /signals?symbol=C98USDT
=======
Analytics-service

objective:
  - count indicators
  - signals
  - patterns
  - alerts
  
interface:
  - REST/gRPC for API-service or
  - writes results in separate tables (signals, indicators)
>>>>>>> main
