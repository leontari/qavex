-- ============================================================
-- USERS & SETTINGS
-- ============================================================

CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    email           TEXT UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE settings (
    id          SERIAL PRIMARY KEY,
    user_id     INT REFERENCES users(id) ON DELETE CASCADE,
    key         TEXT NOT NULL,
    value       TEXT NOT NULL
);

CREATE TABLE watchlists (
    id          SERIAL PRIMARY KEY,
    user_id     INT REFERENCES users(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE watchlist_items (
    id              SERIAL PRIMARY KEY,
    watchlist_id    INT REFERENCES watchlists(id) ON DELETE CASCADE,
    symbol          TEXT NOT NULL
);

CREATE TABLE portfolios (
    id          SERIAL PRIMARY KEY,
    user_id     INT REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE portfolio_positions (
    id              SERIAL PRIMARY KEY,
    portfolio_id    INT REFERENCES portfolios(id) ON DELETE CASCADE,
    symbol          TEXT NOT NULL,
    amount          DOUBLE PRECISION NOT NULL,
    avg_price       DOUBLE PRECISION NOT NULL
);


-- ============================================================
-- MARKET DATA
-- ============================================================

CREATE TABLE candles (
    id          BIGSERIAL PRIMARY KEY,
    symbol      TEXT NOT NULL,
    timeframe   TEXT NOT NULL,
    ts          TIMESTAMPTZ NOT NULL,
    open        DOUBLE PRECISION NOT NULL,
    high        DOUBLE PRECISION NOT NULL,
    low         DOUBLE PRECISION NOT NULL,
    close       DOUBLE PRECISION NOT NULL,
    volume      DOUBLE PRECISION NOT NULL
);

-- TimescaleDB hypertable (optional)
-- SELECT create_hypertable('candles', 'ts');

CREATE TABLE trades (
    id          BIGSERIAL PRIMARY KEY,
    symbol      TEXT NOT NULL,
    ts          TIMESTAMPTZ NOT NULL,
    price       DOUBLE PRECISION NOT NULL,
    volume      DOUBLE PRECISION NOT NULL,
    side        TEXT CHECK (side IN ('buy', 'sell'))
);

CREATE TABLE orderbook (
    id          BIGSERIAL PRIMARY KEY,
    symbol      TEXT NOT NULL,
    ts          TIMESTAMPTZ NOT NULL,
    bids_json   JSONB NOT NULL,
    asks_json   JSONB NOT NULL,
    checksum    TEXT
);


-- ============================================================
-- ANALYTICS
-- ============================================================

CREATE TABLE indicators (
    id          BIGSERIAL PRIMARY KEY,
    symbol      TEXT NOT NULL,
    timeframe   TEXT NOT NULL,
    ts          TIMESTAMPTZ NOT NULL REFERENCES candles(ts),
    type        TEXT NOT NULL,
    value_json  JSONB NOT NULL
);

CREATE TABLE signals (
    id          BIGSERIAL PRIMARY KEY,
    symbol      TEXT NOT NULL,
    timeframe   TEXT NOT NULL,
    ts          TIMESTAMPTZ NOT NULL REFERENCES candles(ts),
    type        TEXT NOT NULL,
    strength    DOUBLE PRECISION,
    meta_json   JSONB
);

CREATE TABLE patterns (
    id              BIGSERIAL PRIMARY KEY,
    symbol          TEXT NOT NULL,
    ts_start        TIMESTAMPTZ NOT NULL,
    ts_end          TIMESTAMPTZ NOT NULL,
    pattern_type    TEXT NOT NULL,
    confidence      DOUBLE PRECISION NOT NULL
);

CREATE TABLE stats (
    id              BIGSERIAL PRIMARY KEY,
    symbol          TEXT NOT NULL,
    timeframe       TEXT NOT NULL,
    ts              TIMESTAMPTZ NOT NULL,
    metrics_json    JSONB NOT NULL
);


-- ============================================================
-- ALERT SYSTEM
-- ============================================================

CREATE TABLE alert_rules (
    id              SERIAL PRIMARY KEY,
    user_id         INT REFERENCES users(id) ON DELETE CASCADE,
    symbol          TEXT NOT NULL,
    condition_json  JSONB NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE alerts (
    id              BIGSERIAL PRIMARY KEY,
    rule_id         INT REFERENCES alert_rules(id) ON DELETE SET NULL,
    user_id         INT REFERENCES users(id) ON DELETE CASCADE,
    symbol          TEXT NOT NULL,
    ts_triggered    TIMESTAMPTZ NOT NULL,
    type            TEXT NOT NULL,
    payload_json    JSONB NOT NULL
);

CREATE TABLE alert_channels (
    id              SERIAL PRIMARY KEY,
    user_id         INT REFERENCES users(id) ON DELETE CASCADE,
    type            TEXT CHECK (type IN ('email', 'webhook', 'telegram')),
    config_json     JSONB NOT NULL
);


-- ============================================================
-- AUDIT & RETENTION
-- ============================================================

CREATE TABLE audit_logs (
    id              BIGSERIAL PRIMARY KEY,
    user_id         INT REFERENCES users(id) ON DELETE SET NULL,
    ts              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    action          TEXT NOT NULL,
    details_json    JSONB
);

CREATE TABLE retention_policies (
    id              SERIAL PRIMARY KEY,
    table_name      TEXT NOT NULL,
    keep_days       INT NOT NULL,
    last_cleanup_ts TIMESTAMPTZ
);
