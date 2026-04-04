# Shared Protobuf Definitions

This directory contains all `.proto` files used across the platform.  
It serves as the **single source of truth** for inter-service communication, ensuring consistency and compatibility between microservices.

---

## Why This Exists

Microservices often exchange structured data. To avoid duplication and mismatched models, all message schemas and service definitions are stored here and generated automatically for each language.

Benefits:

- **Consistent contracts** across all services  
- **Automatic code generation** for Python, TypeScript, Go, etc.  
- **Reduced duplication** and fewer integration bugs  
- **Clear versioning** of API and event schemas  

---

## Structure

```
shared-proto/
├── market_data.proto
├── analytics.proto
├── alerts.proto
└── common/
    ├── timestamp.proto
    └── uuid.proto
```

---

## Code Generation

Code generation is typically handled via `protoc` or language‑specific plugins.

Example:

```bash
protoc --python_out=./generated python market_data.proto
```

Or via Makefile:

```bash
make generate-proto
```

---

## Guidelines

- Do not duplicate message definitions across files
- Use common/ for shared types
- Keep backward compatibility in mind when modifying schemas
- Always regenerate code after updating .proto files
