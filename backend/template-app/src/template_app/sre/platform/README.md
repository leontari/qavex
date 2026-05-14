# Full control plane

Things to be considered before using it:
- lightweight runtime
- advanced runtime
- centralized control plane

This is not a `health subsystem` but a `runtime orchestration kernel`

It has:

- reconciliation engine
- state synthesis system
- runtime decision engine
- event-driven control plane

## USE CASES:

### A. High-criticality microservices:

- payments
- auth
- trading
- messaging
- orchestrarion
- workflow execution

when it's important for a microservice:

- graceful degradation
- dependency-aware readiness
- circuit breaking
- traffic safety
- runtime orchestration

Example:

```
payment service:
- postgres required
- redis optional
- kafka optional

decision engine:
if kafka fails:
    degraded but still traffic-safe

if postgres fails:
    remove from readiness
```

### B. API Gateways

Gateway is an ideal place for control plane runtime as it:

- knows downstream services
- can do rerouting
- can dor failover
- accepts traffic decisions

Example:

```text
if user-service degraded:
    route to read replica
```

### C.Platform services

It fits well:

- scheduler service
- orchestration service
- worker runtime
- event processor
- queue orchestrator

### D.Service Mesh Control Services

Examples:
- internal ingress
- routing layer
- runtime router

## WHERE NOT TO USE IT

### ❌CRUD microservices:

- profile-service
- catalog-service
- comments-service

It's enough for them:
```text
/health
/ready
Prometheus metrics
basic circuit breaker
```

### ❌ Internal admin tools

### ❌ Small low-risk services

## Follow Runtime Tiers

```text
tiered runtime architecture
```

### Tier - Minimal Runtime

it's enough for 80% of microservices:

```text
- health checks
- metrics
- logging
- readiness
```

### Tier 2 - Enhanced Runtime

For critical services:

```text
- dependency graph
- scheduler
- cache
- degradation
```

### Tier 3 — Full Control Plane

ONLY for:

```text
gateway
orchestration
critical infra services
```

## Design

Core `runtime orchestration kernel` components:

- Runtime Event Bus
- State Transition Engine

### Goal

This subsystem transforms the platform from:

- passive health reporting

into:

- active runtime state orchestration
- event-driven reconciliation
- observability-grade control plane runtime

The design is inspired by:

- Kubernetes controllers
- Datadog runtime synthesis
- service mesh control planes
- operator reconciliation loops
- event-driven infrastructure runtimes

### High-Level Architecture

```text
health plugins
      ↓
executor
      ↓
decision engine
      ↓
state transition engine
      ↓
runtime event bus
      ↓
actions / metrics / alerts / reconciliation
```

### Target Structure

```text
platform/
├── events/
│   ├── __init__.py
│   ├── bus.py
│   ├── emitter.py
│   ├── subscribers.py
│   ├── event_types.py
│   ├── models.py
│   └── dispatcher.py
│
├── state_engine/
│   ├── __init__.py
│   ├── engine.py
│   ├── transitions.py
│   ├── policies.py
│   ├── state_store.py
│   └── snapshots.py
│
├── reconciliation/
│   ├── reconcile_loop.py
│   ├── actions.py
│   └── planner.py
```

## Kubernetes Integration

### readiness

/ready should consume:

`RuntimeStateStore.get_snapshot()`

NOT raw health plugins.

## Prometheus Integration

Export:

```text
runtime_health_score
runtime_degraded
runtime_unhealthy
runtime_failed_services_total
```

## SRE Integration

SRE systems consume:

- runtime transitions
- degradation events
- readiness changes
- reconciliation actions
- state snapshots

instead of raw probes.

## Final Mental Model

```text
Infrastructure
    ↓
Health Graph
    ↓
Decision Engine
    ↓
Runtime State Engine
    ↓
Event Bus
    ↓
Reconciliation Loop
    ↓
Platform Actions
    ↓
Kubernetes / SRE / Traffic Routing
```

## What is it for

This is not for:

`FastAPI microservice template`

This is for:

'runtime orchestration platform kernel'

with:

- control plane
- event system
- state synthesis
- reconciliation engine
- runtime orchestration
- observability integration
- Kubernetes-compatible readiness intelligence
