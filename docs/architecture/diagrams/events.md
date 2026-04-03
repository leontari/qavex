# Event-Driven Architecture (ASCII)
```
External Market Data
        │
        ▼
 (market_data_event)
        │
        ▼
 Market Data Service
        │
        ├── emits normalized_candle → Queue: candles
        └── emits normalized_trade  → Queue: trades


Analytics Service
        ▲
        │ consumes candles/trades
        │
        ├── emits indicator_event → Queue: indicators
        └── emits signal_event    → Queue: signals


Alert Service
        ▲
        │ consumes indicators/signals
        │
        ├── emits alert_triggered → Queue: alerts
        └── sends notifications → Email/Webhook/Telegram


CronJobs → Worker Service → cleanup_event → Queue: maintenance
```
