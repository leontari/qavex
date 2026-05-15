# 🧪 Test Suite for Template App
This directory contains the complete automated test suite for the Template App project.
The tests are organized by level (unit, integration, e2e) and by domain (users, auth, observability, etc.).
The goal is to keep tests fast, isolated, predictable, and easy to navigate.

## 📁 Directory Structure
```text
tests/
├── conftest.py
│
├── unit/
│   ├── services/
│   │   ├── test_user_service.py
│   │   └── test_auth_service.py
│   ├── repositories/
│   │   └── test_user_repository.py
│   ├── models/
│   │   └── test_user_models.py
│   └── utils/
│       └── test_password_hashing.py
│
├── integration/
│   ├── api/
│   │   ├── test_users_api.py
│   │   ├── test_auth_api.py
│   │   ├── test_health_api.py
│   │   └── test_metrics_api.py
│   ├── db/
│   │   └── test_migrations.py
│   └── test_app_startup.py
│
└── e2e/
    └── test_full_flow.py

```

Each folder has a clear purpose and mirrors the architecture of the application.

## 🧩 Test Levels

### 1. Unit Tests (tests/unit/)

Unit tests validate pure business logic without external dependencies.

They do not use:

- FastAPI
- HTTP
- the real database
- dependency injection

Examples:

- `test_user_service.py`
- `test_auth_service.py`
- `test_user_repository.py`

### 2. Integration Tests (tests/integration/)

Integration tests validate how components work together:

- FastAPI routing
- dependency injection
- async SQLAlchemy
- test SQLite database
- HTTP requests via AsyncClient

Examples:

- test_users_api.py
- test_auth_api.py
- test_health_api.py

### 3. End‑to‑End Tests (tests/e2e/)

E2E tests simulate real user flows across the entire system.

Example:

- test_full_flow.py

## ⚙️ Test Environment (conftest.py)

The shared conftest.py provides:

- an in‑memory SQLite database
- an async SQLAlchemy session
- FastAPI app created via `create_app()`
- dependency overrides for:
  - `get_session`
  - `get_user_repository`
  - `get_user_service`
  - an `AsyncClient` for HTTP tests

This ensures:

- isolation between tests
- no external services required
- deterministic behavior
- compatibility with CI/CD

## ▶️ Running Tests
Run all tests:
```
pytest -q
```
Run only unit tests:

```
pytest tests/unit
```
Run only integration tests:

```
pytest tests/integration
```
Run only e2e tests:
```
pytest tests/e2e
```

## 📊 Coverage
To run tests with coverage:

```
pytest --cov=template_app --cov-report=term-missing
```

## 🧱 Adding Tests for a New Feature

Suppose you add a new domain called orders.
You should create:
```
tests/unit/services/test_orders_service.py
tests/unit/repositories/test_orders_repository.py
tests/integration/api/test_orders_api.py
tests/e2e/test_orders_flow.py
```

This keeps the test suite consistent and predictable.

## 🧼 Principles

- No duplicated tests
- No real database connections
- No real external services
- Clear separation of test levels
- Tests mirror the application architecture
- Tests must be deterministic and isolated
