api-gateway / backend-api (FastAPI)

objective:
  - authorisation/authentication (if in need)
  - REST API for the frontend:
    - /candles, /orderbook, /signals, /stats, etc. 
  
interface:
  - reads from database/cache
  - can go to market-data/analytics via inner HTTP/gRPC

interactions:
  - returns to the frontend:
    - /candles?symbol=C98USDT&tf=1h
    - /indicators?symbol=C98USDT
    - /signals?symbol=C98USDT
