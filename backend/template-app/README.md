# Multi-Runtime Kernel — Migration Plan

Vision

Build a production-grade distributed application runtime kernel for Python microservices with:

- multi-transport runtime
- Kubernetes-native orchestration
- DAG lifecycle execution
- runtime task scheduler
- unified observability
- modular plugin architecture
- distributed messaging
- self-aware runtime state model

The system must support:

- HTTP
- Kafka workers
- gRPC
- CLI
- future transports

without changing kernel internals.

# Architectural Principles

## 1. Runtime-first architecture

Kernel owns:

- lifecycle
- orchestration
- state
- telemetry
- scheduling
- readiness
- messaging

Transports are adapters only.

## 2. Transport independence

## Kernel MUST NOT depend on:

FastAPI
Kafka SDK
gRPC SDK

Transport layer is optional and replaceable.

## 3. Kubernetes-native runtime

Runtime must:

- expose readiness
- support draining
- support graceful shutdown
- support dependency graph execution
- expose observability
- support orchestration

## 4. Self-aware runtime

Runtime knows:

- which modules exist
- which transports exist
- readiness state
- active tasks
- dependency graph
- failures
- retries
- worker state

# Current State

## Already implemented

### Runtime kernel

- RuntimeKernel
- KernelContext
- RuntimeState

### Lifecycle
- LifecycleManager
- LifecycleRegistry
- DAG executor
- retry policies
- readiness probes

### Messaging

- command bus
- query bus
- event bus

### Transports

- HTTP
- Kafka
- gRPC
- CLI

### Module system

- ModuleContext
- capabilities
- manifests
- discovery

# Migration Goal

Move from:

`hook-based orchestration`

to:

`runtime task orchestration platform`

## PHASE 1 — Stabilize Current Runtime

### Goal

Freeze current architecture before major migration.

## PHASE 2 — RuntimeTask Migration

### Goal

Replace hook-based runtime with scheduler-driven runtime.

New Core Abstraction:

`RuntimeTask`  - canonical orchestration primitive.

#### Responsibilities

A task describes:

- executable runtime unit
- dependencies
- retries
- health
- transport affinity
- scheduling policy

#### RuntimeTask model
```
name
phase
handler
dependencies
retry_policy
critical
transport_affinity
module_affinity
health_policy
timeouts
restart_policy
```

Hooks become compatibility adapters
```
LifecycleHook
    ↓
RuntimeTask
```

## New Runtime Components:

- RuntimeScheduler
- RuntimeTaskRegistry
- RuntimeTaskStateGraph
- RuntimeSupervisor


## PHASE 3 — Kubernetes-grade Runtime
### Goal

Transform runtime into cluster-native orchestration engine.

Runtime states
```
BOOTING
STARTING
READY
DEGRADED
DRAINING
STOPPING
STOPPED
FAILED
```

## PHASE 4 — Observability Runtime

### Goal

Make runtime fully observable via `Runtime telemetry layer`

- RuntimeTelemetry
- SRE Endpoints
```
/live
/ready
/startup
/metrics
/version
/info
Health
/health/runtime
/health/dependencies
/health/transports
/health/workers
Debug
/debug/tasks
/debug/runtime
/debug/events
/debug/connections
/debug/config

Disabled by default.
```

## PHASE 5 — Universal Module Runtime

Goal

Turn modules into self-contained runtime units.

# TARGET:

`microservice kernel` which is:

- transport-agnostic runtime
- modular runtime graph
- runtime domains
- lifecycle orchestration
- distributed-ready kernel
- kubernetes-oriented architecture
