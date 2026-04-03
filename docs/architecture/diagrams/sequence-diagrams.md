# Sequence Diagrams
```
============================================================
1. User opens chart
============================================================

Frontend → API: GET /candles
API → DB: SELECT candles
DB → API: candles[]
API → Frontend: candles[]

Frontend → API: GET /indicators
API → DB: SELECT indicators
DB → API: indicators[]
API → Frontend: indicators[]

Frontend → API: GET /signals
API → DB: SELECT signals
DB → API: signals[]
API → Frontend: signals[]


============================================================
2. Market data arrives → analytics → alerts
============================================================

Exchange → MarketData: tick
MarketData → DB: INSERT candle/trade
MarketData → Analytics: new candle event

Analytics → DB: SELECT recent candles
Analytics → DB: INSERT indicators
Analytics → DB: INSERT signals

Analytics → AlertService: signal_event
AlertService → DB: SELECT alert_rules
AlertService → DB: INSERT alert
AlertService → Notification: send alert


============================================================
3. Cron → Worker → Analytics
============================================================

Cron → Worker: trigger job
Worker → Analytics: run daily indicators
Analytics → DB: SELECT candles
Analytics → DB: INSERT indicators/stats
Worker → DB: INSERT reports
```
