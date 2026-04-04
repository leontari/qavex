# Shared Libraries

This directory contains reusable libraries and utilities shared across multiple services.  

These modules provide common infrastructure functionality and help maintain consistency throughout the codebase.

---

## Purpose

`shared-libs` exists to avoid duplication and ensure that all services follow the same standards for:

- logging  
- configuration  
- database access  
- middleware  
- retry/backoff logic  
- metrics  
- common exceptions  
- utility helpers  

This is **not** the place for business logic — only infrastructure-level components belong here.

---

## Structure

```
shared-libs/
├── python/
│     ├── logging/
│     ├── config/
│     ├── db/
│     ├── middleware/
│     └── utils/
├── node/
│     ├── logger/
│     └── utils/
```

---

## Installation

### Python (via uv)

```bash
cd shared-libs/python
uv pip install -e .
```

### Node (via npm)
```bash
cd shared-libs/node
npm install
```

---

## Guidelines

- Keep modules small, focused, and framework‑agnostic
- Avoid circular dependencies between shared modules
- Do not include service‑specific logic
- Version shared libraries if used across multiple repositories
- Document breaking changes clearly

## When to Add Something Here

Add code to shared-libs when:
- multiple services need the same functionality
- the logic is infrastructure‑related
- the code is stable and unlikely to change per service

Do **not** add code here if:
- it is business logic
- it depends heavily on a specific service’s domain
- it is experimental or unstable
