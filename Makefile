.PHONY: help \
        sync lock export \
        install-pre-commit run-pre-commit \
        uvicorn fastapi test lint fmt \
        build run sh log stop \
        build-run build-git push \
        %

# =============================================================================
#    ROOT MAKEFILE: service utilities
# =============================================================================
.DEFAULT_GOAL := help

SERVICE := $(word 2, $(MAKECMDGOALS))
PACKAGE := $(subst -,_,$(SERVICE))
SRC_DIR := backend/$(SERVICE)/src
APP_PATH := $(SRC_DIR)/$(PACKAGE)/main.py
TAG ?= latest

# =============================================================================
#    HELP
# =============================================================================
help:
	@echo " ============================================================================= "
	@echo "     AVAILABLE COMMANDS:                                                       "
	@echo " ============================================================================= "
	@echo " >>> make help                            :show this help                      "
	@echo "                                                                               "
	@echo " --- Dev Tools --------------------------------------------------------------- "
	@echo " >>> make sync                            :install all deps using lockfile     "
	@echo " >>> make lock                            :discover deps and update uv.lock    "
	@echo " >>> make export <service>                :export requirements.txt             "
	@echo "                                                                               "
	@echo " >>> make install-pre-commit              :install pre-commit hooks            "
	@echo " >>> make run-pre-commit                  :run pre-commit checks               "
	@echo "                                                                               "
	@echo " >>> make uvicorn <service>               :run service locally via uvicorn     "
	@echo " >>> make fastapi <service>               :run service locally via fastapi dev "
	@echo " >>> make test <service>                  :run pytest                          "
	@echo " >>> make lint <service>                  :run ruff check                      "
	@echo " >>> make fmt <service>                   :run ruff format                     "
	@echo "                                                                               "
	@echo " --- Docker ------------------------------------------------------------------ "
	@echo " >>> make build <service> TAG=<tag>       :build a Docker image                "
	@echo " >>> make run <service> TAG=<tag>         :run service containerized           "
	@echo " >>> make sh <service>                    :view an image's contents            "
	@echo " >>> make log <service>                   :view container logs                 "
	@echo " >>> make stop <service>                  :stop image container                "
	@echo "                                                                               "
	@echo " >>> make build-run <service> TAG=<tag>   :build and run service containerized "
	@echo " >>> make build-git <service>             :build an image with git tag         "
	@echo " >>> make push <service> TAG=<tag>        :push image to registry              "
	@echo " ============================================================================= "

# =============================================================================
#    DEV COMMANDS
# =============================================================================
sync:
	uv sync --locked --all-packages

lock:
	uv lock

export:
	@if "$(SERVICE)"=="" ( echo Usage: make export ^<service^> exit 1 )
	uv export --no-hashes --format requirements.txt --package $(SERVICE) --output-file backend/$(SERVICE)/requirements.txt

# -----------------------------------------------------------------------------
install-pre-commit:
	@echo "Installing pre-commit globally on the system..."
	uv tool install pre-commit --with pre-commit-uv --force-reinstall
	@echo "Installing hooks for the current repo..."
	uv run pre-commit install
	@echo "pre-commit hooks installed successfully."

run-pre-commit:
	echo "Running pre-commit checks..."
	uv run pre-commit run --all-files

# -----------------------------------------------------------------------------
uvicorn:
	@if "$(SERVICE)"=="" ( echo Usage: make run ^<service^> & exit 1 )
	uv run uvicorn $(PACKAGE).main:app --reload --reload-dir backend/$(SERVICE) --log-level debug --host 127.0.0.1 --port 8000 --app-dir $(SRC_DIR)

fastapi:
	@if "$(SERVICE)"=="" ( echo Usage: make fastapi ^<service-name^> & exit 1 )
	uv run fastapi dev --reload-dir backend/$(SERVICE) backend/$(SERVICE)/src/$(PACKAGE)/main.py

test:
	@if "$(SERVICE)"=="" ( echo Usage: make test ^<service^> & exit 1 )
	uv run pytest $(SRC_DIR) -q

lint:
	@if "$(SERVICE)"=="" ( echo Usage: make lint ^<service^> & exit 1 )
	uv run ruff check $(SRC_DIR)

fmt:
	@if "$(SERVICE)"=="" ( echo Usage: make fmt ^<service^> & exit 1 )
	uv run ruff format $(SRC_DIR)

# =============================================================================
#    DOCKER COMMANDS
# =============================================================================
build:
	@if "$(SERVICE)" == "" ( echo Usage: make build ^<service^> TAG=^<tag^> & exit 1 )
	docker build -t $(SERVICE):$(TAG) -f backend/$(SERVICE)/Dockerfile .

run:
	@if "$(SERVICE)" == "" ( echo Usage: make run ^<service^> TAG=^<tag^> & exit 1 )
	docker run --rm -p 8000:8000 $(SERVICE):$(TAG)

sh:
	@if "$(SERVICE)" == "" ( echo Usage: make sh ^<service^> & exit 1 )
	docker run --rm -it $(SERVICE) sh

log:
	@if "$(SERVICE)" == "" ( echo Usage: make logs ^<service^> & exit 1 )
	docker logs -f $(SERVICE)

stop:  # stop container
	@if "$(SERVICE)" == "" ( echo Usage: make stop ^<service^> & exit 1 )
	docker stop $(SERVICE)

# -----------------------------------------------------------------------------
build-run:
	@if "$(SERVICE)" == "" ( echo Usage: make build-run ^<service^> TAG=^<tag^> & exit 1 )
	docker build -t $(SERVICE):$(TAG) -f backend/$(SERVICE)/Dockerfile .
	docker run --rm -p 8000:8000 $(SERVICE):$(TAG)

build-git:
	@if "$(SERVICE)" == "" ( echo Usage: make build-git ^<service^> & exit 1 )
	docker build -t $(SERVICE):$(GIT_TAG) -f backend/$(SERVICE)/Dockerfile .

push:
	@if "$(SERVICE)" == "" ( echo Usage: make push ^<service^> TAG=^<tag^> & exit 1 )
	docker push $(SERVICE):$(TAG)

# -----------------------------------------------------------------------------
%:
	@:
