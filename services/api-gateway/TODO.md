# TODO — API Gateway / Backend API (FastAPI)

## 🎯 Objectives
- [ ] Implement authorization / authentication (if required)
- [ ] Build REST API for the frontend:
  - [ ] `/candles`
  - [ ] `/orderbook`
  - [ ] `/signals`
  - [ ] `/stats`
  - [ ] additional endpoints as needed

---

## 🔌 Interface
- [ ] Read data from database / cache
- [ ] Implement communication with internal services:
  - [ ] market-data (HTTP/gRPC)
  - [ ] analytics-service (HTTP/gRPC)
- [ ] Define and document JSON response schemas
- [ ] Add request validation (Pydantic)

---

## 🔄 Interactions

### 📥 Data Retrieval
- [ ] Implement endpoint `/candles?symbol=C98USDT&tf=1h`
  - [ ] Read from `candles` table
  - [ ] Validate `symbol` and `tf` parameters
- [ ] Implement endpoint `/indicators?symbol=C98USDT`
  - [ ] Read from `indicators` table
- [ ] Implement endpoint `/signals?symbol=C98USDT`
  - [ ] Read from `signals` table

### 📤 Response Handling
- [ ] Format responses as clean JSON
- [ ] Add error handling (400, 404, 500)
- [ ] Add logging for requests and errors
- [ ] Add caching layer (optional)

---

## 🧪 Testing
- [ ] Write unit tests for core endpoints
- [ ] Write integration tests for interactions with market-data / analytics services
- [ ] Validate responses using real dataset samples

---

## 📚 Documentation
- [ ] Add OpenAPI/Swagger documentation
- [ ] Create `docs/api-gateway.md` with endpoint descriptions
- [ ] Add request/response examples
