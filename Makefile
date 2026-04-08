.PHONY: help, lock, sync, build
# =============================================================================
# Root Makefile - Developer Onboarding & Service Utilities
#
# Purpose:
#   Provides a unified developer experience for all services
#   in the monorepo. Includes commands for:
#     - Python environment management via uv
#     - Running services (uvicorn / fastapi)
#     - Testing, linting, formatting
#
# Usage:
#     - to see available commands run in terminal:
#         >>> make help
#
# Arguments:
#   <service> - directory name under ./backend/
#               e.g.: market-data, user-api, auth-service
#
# Notes:
#   - SERVICE is extracted as the 2nd Make argument:
#         $(word 2, $(MAKECMDGOALS))
#   - PACKAGE converts service name into a valid Python
#     package name by replacing '-' with '_'
#   - The pattern rule "%: @:" allows Make to accept
#     arbitrary arguments without treating them as targets.
#
# Troubleshooting (Windows / PowerShell):
#   - PowerShell does NOT support Bash syntax (pipes, $(), etc.)
#   - CMD does NOT support Bash utilities (grep, tr, cut)
#   - This Makefile avoids all shell-specific syntax so it
#     works consistently across Bash, CMD, and PowerShell.
#
# =============================================================================

help:
	@echo " ============================================================================= "
	@echo "  AVAILABLE COMMANDS:                                                          "
	@echo " ============================================================================= "
	@echo "   > make help                             show this help                      "
	@echo "                                                                               "
	@echo " --- Dev tools --------------------------------------------------------------- "
	@echo "   > make sync                             install|update global .venv uv.lock "
	@echo "   > make lock <service>                   create/update service's uv.lock     "
	@echo "                                                                               "
	@echo "   > make uvicorn <service>                run service via uvicorn             "
	@echo "   > make fastapi <service>                run service via fastapi dev         "
	@echo "   > make test <service>                   run pytest                          "
	@echo "   > make lint <service>                   run ruff check                      "
	@echo "   > make fmt <service>                    run ruff format                     "
	@echo "                                                                               "
	@echo " --- Docker ------------------------------------------------------------------ "
	@echo "   > make build <service> TAG=<tag>        build a Docker image                "
	@echo "   > make build-run <service> TAG=<tag>    build and run service containerized "
	@echo "   > make build-git <service>              build an image with git tag         "
	@echo "   > make run <service> TAG=<tag>          run service containerized           "
	@echo "   > make logs <service>                   view container logs                 "
	@echo "   > make logs <service>                   view container logs                 "
	@echo "   > make sh <service>                     view an image's contents            "
	@echo "   > make push <service> TAG=<tag>         push image to registry              "
	@echo " ============================================================================= "

# --- Commands --------------------------------------------
.DEFAULT_GOAL := help
SERVICE := $(word 2, $(MAKECMDGOALS))
PACKAGE := $(subst -,_,$(SERVICE))
SRC_DIR := backend/$(SERVICE)/src
APP_PATH := $(SRC_DIR)/$(PACKAGE)/main.py
TAG ?= latest

sync: # install/update .venv and uv.lock
	uv sync --locked --all-packages

lock: # update uv.lock
	@if "$(SERVICE)"=="" ( echo Usage: make lock   exit 1 )
	uv lock

export: # export dependencies from uv.lock to requirements.txt for a specific python package
	@if "$(SERVICE)"=="" ( echo Usage: make export ^<service^> exit 1 )
	uv export --no-hashes --format requirements.txt --package $(SERVICE) --output-file backend/$(SERVICE)/requirements.txt

uvicorn: # run a service via uvicorn
	@if "$(SERVICE)"=="" ( echo Usage: make run ^<service^> & exit 1 )
	uv run uvicorn $(PACKAGE).main:app --reload --reload-dir backend/$(SERVICE) --log-level debug --host 127.0.0.1 --port 8000 --app-dir $(SRC_DIR)

fastapi: # run a service via fastapi
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

# build docker image for a service
	# docker build -t users-service ./services/users
	# docker build --no-cache -t $(SERVICE):$(TAG) -f backend/$(SERVICE)/Dockerfile .
build:
	@if "$(SERVICE)" == "" ( echo Usage: make build ^<service^> TAG=^<tag^> & exit 1 )
	docker build -t $(SERVICE):$(TAG) -f backend/$(SERVICE)/Dockerfile .

build-run: # build an image and start it in a container
	@if "$(SERVICE)" == "" ( echo Usage: make build-run ^<service^> TAG=^<tag^> & exit 1 )
	docker build -t $(SERVICE):$(TAG) -f backend/$(SERVICE)/Dockerfile .
	docker run --rm -p 8000:8000 $(SERVICE):$(TAG)

build-git: # build  an image with git tag
	@if "$(SERVICE)" == "" ( echo Usage: make build-git ^<service^> & exit 1 )
	docker build -t $(SERVICE):$(GIT_TAG) -f backend/$(SERVICE)/Dockerfile .

run:  # run docker container for a service with auto-removal
	@if "$(SERVICE)" == "" ( echo Usage: make run ^<service^> TAG=^<tag^> & exit 1 )
	docker run --rm -p 8000:8000 $(SERVICE):$(TAG)

logs: # view logs (container must be running)
	@if "$(SERVICE)" == "" ( echo Usage: make logs ^<service^> & exit 1 )
	docker logs -f $(SERVICE)

sh: # view an image's contents
	@if "$(SERVICE)" == "" ( echo Usage: make sh ^<service^> & exit 1 )
	docker run --rm -it $(SERVICE) sh

stop:  # stop container
	@if "$(SERVICE)" == "" ( echo Usage: make stop ^<service^> & exit 1 )
	docker stop $(SERVICE)

push: # push image to registry
	@if "$(SERVICE)" == "" ( echo Usage: make push ^<service^> TAG=^<tag^> & exit 1 )
	docker push $(SERVICE):$(TAG)

%: #  Prevent "No rule to make target"
    @:

# bind:
# The --rm flag is included to ensure the container and anonymous volume are cleaned up when the container exits
# docker run --rm --volume .:/app --volume /app/.venv [...]
