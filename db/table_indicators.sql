CREATE TABLE indicators (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,

    name TEXT NOT NULL,                -- rsi, ema20, macd
    value NUMERIC(18,8) NOT NULL,

    UNIQUE(symbol, timeframe, ts, name)
);
