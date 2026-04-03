# Scripts

This directory contains utility scripts used across the repository.  
They automate common development, build, and maintenance tasks to ensure a consistent workflow for all developers.

## Contents

- **build-images.sh** — builds Docker images for all backend services  
- **push-images.sh** — pushes images to the configured container registry  
- **migrate-db.sh** — applies database migrations to the local or remote environment  
- **check_service_structure.py** — validates that every microservice follows the required folder structure  

## Purpose

These scripts help streamline repetitive tasks and reduce the chance of human error.  
They are used by:

- developers during local development  
- CI/CD pipelines  
- onboarding workflows  
- pre‑commit hooks (e.g., service structure validation)

## Usage

Scripts are typically invoked through the root `Makefile`, but can also be run directly:

```bash
./scripts/build-images.sh
```

## Make sure the scripts are executable:
```bash
chmod +x scripts/*.sh
```

## Notes
Scripts should remain idempotent and safe to run multiple times

Avoid adding business logic here — keep scripts focused on tooling and automation
