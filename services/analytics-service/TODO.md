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
