# Qavex

This repository contains the full set of microservices, frontend, database and documentation for a analytics platform.

---

## 📦 Repo structure
```
repo/
├── services/              # Backend microservices
│   ├── api-gateway/
│   ├── market-data/
│   ├── analytics/
│   ├── alert-service/
│   ├── worker-service/
│   └── scheduler/
│
├── frontend/              # SPA (Vue/Svelte)
│
├── db/                    # Migrations and database schema
│
└── docs/                  # Arhitecture adn docs
```


---

## 🚀 Quick Start

### 1. Install dependencies

```bash
make install
```

### 2. Run everything locally

```bash
docker-compose up --build
```

### 3. Run a single service

```bash
make run SERVICE=api-gateway
```

---

## 🧱 Services

| Сервис                                               | Описание                      |
|------------------------------------------------------|-------------------------------|
| [API Gateway](/services/api-gateway/README.md)       | REST API for the frontend     |
| [Market Data](/services/market-data/README.md)       | Market data ingestion         |
| [Analytics](/services/analytics/README.md)           | Indicators, signals, patterns |
| [Alert Service](/services/alert-service/README.md)   | Rules and notifications       |
| [Worker Service](/services/worker-service/README.md) | Heavy tasks, reports          |
| [Scheduler](/services/scheduler/README.md)           | CronJobs                      |

---

## 📚 Documentations

- [Architecture](/docs/architecture/index.md)
- [Roadmap](/docs/roadmap/full-system-roadmap.md)
- [ERD](/docs/architecture/diagrams/erd.md)
- [DFD](/docs/architecture/diagrams/dfd.md)
- [Sequence Diagrams](/docs/architecture/diagrams/sequence-diagrams.md)

---

## 📦 Contributing
- [Onboarding guide](/docs/onboarding.md)
- [Contribution guide](/CONTRIBUTING.md)
- [Security policy](/SECURITY.md)

---

## 🛠 CI/CD

The project uses GitHub Actions:

- linting
- tests
- Docker image builds
- deployment в k8s

Configuration: `.github/workflows/*.yml`

---

## 📄 License

[MIT](/LICENSE)
