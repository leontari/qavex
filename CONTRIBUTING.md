# Contributing

Thank you for contributing to the project!

We welcome pull requests, bug reports, feature suggestions, and documentation improvements.

This guide explains how to set up your environment, follow coding standards, and submit changes.

---
## 🧱 Code of Conduct

By participating in this project, you agree to follow the community standards described in:

[**CODE_OF_CONDUCT.md**](/CONTRIBUTING.md)

---
## 🛠 Development Environment Requirements

- [**GNU Make 4.4+**](https://www.gnu.org/software/make/) - used for automation and development workflows
- [**UV 0.11+**](https://docs.astral.sh/uv/) -  Python package and environment manager  
- [**Docker & Docker Compose**](https://www.docker.com/) - for containerized development and testing
- Node.js - managed via `nvm` (on windows)
- Kind (optional for Kubernetes testing) - for running local Kubernetes-based tests

---
## 🚀 Getting started

For detailed setup instructions and guidance on preparing your local virtual environment, refer to [onboarding.md](/docs/onboarding.md)

---
## 🛠 Contributing workflow

1. Fork the repository  
2. Clone your fork  
3. Create a feature branch  
4. Make your changes  
5. Run tests  
6. Submit a Pull Request

---
## 🧩 Development Workflow

### no Docker:

#### 1. Run all services locally
```
make run-backend
make run-frontend
```

#### 2. Run a single service (```api-gateway``` service as an example)
```
make uvicorn SERVICE=api-gateway
```

### Docker:
```
cd infra
make up
```

## 🧪 Testing

Each service contains its own test suite.

Run tests for a specific service:
```bash
make test SERVICE=analytics
```

or

```
cd services/<service> pytest
```

---

## 📦 Commit Guidelines

We follow conventional commits:
```
feat: add new indicator calculation
fix: correct RSI formula
docs: update architecture diagrams
refactor: cleanup analytics pipeline
test: add unit tests for alert rules
```

---

## 🧹 Code Quality
Pre-commit hooks enforce:
- ruff (linting)
- ruff-format / black (formatting)
- isort (imports)
- mypy (typing)
- prettier (frontend)
- kubeconform (Kubernetes manifests)
- service structure validation
- secrets scanning

Run manually:
```
make run-pre-commit
```

---
## 🔀 Pull Requests
1. Create a feature branch
2. Ensure all tests pass
3. Ensure pre-commit passes
4. Submit a PR with a clear description which:
    - is small and focused
    - includes tests (if applicable)
    - updates documentation (if needed)
    - passes CI checks
    - has a clear description of the change

---
## 🐛 Reporting Bugs

Please include:
- steps to reproduce
- expected behavior
- actual behavior
- logs or screenshots (if relevant)

Create an issue here:
https://github.com/leontari/qavex/issues

---

## 💡 Suggesting Features
Feature requests are welcome!

Please describe:
- the problem
- the proposed solution
- alternatives considered
- potential impact

---

## 🤝 Thank You
Your contributions help make this project better for everyone.
