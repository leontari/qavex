# =============================================================================
# CONFIG
# =============================================================================
PY_SERVICES = \
    services/backend-api \
    services/market-data-service \
    services/analytics-service \
    services/worker-service

FRONTEND_DIR = services/frontend

DOCKER_SERVICES = backend-api market-data-service analytics-service worker-service frontend

HELM_CHART = charts/app
K8S_NAMESPACE = app

# =============================================================================
# PYTHON: VENV + RUN
# =============================================================================
.PHONY: venv
venv:
    @for srv in $(PY_SERVICES); do \
        echo ">>> Creating venv for $$srv"; \
        python3 -m venv $$srv/.venv; \
        $$srv/.venv/bin/pip install -U pip; \
        if [ -f $$srv/requirements.txt ]; then \
            $$srv/.venv/bin/pip install -r $$srv/requirements.txt; \
        fi \
    done

.PHONY: run-backend
run-backend:
    @for srv in $(PY_SERVICES); do \
        echo ">>> Starting $$srv"; \
        cd $$srv && ../$$srv/.venv/bin/python -m uvicorn app.main:app --reload & \
    done

# =============================================================================
# FRONTEND
# =============================================================================
.PHONY: run-frontend
run-frontend:
    cd $(FRONTEND_DIR) && npm install && npm run dev

# =============================================================================
# ALL SERVICES
# =============================================================================
.PHONY: up
up: run-backend run-frontend
    @echo ">>> All services started"

.PHONY: stop
stop:
    @echo ">>> Stopping Python services"
    @pkill -f uvicorn || true
    @echo ">>> Stopping frontend dev server"
    @pkill -f "vite" || true

# =============================================================================
#   DOCKER
# =============================================================================
.PHONY: docker-build
docker-build:
    @for srv in $(DOCKER_SERVICES); do \
        echo ">>> Building $$srv"; \
        docker build -t $$srv:latest services/$$srv; \
    done

.PHONY: docker-up
docker-up:
    docker compose up -d

.PHONY: docker-down
docker-down:
    docker compose down

# =============================================================================
# TESTS
# =============================================================================
.PHONY: test
test:
    @for srv in $(PY_SERVICES); do \
        if [ -d $$srv/tests ]; then \
            echo ">>> Running tests for $$srv"; \
            $$srv/.venv/bin/pytest $$srv/tests; \
        fi \
    done

# =============================================================================
# LINT / FORMAT
# =============================================================================
.PHONY: format
format:
    @for srv in $(PY_SERVICES); do \
        if [ -d $$srv/app ]; then \
            echo ">>> Formatting $$srv"; \
            $$srv/.venv/bin/black $$srv/app; \
        fi \
    done

# =============================================================================
# KUBERNETES / HELM
# =============================================================================
.PHONY: helm-deploy
helm-deploy:
    helm upgrade --install app $(HELM_CHART) -n $(K8S_NAMESPACE) --create-namespace

.PHONY: helm-delete
helm-delete:
    helm uninstall app -n $(K8S_NAMESPACE)

# =============================================================================
# ARGO CD
# =============================================================================
.PHONY: argocd-sync
argocd-sync:
    argocd app sync app

.PHONY: argocd-status
argocd-status:
    argocd app get app
