# IT IS NOT a FastAPI CRUD app

It is an other architecture level which can be described as:

- microservice runtime platform;
- extensible service host;
- plugin-oriented service architecture;
- orchestration layer around FastAPI instance

## Architecture model
```text
FastAPI = transport/runtime kernel

services/* = plugins/modules/business capabilities

infrastructure/* = adapters/external integrations

bootstrap/* = composition root + orchestration

domain/* = business contracts and abstractions
```

## Core adea

FastAPI - is NOT an application

FastAPI  is used here as:
- transport host;
- DI entrypoint;
- HTTP runtime;
- middleware pipeline;
- lifecycle runtime.

The application itself is represented by the `template_app`'s:
- modules;
- services;
- plugins.

Services (or business-logic in other words) is represented by plugins here.

## What it looks like

Runtime Kernel:

- FastApi
- Lifecycle
- DI Container
- Observability
- Configuration
- Event Bus
- Task Scheduler

Plugins / Modules:

- UserService
- AuthService
- SyncService
- ImportService
- MetricsService
- HealthService

Infrastructure Adapters:

- Postrgres
- Kafka
- Redis
- S3
- ClickHouse
- SMTP
- REST clients
