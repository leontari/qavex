# Qavex Runtime Architecture v2

## Overview

Qavex Runtime is a transport-agnostic micro-runtime inspired by operating system architecture principles.

The runtime is designed as a reusable orchestration kernel for microservices, distributed workers, APIs, event-driven systems and hybrid runtimes.

Core principles:

* transport agnostic
* runtime-centric orchestration
* immutable kernel boundary
* explicit ownership
* modular runtime domains
* infrastructure isolation
* lifecycle-driven startup/shutdown
* capability-based module access
* Kubernetes-friendly runtime model
* test-first architecture

---

# Runtime Architecture

## Runtime Topology

```text
RuntimeKernel
    ↓
KernelContext (immutable boundary)
    ↓
RuntimeState (mutable runtime graph)
    ↓
runtime domains
    ├── lifecycle
    ├── infrastructure
    ├── messaging
    ├── modules
    └── transports
```

---

# Architectural Principles

## 1. Runtime Owns Everything

The runtime kernel is the single owner of:

* lifecycle
* transports
* messaging
* infrastructure
* module registry
* startup/shutdown orchestration

Nothing bypasses the runtime.

---

## 2. Transports Are Adapters

HTTP, Kafka, gRPC and CLI are NOT application owners.

They are only runtime adapters.

Example:

```text
WRONG:
FastAPI app owns runtime

CORRECT:
Runtime owns FastAPI transport
```

---

## 3. KernelContext Is Immutable

```python
RuntimeKernel
    -> KernelContext
        -> RuntimeState
```

Tests and transports should prefer the immutable kernel facade instead of mutating runtime internals directly.

---

## 4. Runtime Domains Are Independent

Each runtime domain has isolated responsibilities.

Example:

| Domain         | Responsibility             |
| -------------- | -------------------------- |
| lifecycle      | startup/shutdown/readiness |
| infrastructure | providers/resources        |
| messaging      | buses/handlers             |
| transports     | transport orchestration    |
| modules        | module ownership           |

---

## 5. Modules Never Access Runtime Directly

Modules receive restricted APIs:

```python
ModuleRuntimeAPI
ModuleInfraAPI
ModuleMessagingAPI
```

Modules never receive RuntimeState.

---

# Runtime Lifecycle

## Startup Order

```text
1. lifecycle startup hooks
2. readiness validation
3. transport startup
```

---

## Shutdown Order

```text
1. transports shutdown
2. lifecycle shutdown hooks
```

---

# Readiness System

Readiness is transport-agnostic.

```text
ReadinessGate
    ↓
TransportGate
    ↓
transport startup
```

This enables:

* Kubernetes readiness probes
* delayed transport startup
* distributed coordination
* startup barriers
* rolling deployments

---

# Testing Architecture v2

## Philosophy

Tests validate runtime contracts instead of implementation details.

The runtime is tested like a distributed operating system kernel.

---

# Test Layout

```text
tests/
├── plugins/
├── support/
│   ├── fakes/
│   ├── fixtures/
│   ├── harness/
│   └── testing/
├── unit/
├── integration/
├── contract/
├── e2e/
└── smoke/
```

---

# Test Levels

## unit/

Pure isolated component tests.

No orchestration.

Examples:

* registries
* providers
* validators
* descriptors
* graph utilities

---

## integration/

Runtime orchestration tests.

Examples:

* startup/shutdown
* lifecycle execution
* transport coordination
* runtime composition

---

## contract/

Architecture guarantees.

These tests protect invariants.

Examples:

* transport isolation
* module restrictions
* runtime ownership boundaries
* immutable interfaces

---

## smoke/

Import safety and entrypoints.

Examples:

* package import
* ASGI import
* CLI import
* uvicorn bootstrap

---

## e2e/

Full runtime execution.

Examples:

* HTTP runtime
* Kafka runtime
* gRPC runtime

---

# Golden Test Harness

## KernelTestHarness

Single runtime-aware testing entrypoint.

```python
KernelTestHarness
```

Responsibilities:

* runtime bootstrap
* transport installation
* startup/shutdown
* runtime orchestration
* transport lookup
* fake injection

---

# IMPORTANT

Tests MUST NOT bootstrap kernels manually.

WRONG:

```python
kernel = bootstrap_kernel()
```

CORRECT:

```python
def test_runtime(kernel):
    ...
```

or

```python
def test_runtime(kernel_harness):
    ...
```

---

# Fixture Architecture v2

## Runtime-Aware Fixtures

Fixtures expose runtime domains explicitly.

Examples:

```python
kernel
runtime
lifecycle
messaging
infrastructure
transports
modules
```

---

# Fixture Rules

## GOOD

```python
def test_transport_manager(
    transport_manager,
):
    ...
```

---

## BAD

```python
def test_transport_manager():
    kernel = bootstrap_kernel()
```

---

# Plugin System

Pytest plugins provide:

* markers
* runtime fixtures
* transport fixtures
* messaging fixtures
* lifecycle fixtures
* module fixtures

---

# Example Plugin Registration

```python
pytest_plugins = [
    "tests.plugins.kernel",
    "tests.plugins.runtime",
    "tests.plugins.transports",
    "tests.plugins.modules",
]
```

---

# Runtime Fixture Hierarchy

```text
kernel_harness
    ↓
kernel
    ↓
runtime
    ↓
runtime domains
```

---

# Transport Testing

## Transport Fixtures

Transports are injected dynamically.

Example:

```python
def test_http_transport(
    http_transport,
    transport_manager,
):
    assert http_transport in transport_manager.transports
```

---

# Runtime Domain Testing

Each runtime domain is tested independently.

Example:

```text
runtime.lifecycle
runtime.messaging
runtime.infrastructure
runtime.modules
runtime.transports
```

This prevents monolithic integration coupling.

---

# Fakes

Reusable runtime-safe fakes live in:

```text
tests/support/fakes/
```

Examples:

* FakeTransport
* FakeProvider
* FakeCommandBus
* FakeEventBus

---

# DO NOT MOCK RUNTIME DOMAINS

Prefer runtime-aware fakes.

WRONG:

```python
Mock()
```

CORRECT:

```python
FakeTransport()
```

---

# Architecture Contracts

Contract tests protect architectural invariants.

Examples:

## transport isolation

```text
transport must not own runtime
```

## module isolation

```text
module must not access RuntimeState
```

## immutable kernel boundary

```text
KernelContext must remain immutable
```

---

# Entry Points

Supported runtime entrypoints:

```text
template_app:app
template_app.cli
template_app.http_
template_app.grpc
template_app.kafka
```

All entrypoints MUST remain lightweight and import-safe.

---

# Runtime Capability System

Runtime capabilities are transport-derived.

Example:

```python
runtime.capabilities.http
runtime.capabilities.kafka
```

Capabilities are computed from installed transports.

---

# Runtime Descriptor System

Runtime descriptors provide runtime diagnostics.

Example:

```python
runtime.descriptor.transports
runtime.descriptor.modules
runtime.descriptor.startup_hooks
```

---

# Future Goals

## Planned Features

* distributed runtime graph
* hot transport reload
* runtime snapshots
* runtime freeze enforcement
* async provider supervision
* distributed readiness barriers
* cluster runtime coordination
* runtime telemetry
* service mesh integration

---

# Development Rules

## NEVER

* bootstrap runtime manually in tests
* leak RuntimeState into modules
* bind runtime to FastAPI
* bind runtime to transport implementation
* access infrastructure globally

---

## ALWAYS

* use fixtures
* use runtime-aware harnesses
* keep transports isolated
* test contracts
* preserve ownership boundaries

---

# MENTAL MODEL

Think about Qavex as:

```text
Linux kernel
    +
transport adapters
    +
distributed orchestration runtime
```

NOT as:

```text
FastAPI application framework
```

The runtime is the product.

Transports are plugins.

```text
SPEC        = "what system MUST be or runtime MUST behave like X, or what system promises to give"
UNIT        = "how components behave or component behaves correctly, or how system works"
INTEGRATION = "how graph is assembled or graph wiring works, or how everything is wired"
E2E         = "how system is used or how user starts the system"
SMOKE       = "does it start"
SUPPORT     = "test helper tools to build reality"
```

```text
tests/
├── support/          # ONLY runtime builders (single source)
├── unit/             # isolated logic
├── spec/        # runtime guarantees
├── integration/      # full graph
├── e2e/              # external entrypoints
└── smoke/            # startup
```

```text
tests/
├── spec/                      # 🧠 ARCHITECTURE CONTRACTS
│   ├── kernel/
│   ├── lifecycle/
│   ├── runtime/
│   ├── messaging/
│   ├── infrastructure/
│   ├── transports/
│   ├── modules/
│   └── launcher/
│
├── unit/                      # 🔬 ISOLATED COMPONENT TESTS
│   ├── lifecycle/
│   ├── runtime/
│   ├── messaging/
│   ├── infrastructure/
│   ├── modules/
│   ├── transports/
│   └── kernel/
│
├── integration/              # 🔗 COMPOSITION GRAPH TESTS
│   ├── kernel/
│   ├── bootstrap/
│   ├── lifecycle/
│   ├── modules/
│   ├── runtime/
│   ├── transports/
│   └── api/
│
├── e2e/                      # 🌐 FULL SYSTEM BEHAVIOR
│   ├── http/
│   ├── cli/
│   ├── grpc/
│   └── kafka/
│
├── smoke/                    # 🚀 ENTRYPOINT SANITY CHECKS
│   ├── import/
│   ├── startup/
│   └── package/
│
├── support/                  # 🧰 TEST INFRA LAYER
│   ├── fixtures/
│   ├── builders/
│   ├── fakes/
│   ├── harness/
│   └── assertions/
│
└── conftest.py
```
