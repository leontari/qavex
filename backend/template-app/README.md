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

```text
RuntimeKernel
    ├── transport orchestration
    ├── module orchestration
    ├── infrastructure orchestration
    └── lifecycle orchestration
```

```text
RuntimeKernel
    ├── lifecycle
    ├── modules
    ├── DI container
    └── infrastructure providers
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

modules/
```text
registry     -> runtime module graph
manifest     -> static metadata
discovery    -> enable/disable/filtering
loader       -> runtime activation
context      -> restricted runtime API
```

which is base for:

- event-driven microservices;
- microservice kernel;
- plugin-based systems;
- orchestration runtime.

As for now has been implemented:

- Runtime kernel
- Plugin modules
- Lifecycle orchestration
- Infrastructure registry
- Dependency container
- Provider abstraction
- Restricted module API
- Runtime/application separation

### Application package responsibility separation:
FastAPI is used more like a transport plugin above the application runtime kernel now.

| Layer          | 	Responsibility             |
|----------------|-----------------------------|
| kernel         | 	runtime orchestration      |
| lifecycle      | 	startup/shutdown execution |
| modules        | 	business plugins           |
| infrastructure | 	external systems adapters  |
| api            | 	transport layer            |
| domain         | 	business contracts         |
| services       | 	application capabilities   |
| contracts      | system component protocols  |
| runtime        | runtime kernel              |

## Event Bus

Target:
- `inter-module communication` without `direct coupling`

like:

- `UserModule -> EventBus -> NotificatioonModule`

and NOT:
- `UserModule -> NotificationService`

### Event Bus responsibilities

| Responsibility	         | Description            |
|-------------------------|------------------------|
| publish events	         | runtime event emission |
| subscribe handlers      | 	event routing         |
| decouple modules	plugin | isolation              |
| async orchestration	    | async execution        |
| domain event transport  | 	business messaging    |
| infrastructure bridge	  | Kafka/NATS later       |

### Event system architecture

```text
bootstrap/
├── events/
│   ├── __init__.py
│   ├── bus.py
│   ├── protocols.py
│   ├── registry.py
│   ├── dispatcher.py
│   ├── handlers.py
│   ├── event.py
│   └── exceptions.py
```

### System Graph
```text
Module A
    │
    ▼
publish(event)
    │
    ▼
┌──────────────────┐
│    EventBus      │
├──────────────────┤
│ registry         │
│ dispatcher       │
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│ Event Handlers   │
└─────────┬────────┘
          │
 ┌────────┴────────┐
 ▼                 ▼
Module B       Module C
```

## Current architecture layers

### Kernel Layer
- RuntimeKernel
- ApplicationContext
- RuntimeState
- Container

### Lifecycle Layer
- startup/shutdown hooks
- registry
- manager

### Messaging Layer
- EventBus
- CommandBus
- QueryBus
- HandlerRegistry

### Module Layer
- ModuleProtocol
- ModuleLoader
- ModuleRegistry
- ModuleSetupContext

### Infrastructure Layer
- providers
- registry
- lifecycle integration
