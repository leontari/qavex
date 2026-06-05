from template_app.runtime.container.types import DependencyVisibility

# Runtime DI Container

Lightweight typed dependency injection container used by the Kernel runtime.

## Features

* Typed dependency resolution
* Singleton / Transient / Scoped lifetimes
* Async providers
* Namespace isolation
* Visibility rules
* Dependency graph export
* Runtime diagnostics

# Basic Usage

## Register singleton

```python
manager.register(
    Database,
    SingletonProvider(lambda di: PostgresDatabase()),
    namespace=Namespace("infrastructure"),
    visibility=DependencyVisibility.PUBLIC,
)
```

Resolve:

```python
db = manager.resolve(
    Database,
    owner=Namespace("infrastructure"),
    requester=Namespace("kernel"),
)
```

## Register factory

### Transient dependency

```python
container.register(
    RequestId,
    FactoryProvider(lambda di: RequestId(),),
    namespace=Namespace("kernel"),
    visibility=DependencyVisibility.PUBLIC,
)
```

Every resolve creates a new instance:

```python
id1 = manager.resolve(RequestId)
id2 = manager.resolve(RequestId)

assert id1 != id2
```

## Scoped dependency

```python
scope = ScopeContext()

service = manager.resolve(
    UserService,
    owner=Namespace("plugin.auth"),
    requester=Namespace("plugin.auth"),
    scope=scope,
)
```

Scoped instances live only inside the provided scope.

Typical use cases:

- HTTP request
- Kafka message
- gRPC call
- GUI window
- background job

## Async dependency

```python
manager.register(
    KafkaClient,
    AsyncProvider(create_client,
    namespace=Namespace("transport"),
    visibility=DependencyVisibility.PUBLIC,
)
```

Resolve:

```python
client = await manager.resolve_async(KafkaClient)
```

# Namespaces

Dependencies belong to namespaces.

```python
Namespace("kernel")
Namespace.("plugin.auth")
Namespace.TRANSPORT
Namespace.INFRASTRUCTURE
Namespace.GUI
Namespace.TESTING
```

Namespaces isolate plugins and runtime subsystems.

Example:

```python
container.register(
    AuthService,
    provider,
    namespace=Namespace.PLUGIN,
)
```

## Visibility

```python
Visibility.PUBLIC
Visibility.PRIVATE
Visibility.KERNEL
```

### PUBLIC:

```text
Accessible from all namespaces (from everywhere).
```

### PRIVATE:

```text
Accessible only inside owner namespace.
```

Example:

```text
plugin.auth
    ↓
UserRepository
```
Only `plugin.auth` can resolve it.

### KERNEL:

```text
Accessible only from Kernel.
```

Useful for internal runtime services.


# Plugin Isolation

Auth plugin:

```python
container.register(
    UserRepository,
    provider,
    namespace=Namespace.AUTH,
    visibility=Visibility.PRIVATE,
)
```

Allowed:

```python
container.resolve(
    UserRepository,
    requester=Namespace.AUTH,
)
```

Denied:

```python
container.resolve(
    UserRepository,
    requester=Namespace.BILLING,
)
```

Raises:

```python
PermissionError
```

---

# Diagnostics

Snapshot:

```python
snapshot = manager.snapshot()
```

Export JSON:

```python
export_json(snapshot)
```

GraphViz:

```python
export_graph(snapshot)
```

Human dump:

```python
export_dump(snapshot)
```

# Kernel Integration

The Container is not the application graph.

```text
Kernel
 ├─ DependencyManager
 ├─ Module Registry
 ├─ Infrastructure Registry
 ├─ Lifecycle Manager
 └─ Transport Manager
```

Kernel remains the root composition graph.

The container manages only:

- dependency registration
- dependency resolution
- lifetimes
- visibility
- namespaces

# Typical Architecture

```text
kernel
│
├── infrastructure
│   ├── Database
│   ├── Cache
│   └── Queue
│
├── transport
│   ├── HTTP
│   ├── Kafka
│   └── gRPC
│
└── plugins
    ├── Auth
    ├── Billing
    └── Notifications
```

Each plugin owns its dependencies and decides which ones are exposed.

# Recommended Rules

1. Register by type, never by string.
2. Use PUBLIC only when really needed.
3. Prefer PRIVATE inside plugins.
4. Use SINGLETON for infrastructure.
5. Use SCOPED for request/job state.
6. Keep Kernel as the composition root.
7. Plugins communicate through contracts, not implementations.
