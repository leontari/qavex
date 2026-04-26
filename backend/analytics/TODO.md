# TODO — Analytics Service

## 🎯 Objectives

- [ ] Calculate technical indicators
- [ ] Generate trading signals
- [ ] Detect patterns
- [ ] Produce alerts (optional or future feature)

## 🔌 Interface

- [ ] Provide REST or gRPC interface for API-service  
  **or**
- [ ] Write results directly into database tables:
  - [ ] `indicators`
  - [ ] `signals`
- [ ] Define data schemas for indicators and signals
- [ ] Add validation for input parameters (symbol, timeframe, etc.)

## 🔄 Interactions

### 📥 Data Input

- [ ] Read candle data from `candles` table
- [ ] Add caching layer (optional)
- [ ] Add batching or streaming support (optional)

### ⚙️ Processing

- [ ] Implement indicator calculations:
  - [ ] RSI
  - [ ] MACD
  - [ ] EMA/SMA
  - [ ] ATR
  - [ ] Additional indicators as needed
- [ ] Write calculated indicators into `indicators` table
- [ ] Implement signal generation logic
- [ ] Write generated signals into `signals` table
- [ ] Implement pattern detection (optional)
- [ ] Implement alert generation (optional)

### 📤 Output

- [ ] Expose results via REST/gRPC (if not writing directly to DB)
- [ ] Add error handling and logging
- [ ] Ensure idempotency for repeated calculations

## 🧪 Testing

- [ ] Unit tests for each indicator
- [ ] Unit tests for signal generation logic
- [ ] Integration tests with database
- [ ] Integration tests with API-service (REST/gRPC)
- [ ] Validate indicator values against known reference data

## 📚 Documentation

- [ ] Create `docs/architecture/analytics-service.md`
- [ ] Document indicator formulas and calculation rules
- [ ] Document signal generation logic
- [ ] Add examples of input/output data
