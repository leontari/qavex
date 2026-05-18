# System Composition Graph

```text
                         ┌──────────────────────┐
                         │    template_app      │
                         │    __init__.py       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       asgi.py        │
                         │ bootstrap_application│
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌────────────────────────────────┐
                    │ RuntimeKernel                  │
                    │--------------------------------│
                    │ - startup()                    │
                    │ - shutdown()                   │
                    │ - context                      │
                    │ - module_registry              │
                    └──────────────┬─────────────────┘
                                   │
             ┌─────────────────────┼─────────────────────┬─────────────────────────────────────┐
             ▼                     ▼                     ▼                                     ▼
┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐            ┌─────────────────────────┐
│ ApplicationContext │  │   RuntimeState     │  │   ModuleRegistry   │            │ InfrastructureRegistry  │
├────────────────────┤  ├────────────────────┤  ├────────────────────┤            └────────────┬────────────┘
│ app: FastAPI       │  │ container          │  │ modules            │                         │
│ runtime            │  │ lifecycle_registry │  └────────────────────┘    ┌────────────────────┼─────────────────┐
└─────────┬──────────┘  │ infrastructure_reg │                            ▼                    ▼                 ▼
          │             │ lifecycle_manager  │                      ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
          │             └─────────┬──────────┘                      │ CacheProvider  │ │ DatabaseProv.  │ │ QueueProvider  │
          │                       │                                 └──────┬─────────┘ └───────┬────────┘ └──────┬─────────┘
          ▼                       ▼                                        │                   │                 │
┌────────────────────┐  ┌────────────────────┐                             ▼                   ▼                 ▼
│      FastAPI       │  │ LifecycleManager   │                      ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ transport adapter  │  │ executes hooks     │                      │ CacheProvider  │ │ DatabaseProv.  │ │ QueueProvider  │
└────────────────────┘  └─────────┬──────────┘                      └──────┬─────────┘ └──────┬─────────┘ └──────┬─────────┘
                                  │                                        │                  │                  │
                    ┌─────────────┼─────────────┐                          ▼                  ▼                  ▼
                    ▼                           ▼                   ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
         ┌────────────────────┐     ┌────────────────────┐          │ CacheClient    │ │ SQLAlchemy     │ │ Kafka/RabbitMQ │
         │ startup hooks      │     │ shutdown hooks     │          └────────────────┘ └────────────────┘ └────────────────┘
         └────────────────────┘     └────────────────────┘
```

## Module (Plugin) Architecture

```text
                  ┌────────────────────┐
                  │   Business Module  │
                  └─────────┬──────────┘
                            │
                            ▼
               ┌─────────────────────────┐
               │ ModuleSetupContext      │
               ├─────────────────────────┤
               │ register_router()       │
               │ register_dependency()   │
               │ register_startup_hook() │
               │ register_shutdown_hook()│
               │ get_provider()          │
               └────────────┬────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ Runtime Kernel │ │ Infrastructure │ │ Lifecycle      │
│ Container      │ │ Providers      │ │ Registry       │
└────────────────┘ └────────────────┘ └────────────────┘
```

## System Initialization Flow

```text
1.  template_app:app import
              │
              ▼
2.         asgi.py
    bootstrap_application()
              │
              ▼
3. create lifecycle registry
              │
              ▼
4. create infrastructure registry
              │
              ▼
5.     create container
              │
              ▼
6.   create runtime state
              │
              ▼
7. create application context
              │
              ▼
8.   create RuntimeKernel
              │
              ▼
9.  create FastAPI transport
              │
              ▼
10. attach transport into context
              │
              ▼
11.      load modules
              │
              ▼
12.   modules register:
        - routes
        - hooks
        - dependencies
              │
              ▼
13. infrastructure providers register hooks
              │
              ▼
14.   application ready
```

## Module Development Guide
## 1. What is a module

#### A module is:

- Business capability plugin.

#### Examples:

- users
- auth
- trading
- analytics
- notifications
- ingestion
- pipelines

#### Modules MUST NOT:

- create DB engines
- create Redis clients
- create Kafka producers
- initialize infrastructure directly

#### Infrastructure belongs to infrastructure layer.

### 2. Module contract

#### Required interface
```text
class ModuleProtocol(Protocol):

    def setup(
        self,
        context: ModuleSetupContext,
    ) -> None:
        ...
```

### 3. What modules can do

#### Modules MAY:

| Capability                      | 	Allowed |
|---------------------------------|----------|
| register routes                 | 	✅       |
| register lifecycle hooks        | 	✅       |
| register runtime dependencies   | 	✅       |
| access infrastructure providers | 	✅       |
| create business services        | 	✅       |

### 4. What modules MUST NOT do

| Forbidden                          | 	Reason                   |
|------------------------------------|---------------------------|
| create Redis client directly	      | infrastructure leak       |
| create DB engine directly	         | lifecycle violation       |
| mutate kernel	                     | runtime corruption        |
| mutate lifecycle manager internals | 	orchestration corruption |
| access FastAPI                     | state	transport leakage   |

### 5. Module dependency access

#### Modules access dependencies via:

```text
context.get_provider("cache")`
```

#### Example:

```text
cache = context.get_provider("cache")
client = cache.client
```

### 6. Dependency registration

#### Modules may expose business services:

```text
context.register_dependency(
    UserServiceProvider(),
)
```

#### Later:
```text
service = container.resolve("user_service")
```

### 7. Route registration

```text
router = APIRouter()

@router.get("/users")
async def users():
    return []

context.register_router(router)
```

### 8. Lifecycle registration

```text
context.register_startup_hook(
    LifecycleHook(
        name="users.startup",
        handler=self.startup,
    )
)
```

### 9. Full example module

```text
from __future__ import annotations

from fastapi import APIRouter

from template_app.bootstrap.lifecycle.hooks import (
    LifecycleHook,
)


class UserModule:

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.started = False

    def setup(self, context) -> None:

        cache_provider = context.get_provider("cache")

        router = APIRouter(
            prefix="/users",
            tags=["users"],
        )

        @router.get("/")
        async def users() -> list[dict]:
            return []

        context.register_router(router)

        context.register_startup_hook(
            LifecycleHook(
                name="users.startup",
                handler=self.startup,
            )
        )

        context.register_shutdown_hook(
            LifecycleHook(
                name="users.shutdown",
                handler=self.shutdown,
            )
        )
```

### 10. Architectural Philosophy

Architecture is:

- Kernel-driven
- modular
- plugin-based
- runtime system
- with transport adapters
- with infrastructure adapters.

NOT:

FastAPI monolith.

### Final Layering

```text
        domain
          ↑
   services/modules
          ↑
kernel/runtime/lifecycle
          ↑
     transport/api
          ↑
    infrastructure
```

### Most Important Concept

#### FastAPI is:

- ONLY HTTP TRANSPORT PLUGIN

#### NOT:

- application center
