CREATE TABLE candles (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,              -- C98USDT
    timeframe TEXT NOT NULL,           -- 1m, 5m, 1h, 1d
    ts TIMESTAMPTZ NOT NULL,           -- candle opening time
    open NUMERIC(18,8),
    high NUMERIC(18,8),
    low NUMERIC(18,8),
    close NUMERIC(18,8),
    volume NUMERIC(18,8),

    UNIQUE(symbol, timeframe, ts)
);
