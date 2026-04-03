```
# Entity Relationship Diagram (ERD)

============================================================
                        USERS & SETTINGS
============================================================

 users
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ email                    │
 │ password_hash            │
 │ created_at               │
 └───────────────┬──────────┘
                 │ 1:N
 settings        ▼
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ user_id (FK → users.id)  │
 │ key                      │
 │ value                    │
 └──────────────────────────┘


 watchlists
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ user_id (FK)             │
 │ name                     │
 │ created_at               │
 └───────────────┬──────────┘
                 │ 1:N
 watchlist_items ▼
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ watchlist_id (FK)        │
 │ symbol                   │
 └──────────────────────────┘


 portfolios
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ user_id (FK)             │
 │ created_at               │
 └───────────────┬──────────┘
                 │ 1:N
 portfolio_pos   ▼
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ portfolio_id (FK)        │
 │ symbol                   │
 │ amount                   │
 │ avg_price                │
 └──────────────────────────┘


============================================================
                        MARKET DATA
============================================================

 candles
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ symbol                   │
 │ timeframe                │
 │ ts                       │
 │ open, high, low, close   │
 │ volume                   │
 └──────────────────────────┘

 trades
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ symbol                   │
 │ ts                       │
 │ price                    │
 │ volume                   │
 │ side                     │
 └──────────────────────────┘

 orderbook
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ symbol                   │
 │ ts                       │
 │ bids_json                │
 │ asks_json                │
 │ checksum                 │
 └──────────────────────────┘


============================================================
                        ANALYTICS
============================================================

 indicators
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ symbol                   │
 │ timeframe                │
 │ ts (FK → candles.ts)     │
 │ type                     │
 │ value_json               │
 └──────────────────────────┘

 signals
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ symbol                   │
 │ timeframe                │
 │ ts (FK → candles.ts)     │
 │ type                     │
 │ strength                 │
 │ meta_json                │
 └──────────────────────────┘

 patterns
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ symbol                   │
 │ ts_start                 │
 │ ts_end                   │
 │ pattern_type             │
 │ confidence               │
 └──────────────────────────┘

 stats
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ symbol                   │
 │ timeframe                │
 │ ts                       │
 │ metrics_json             │
 └──────────────────────────┘


============================================================
                        ALERT SYSTEM
============================================================

 alert_rules
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ user_id (FK)             │
 │ symbol                   │
 │ condition_json           │
 │ created_at               │
 └───────────────┬──────────┘
                 │ 1:N
 alerts          ▼
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ rule_id (FK)             │
 │ user_id (FK)             │
 │ symbol                   │
 │ ts_triggered             │
 │ type                     │
 │ payload_json             │
 └──────────────────────────┘

 alert_channels
 ┌───────────────────────────────┐
 │ id (PK)                       │
 │ user_id (FK)                  │
 │ type (email/webhook/telegram) │
 │ config_json                   │
 └───────────────────────────────┘


============================================================
                        AUDIT & RETENTION
============================================================

 audit_logs
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ user_id (FK)             │
 │ ts                       │
 │ action                   │
 │ details_json             │
 └──────────────────────────┘

 retention_policies
 ┌──────────────────────────┐
 │ id (PK)                  │
 │ table_name               │
 │ keep_days                │
 │ last_cleanup_ts          │
 └──────────────────────────┘
```
