# Qavex

This repository contains a modular microservices architecture designed for scalability, reliability, and developer productivity. 

It includes backend services, a frontend application, shared libraries, protobuf definitions, infrastructure tooling, and Kubernetes deployment configurations.

---

## 📁 Repository Structure
```
repo/
├── backend/               # Backend microservices
│   ├── api-gateway/
│   ├── market-data/
│   ├── analytics/
│   ├── alert-service/
│   ├── worker-service/
│   └── scheduler/
├── db/                    # Migrations and database schema
├── deploy/                # Helm charts, Traefik, Kubernetes configs
├── docs/                  # Arhitecture docs
├── frontend/              # SPA (Vue/Svelte)
├── infra/                 # Local development environment (Docker, Kind, Makefile)
├── scripts/               # Utility scripts for CI, automation, validation
│
├── shared-libs/           # Reusable libraries for Python and Node
└── shared-proto/          # Protobuf contracts for inter-service communication
```

---

## 🧩 Core Concepts

### **Microservices**
Each service is isolated, independently deployable, and follows a consistent structure:
- `src/` — application code  
- `Dockerfile` / `Dockerfile.dev`  
- `requirements.txt`  
- `README.md`  

### **Shared Protobuf**
`shared-proto/` contains all `.proto` files used for gRPC and event schemas.  
This ensures consistent contracts across all services.

### **Shared Libraries**
`shared-libs/` provides reusable infrastructure code:
- logging  
- configuration  
- database utilities  
- middleware  
- retry/backoff logic  

### **Infrastructure**
`infra/` contains everything for local development:
- Docker Compose  
- Kind cluster configs  
- Makefile commands  
- helper scripts  

### **Deployment**
`deploy/` contains:
- Helm charts  
- Traefik ingress  
- Argo CD GitOps configuration  

---

## 🚀 Getting Started 

### Run services locally (Docker-Compose)

```bash
cd infra
make up
````

### Run services locally (no Docker)
```bash
make run-backend
make run-frontend
````

### Run services in Kubernetes (Kind)
```
cd infra
make kind-up
```

### Run a single service

```bash
make run SERVICE=api-gateway
```

---

## 🧱 Services

| Сервис                                               | Описание                      |
|------------------------------------------------------|-------------------------------|
| [API Gateway](/backend/api-gateway/README.md)       | REST API for the frontend     |
| [Market Data](/backend/market-data/README.md)       | Market data ingestion         |
| [Analytics](/backend/analytics/README.md)           | Indicators, signals, patterns |
| [Alert Service](/backend/alert-service/README.md)   | Rules and notifications       |
| [Worker Service](/backend/worker-service/README.md) | Heavy tasks, reports          |
| [Scheduler](/backend/scheduler/README.md)           | CronJobs                      |

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
- [Code of conduct](/CODE_OF_CONDUCT.md)
- [Security policy](/SECURITY.md)

---

## 🛠 CI/CD

GitHub Actions handles:

- building & pushing images
- running pre‑commit hooks
- validating Kubernetes manifests
- triggering Argo CD sync

Configuration: `.github/workflows/*.yml`

---

## 🛠 Tooling
- **uv** for Python virtualenvs
- **nvm** for Node version management
- **pre‑commit** for formatting, linting, and validation
- **kubeconform** for Kubernetes schema validation

---

## 📄 License

[MIT](/LICENSE)
