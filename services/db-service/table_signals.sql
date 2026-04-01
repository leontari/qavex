CREATE TABLE signals (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,

    signal_type TEXT NOT NULL,         -- "rsi_overbought", "ema_cross", "pattern_123"
    direction TEXT NOT NULL,           -- buy / sell / neutral
    strength NUMERIC(5,2),             -- 0–100
    metadata JSONB,                    -- любые доп. данные

    UNIQUE(symbol, timeframe, ts, signal_type)
);
