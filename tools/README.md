# 🛠 Tools

The tools directory contains utility scripts and helper programs used throughout the repository.
These scripts automate development, CI/CD, and maintenance workflows, ensuring consistency and reducing manual effort.

## 📂 Structure

### ci/

Scripts and utilities used exclusively by CI/CD pipelines:

- environment preparation
- validation and checks
- automated build steps
- deployment helpers

These scripts are designed to run in non‑interactive environments and must remain deterministic.

### dev/

Developer‑focused tools used during local development:

- code generation
- project scaffolding
- structure validation
- local automation tasks
- helper scripts for debugging or maintenance

These scripts improve developer productivity and streamline repetitive tasks.

## Purpose

These scripts help streamline repetitive tasks and reduce the chance of human error.  
They are used by:

- developers during local development  
- CI/CD pipelines  
- onboarding workflows  
- pre‑commit hooks (e.g., service structure validation)

## Usage

Scripts are typically invoked through the root `Makefile`.

```bash
make tree backend/template-app
```

## Make sure the scripts are executable:
```bash
chmod +x tools/ci/bash/*.sh
```

## Notes
Scripts should remain idempotent and safe to run multiple times

Avoid adding business logic here — keep scripts focused on tooling and automation
