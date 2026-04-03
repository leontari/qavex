# TODO — Frontend (Vue or Svelte + Lightweight Charts)

## 🎯 Objectives
- [ ] Implement core UI
- [ ] Add charting functionality (Lightweight Charts)
- [ ] Set up routing (pages, layouts)
- [ ] Implement authorization / authentication
- [ ] Add user settings (theme, chart config, etc.)

---

## 🔌 Interface
- [ ] Interact only with `backend-api`
- [ ] Create API client module
- [ ] Add request/response validation
- [ ] Handle loading/error states for all API calls

---

## 🧱 Layers

### 📊 Charts (Lightweight Charts → candles)
- [ ] Create chart component wrapper
- [ ] Fetch candles from `/candles`
- [ ] Render candlestick series
- [ ] Add chart resize handling
- [ ] Add timeframe switching (1m, 5m, 1h, 1d)

### 📈 Overlays → indicators
- [ ] Fetch indicators from `/indicators`
- [ ] Render overlays:
  - [ ] EMA/SMA
  - [ ] RSI (separate panel)
  - [ ] MACD (separate panel)
- [ ] Add toggle controls for indicators

### 📍 Markers → signals
- [ ] Fetch signals from `/signals`
- [ ] Render markers on chart (buy/sell)
- [ ] Add signal filtering (type, strength)
- [ ] Add tooltips for markers

---

## 🧭 Routing
- [ ] Set up router (SvelteKit or Vue Router)
- [ ] Pages:
  - [ ] `/` — main chart
  - [ ] `/settings`
  - [ ] `/login`
  - [ ] `/stats` (optional)
- [ ] Add protected routes (auth required)

---

## 🔐 Authorization
- [ ] Login page
- [ ] Token storage (localStorage or cookies)
- [ ] Auto-refresh tokens (if supported by backend)
- [ ] Add global auth guard
- [ ] Add logout flow

---

## ⚙️ Settings
- [ ] Theme (light/dark)
- [ ] Chart appearance settings
- [ ] Default symbol/timeframe
- [ ] Save settings to backend or local storage

---

## 🧪 Testing
- [ ] Component tests (UI)
- [ ] Chart rendering tests
- [ ] API integration tests
- [ ] Routing tests
- [ ] Auth flow tests

---

## 📚 Documentation
- [ ] Create `docs/frontend.md`
- [ ] Document chart architecture
- [ ] Document API usage
- [ ] Add screenshots or diagrams (optional)
