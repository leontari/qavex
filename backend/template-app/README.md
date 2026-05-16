# IT IS NOT a FastAPI CRUD app

Plugin Runtime Platform

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

```
RuntimeKernel
    ├── transport orchestration
    ├── module orchestration
    ├── infrastructure orchestration
    └── lifecycle orchestration
```

## Plugins / Modules:

- UserService
- AuthService
- SyncService
- ImportService
- MetricsService
- HealthService

Supports:
- sandbox modules;
- hot reload modules;
- dynamic plugins;
- remote plugins;
- signed plugins;
- multi-tenant modules.

Modules work only via public setup API:
- `register_router`
- `register_startup_hook`
- `register_shutdown_hook`
- `register_dependency`
- `get_provider`

## Infrastructure Adapters:

- Postrgres
- Kafka
- Redis
- S3
- ClickHouse
- SMTP
- REST clients

## This is the foundation for

The target to get as a result:

- plugin loading
- feature flags
- runtime capability discovery
- dynamic module enabling/disabling
- background runtime services
- event-driven orchestration
- service runtime platform

## Target system design

Hexagonal Runtime Architecture

`template-app` is a `Application Runtime Kernel`

where:

- FastAPI = transport adapter;
- lifespan = runtime adapter;
- services/modules = plugins;
- infrastructure = adapters/providers;
- runtime = orchestration layer.

This will allow the change FastApi itself:
For example:
```text
HTTP adapter
gRPC adapter
Kafka consumer runtime
CLI runtime
Worker runtime
Scheduler runtime
```
will be on the same `kernel`

## Current Architecture

Current architecture design:

```
FastAPI = transport;
providers = infrastructure adapters;
modules = business plugins;
lifecycle = orchestration engine;
kernel = runtime platform.
```

which is close to:
```text
Temporal worker runtime;
internal platform runtimes;
microservice kernels;
plugin-based enterprise systems.
```
