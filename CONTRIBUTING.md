# Contributing to Qavex

Thank you for your interest in contributing!  

We welcome pull requests, bug reports, feature suggestions, and documentation improvements.

This document explains how to work with the repository and how to submit high‑quality contributions.

---

## 🧱 Code of Conduct

By participating in this project, you agree to follow the community standards described in:

[**CODE_OF_CONDUCT.md**](/CONTRIBUTING.md)

---

## 🛠 Development Setup

1. Fork the repository  
2. Clone your fork  
3. Create a feature branch  
4. Make your changes  
5. Run tests  
6. Submit a Pull Request

---

## 🚀 Running the project locally

### Using Docker Compose

```bash
docker-compose up --build
```

### Using Makefile
```bash
make install
```
```bash
make run SERVICE=api-gateway
```

---

## 🧪 Tests

Each service contains its own test suite.

Run tests for a specific service:
```bash
make test SERVICE=analytics
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

## 🔀 Pull Requests
A good PR:
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
