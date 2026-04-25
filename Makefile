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
.PHONY: help
help:
	@echo " ============================================================================= "
	@echo "     AVAILABLE COMMANDS:                                                       "
	@echo " ============================================================================= "
	@echo " >>> make help                            :show this help                      "
	@echo "                                                                               "
	@echo " --- Dev Tools --------------------------------------------------------------- "
	@echo " >>> make sync                            :install all deps using lockfile     "
	@echo " >>> make lock                            :discover deps and update uv.lock    "
	@echo " >>> make export-deps <service>           :export requirements.txt             "
	@echo "                                                                               "
	@echo " >>> make install-git-hooks               :install 'pre-commit' scripts        "
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
.PHONY: sync
sync:
	uv sync --locked --all-packages

.PHONY: lock
lock:
	uv lock

.PHONY: export-deps
export-deps:
	@if "$(SERVICE)"=="" ( echo Usage: make export-deps ^<service^> exit 1 )
	uv export --no-hashes --format requirements.txt --package $(SERVICE) --output-file backend/$(SERVICE)/requirements.txt

# -----------------------------------------------------------------------------
.PHONY: install-git-hooks
install-git-hooks:
	uv run pre-commit install

.PHONY: run-pre-commit
run-pre-commit:
	uv run pre-commit run --all-files

# -----------------------------------------------------------------------------
.PHONY: uvicorn
uvicorn:
	@if "$(SERVICE)"=="" ( echo Usage: make uvicorn ^<service^> & exit 1 )
	uv run uvicorn $(PACKAGE).main:app --reload --reload-dir backend/$(SERVICE) --log-level debug --host 127.0.0.1 --port 8000 --app-dir $(SRC_DIR)

.PHONY: fastapi
fastapi:
	@if "$(SERVICE)"=="" ( echo Usage: make fastapi ^<service-name^> & exit 1 )
	uv run fastapi dev --reload-dir backend/$(SERVICE) backend/$(SERVICE)/src/$(PACKAGE)/main.py

.PHONY: test
test:
	@if "$(SERVICE)"=="" ( echo Usage: make test ^<service^> & exit 1 )
	uv run pytest $(SRC_DIR) -q

.PHONY: lint
lint:
	@if "$(SERVICE)"=="" ( echo Usage: make lint ^<service^> & exit 1 )
	uv run ruff check $(SRC_DIR)

.PHONY: fmt
fmt:
	@if "$(SERVICE)"=="" ( echo Usage: make fmt ^<service^> & exit 1 )
	uv run ruff format $(SRC_DIR)

# =============================================================================
#    DOCKER COMMANDS
# =============================================================================
.PHONY: build
build:
	@if "$(SERVICE)" == "" ( echo Usage: make build ^<service^> TAG=^<tag^> & exit 1 )
	docker build -t $(SERVICE):$(TAG) -f backend/$(SERVICE)/Dockerfile .

.PHONY: run
run:
	@if "$(SERVICE)" == "" ( echo Usage: make run ^<service^> TAG=^<tag^> & exit 1 )
	docker run --rm -p 8000:8000 $(SERVICE):$(TAG)

.PHONY: sh
sh:
	@if "$(SERVICE)" == "" ( echo Usage: make sh ^<service^> & exit 1 )
	docker run --rm -it $(SERVICE) sh

.PHONY: log
log:
	@if "$(SERVICE)" == "" ( echo Usage: make logs ^<service^> & exit 1 )
	docker logs -f $(SERVICE)

.PHONY: stop
stop:
	@if "$(SERVICE)" == "" ( echo Usage: make stop ^<service^> & exit 1 )
	docker stop $(SERVICE)

# -----------------------------------------------------------------------------
.PHONY: build-run
build-run:
	@if "$(SERVICE)" == "" ( echo Usage: make build-run ^<service^> TAG=^<tag^> & exit 1 )
	docker build -t $(SERVICE):$(TAG) -f backend/$(SERVICE)/Dockerfile .
	docker run --rm -p 8000:8000 $(SERVICE):$(TAG)

.PHONY: build-git
build-git:
	@if "$(SERVICE)" == "" ( echo Usage: make build-git ^<service^> & exit 1 )
	docker build -t $(SERVICE):$(GIT_TAG) -f backend/$(SERVICE)/Dockerfile .

.PHONY: push
push:
	@if "$(SERVICE)" == "" ( echo Usage: make push ^<service^> TAG=^<tag^> & exit 1 )
	docker push $(SERVICE):$(TAG)
