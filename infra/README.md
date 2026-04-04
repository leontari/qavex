# Local Development Overview

Everything related to local development is kept inside the `infra/` directory:
- docker-compose.yml — production‑like local stack
- docker-compose.override.yml — development mode with hot reload
- Makefile — unified command interface
- Utility scripts — helpers for building images, running migrations, etc.

Keeping these files inside `infra/` helps keep the repository root clean and organized.

---

## How to Use the infra/ Environment

### 1. Local Development

Start the full local stack:

```bash
cd infra
make up
```

This launches all services using Docker Compose.

### 2. Local Kubernetes Cluster (Kind)

Create a local Kind cluster:

```bash
cd infra 
make kind-up
```

This sets up a Kubernetes environment for testing Helm charts, Traefik, and Argo CD.
