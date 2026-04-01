<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 9149960 (feature: project structure (#1))
<<<<<<< feature/structure
analytics-service

objective:
  - count indicators
  - signals
  - patterns
  - alerts
  
interface:
  - REST/gRPC for API-service or
  - writes results in separate tables (signals, indicators)

interacts:
  - reads table candles
  - calculates indicators -> writes in table indicators
  - generates signals -> writes in table signals
=======
<<<<<<< HEAD
=======
>>>>>>> 3f129e9 (feature: project structure (#1))
=======
>>>>>>> 9149960 (feature: project structure (#1))
Analytics-service

objective:
  - connect to the data source via REST/WebSocket
  - normalise data
  - publish in a queue or database

interface:
  - gRPC/HTTP for inner services (e.g. get last N candles)
  - write directly in the database (table candles, trades)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> main
=======
>>>>>>> 3f129e9 (feature: project structure (#1))
=======
>>>>>>> main
>>>>>>> 9149960 (feature: project structure (#1))
