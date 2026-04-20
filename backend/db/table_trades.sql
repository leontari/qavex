CREATE TABLE trades (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    price NUMERIC(18,8),
    volume NUMERIC(18,8)
);
