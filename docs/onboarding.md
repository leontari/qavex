# Onboarding Guide

Welcome to the project!

This guide will help you get up to speed quickly and start contributing with confidence.

---

## 1. Required Tools

Please install the following:

- Docker + Docker Compose
- Python 3.11
- Node.js 18+
- VS Code (рекомендуется)
- kubectl + k3d/k3s (for local Kubernetes development)

---

## 2. Clone the Repository

```bash
git clone https://github.com/leontari/qavex.git
```

---

## 3. Local Development Setup

### Option 1 — Docker Compose

```bash
docker-compose up --build
```

### Option 2 — Makefile

Install dependencies:

```bash
make install
````

Run a specific service:

```bash
make run SERVICE=api-gateway
```

---

## 4. Project Structure
```
services/       — backend microservices
frontend/       — SPA application
db/             — database schema & migrations
docs/           — architecture * documentation
k8s/            — Kubernetes manifests
helm/           — Helm chart
```

---

## 5. Working With Services

### Run a service

```bash
make run SERVICE=analytics
```

### Run tests

```bash
make test SERVICE=analytics
```

### Build a Docker image

```bash
make build SERVICE=analytics
```

---

## 6. CI/CD

The project uses GitHub Actions for:
- linting
- running tests
- building Docker images
- deploying to Kubernetes via `delploy.yml`
- Helm-based production deployments

Workflow files are located in ```/github/workflows/```.


---

## 7. Documentation

- Architecture: `docs/architecture/index.md`
- Diagrams: `docs/architecture/diagrams/`
- Roadmap: `docs/roadmap/full-system-roadmap.md`

---

## 8. Contact & Support

For questions, discussions, or contributions:
- Open an issue:
https://github.com/leontari/qavex/issues
- Contact the maintainer (email obfuscated for spam protection):
leontari [at] pm [dot] me

Community contributions are welcome - feel free to submit PRs, report bugs, or propose improvements.
