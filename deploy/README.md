# 📦 Deployment & Kubernetes Infrastructure

This directory contains everything required to deploy the platform and manage its Kubernetes environment.

It is intentionally separated from application code to keep the repository clean, modular, and easy to maintain.

## What’s Included

- Helm charts — templated Kubernetes manifests for all services
- Traefik ingress configuration — routing, entrypoints, and public exposure
- Kind/Minikube cluster configs — reproducible local Kubernetes environments

## Why This Structure Works

Keeping deployment assets isolated from the application codebase provides several advantages:

- **Clear separation of concerns** — developers can work on services without touching deployment logic
- **Effortless CI/CD integration** — pipelines can target this directory directly
- **Simplified code reviews** — infrastructure changes are easy to track and evaluate independently
