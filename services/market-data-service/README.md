Market data service

objective:
  - connect to the data source via REST/WebSocket
  - normalise data
  - publish in a queue or database

interface:
  - gRPC/HTTP for inner services (e.g. get last N candles)
  - write directly in the database (table candles, trades)
<<<<<<< feature/structure

interactions:
  - writes in
    - table candles
    - table trades
=======
>>>>>>> main
