# ---------------------------------------------------------
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
#   make help               - show all available commands
#   make sync               - install/update uv environment
#   make run <service>      - run a service via uvicorn
#   make dev <service>      - run a service via fastapi dev
#   make test <service>     - run pytest for the service
#   make lint <service>     - run ruff check
#   make fmt <service>      - run ruff format
#
# Arguments:
#   <service> - directory name under ./services/
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
# ---------------------------------------------------------

help:
	@echo " --------------------------------------------------------- "
	@echo " Available commands:                                       "
	@echo "   make help               - show this help                "
	@echo "   make sync               - install/update uv environment "
	@echo "   make run <service>      - run service via uvicorn       "
	@echo "   make dev <service>      - run service via fastapi --dev "
	@echo "   make test <service>     - run pytest                    "
	@echo "   make lint <service>     - run ruff check                "
	@echo "   make fmt <service>      - run ruff format               "
	@echo " --------------------------------------------------------- "

# --- Commands --------------------------------------------
SERVICE := $(word 2, $(MAKECMDGOALS))
PACKAGE := $(subst -,_,$(SERVICE))
SRC_DIR := services/$(SERVICE)/src
APP_PATH := $(SRC_DIR)/$(PACKAGE)/main.py

sync: # install/update .venv and uv.lock
	uv sync --group dev

uvicorn: # run a service via uvicorn
	@if "$(SERVICE)"=="" ( echo Usage: make run ^<service^> & exit 1 )
	uv run uvicorn $(PACKAGE).main:app --reload --reload-dir services/$(SERVICE) --log-level debug --host 127.0.0.1 --port 8080 --app-dir $(SRC_DIR)

fastapi: # run a service via fastapi
	@if "$(SERVICE)"=="" ( echo Usage: make dev ^<service^> & exit 1 )
	uv run fastapi dev --app $(SRC_DIR)/PACAGE/main:app

test:
	@if "$(SERVICE)"=="" ( echo Usage: make test ^<service^> & exit 1 )
	uv run pytest $(SRC_DIR) -q

lint:
	@if "$(SERVICE)"=="" ( echo Usage: make lint ^<service^> & exit 1 )
	uv run ruff check $(SRC_DIR)

fmt:
	@if "$(SERVICE)"=="" ( echo Usage: make fmt ^<service^> & exit 1 )
	uv run ruff format $(SRC_DIR)
