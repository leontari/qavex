1. [x] Module bootstrap protocol
2. [x] Dynamic module registry
3. [x] Unified lifecycle registry
    - [x] redesigning: Hexagonal Runtime Architecture
4. [x] Infrastructure providers
5. [x] Event bus abstraction
6. [x] Command/query execution layer
   - redesign for future:
     - [ ] RedisStreamEventBridge
     - [ ] NatsEventBridge
     - [ ] DistributedCommandGateway
     - [ ] RPCQueryGateway
7. [x] pluggable transports layer
8. [ ] Background task runtime
9. [ ] Plugin health checks
10. [ ] Runtime capabilities registry
11. [ ] Internal event system

## Provider features to implement after the kernel construction:

- [ ] lazy providers
- [ ] provider health
- [ ] provider dependencies
- [ ] provider retries
- [ ] distributed providers
- [ ] provider hot reload
- [ ] provider observability
- [ ] async resource pools
- [ ] provider isolation

## container.py - runtime service registry, implement latter:
- [x] lazy providers
- [x] scoped dependencies
- [x] async providers
- [x] singleton lifecycle
- [x] transient services
- [x] provider factories
- [x] typed resolution
- [x] plugin isolation
- [x] module namespaces

## DependencyProvider - controlled dependency lifecycle
- [x] SingletonProvider
- [x] FactoryProvider
- [x] AsyncProvider
- [x] ScopedProvide

## Launcher
- [ ] runtime node graph executor instead of switch-case?
- [ ] runtime phases
- [ ] runtime conditions
- [ ] runtime readiness
- [ ] runtime health graph
- [ ] runtime capability negotiation


# Architecture upgrade plan

## PHASE 1

- [x] ApplicationBuilder V3
- [x] Launcher V3
- [x] Transport Factory
- [x] ASGI import-safe mode

## PHASE 2
- [x] DI Container V1
- [x] Scopes
- [x] Factories
- [x] Resolve
- [x] Diagnostics

## PHASE 3

- [ ] Plugin Protocol
- [ ] Module Discovery
- [ ] Module Loader
- [ ] Module Setup Context

## PHASE 4

- [ ] Builder Module Auto Loading

## PHASE 5

- [ ] Event Classification
- [ ] DomainEvent
- [ ] IntegrationEvent
- [ ] SystemEvent

## PHASE 6

- [ ] GUI Transport

## PHASE 7

- [ ] Control Plane
- [ ] Runtime Inspector
- [ ] Observability

## PHASE 8

- [ ] Distributed Runtime
- [ ] Kafka Bridge
- [ ] gRPC Bridge
- [ ] Cluster Features
