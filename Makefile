# ---------------------------------------------------------
# Developer Onboarding Makefile (root)
# Adds:
# - automatic .env generation
# - service health checks
# - Python virtualenv management via uv
# - Node version enforcement via nvm
# ---------------------------------------------------------

INFRA := infra
SERVICES_DIR := services
FRONTEND_DIR := frontend

PY_SERVICES := api-gateway market-data analytics alert-service worker-service scheduler

# ---------------------------------------------------------
# Local Development (Docker)
# ---------------------------------------------------------

up:
    @$(MAKE) -C $(INFRA) up

down:
    @$(MAKE) -C $(INFRA) down

logs:
    @$(MAKE) -C $(INFRA) logs

restart:
    @$(MAKE) -C $(INFRA) restart

# ---------------------------------------------------------
# Local Kubernetes (Kind)
# ---------------------------------------------------------

kind-up:
    @$(MAKE) -C $(INFRA) kind-up

kind-down:
    @$(MAKE) -C $(INFRA) kind-down

# ---------------------------------------------------------
# Helm Deployment
# ---------------------------------------------------------

helm-deploy:
    @$(MAKE) -C $(INFRA) helm-deploy

helm-delete:
    @$(MAKE) -C $(INFRA) helm-delete

# ---------------------------------------------------------
# Argo CD Bootstrap
# ---------------------------------------------------------

argo-bootstrap:
    @$(MAKE) -C $(INFRA) argo-bootstrap

# ---------------------------------------------------------
# Automatic .env generation
# ---------------------------------------------------------

generate-env:
    @echo "Generating .env files for all services..."
    @for svc in $(PY_SERVICES); do \
        ENV_FILE="$(SERVICES_DIR)/$$svc/.env"; \
        if [ ! -f $$ENV_FILE ]; then \
            echo "→ Creating $$ENV_FILE"; \
            echo "ENV=dev" > $$ENV_FILE; \
            echo "DATABASE_URL=postgres://app:app@localhost:5432/appdb" >> $$ENV_FILE; \
            echo "PORT=8000" >> $$ENV_FILE; \
        else \
            echo "→ $$ENV_FILE already exists"; \
        fi \
    done
    @echo "→ Creating frontend .env"
    @if [ ! -f $(FRONTEND_DIR)/.env ]; then \
        echo "VITE_API_URL=http://localhost:8000" > $(FRONTEND_DIR)/.env; \
    fi
    @echo ".env generation complete."

# ---------------------------------------------------------
# Dependency Installation
# ---------------------------------------------------------

install-backend:
    @echo "Installing backend dependencies via uv..."
    @for svc in $(PY_SERVICES); do \
        if [ -f $(SERVICES_DIR)/$$svc/requirements.txt ]; then \
            echo "→ Installing for $$svc"; \
            cd $(SERVICES_DIR)/$$svc && uv venv && uv pip install -r requirements.txt; \
        fi \
    done
    @echo "Backend dependencies installed."

install-frontend:
    @echo "Ensuring correct Node version via nvm..."
    @cd $(FRONTEND_DIR) && nvm install && nvm use
    @echo "Installing frontend dependencies..."
    cd $(FRONTEND_DIR) && npm install
    @echo "Frontend dependencies installed."

install-all: generate-env install-backend install-frontend
    @echo "All dependencies installed."

# ---------------------------------------------------------
# Run Services Locally (NO DOCKER)
# ---------------------------------------------------------

run-backend:
    @echo "Starting all backend services locally..."
    @for svc in $(PY_SERVICES); do \
        echo "→ Starting $$svc"; \
        ( cd $(SERVICES_DIR)/$$svc && uv run python -m src.main ) & \
    done
    @echo "Backend services started."

run:
    @if [ -z "$(service)" ]; then \
        echo "Usage: make run service=<name>"; \
        echo "Available services: $(PY_SERVICES)"; \
        exit 1; \
    fi
    @echo "Running service: $(service)"
    @cd $(SERVICES_DIR)/$(service) && uv run python -m src.main

run-frontend:
    cd $(FRONTEND_DIR) && npm run dev

# ---------------------------------------------------------
# Health Checks
# ---------------------------------------------------------

health:
    @echo "Checking service health..."
    @for svc in $(PY_SERVICES); do \
        URL="http://localhost:8000/health"; \
        echo "→ Checking $$svc at $$URL"; \
        curl -s $$URL || echo "Service $$svc is not responding"; \
    done
    @echo "Health check complete."

# ---------------------------------------------------------
# Pre-commit Hooks
# ---------------------------------------------------------

pre-commit-install:
    @echo "Installing pre-commit hooks..."
    uv tool install pre-commit
    pre-commit install
    @echo "Pre-commit hooks installed."

pre-commit-run:
    @echo "Running pre-commit on all files..."
    pre-commit run --all-files

pre-commit-update:
    @echo "Updating pre-commit hooks..."
    pre-commit autoupdate


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

help:
    @echo ""
    @echo "Developer Onboarding Commands:"
    @echo ""
    @echo "  make install-all         - Install ALL dependencies"
    @echo "  make generate-env        - Generate .env files"
    @echo ""
    @echo "  make run-backend         - Run ALL backend services locally"
    @echo "  make run service=name    - Run ONE backend service locally"
    @echo "  make run-frontend        - Run frontend locally"
    @echo ""
    @echo "  make up                  - Start Docker local stack"
    @echo "  make down                - Stop Docker stack"
    @echo "  make logs                - View logs"
    @echo "  make restart             - Restart Docker stack"
    @echo ""
    @echo "  make kind-up             - Create Kind cluster"
    @echo "  make kind-down           - Delete Kind cluster"
    @echo ""
    @echo "  make helm-deploy         - Deploy via Helm"
    @echo "  make helm-delete         - Remove Helm release"
    @echo ""
    @echo "  make argo-bootstrap      - Bootstrap Argo CD app-of-apps"
    @echo ""
    @echo "  make health              - Check service health"
    @echo ""
    @echo "This Makefile is for onboarding convenience."
    @echo "All infra logic lives in infra/Makefile."
    @echo ""
