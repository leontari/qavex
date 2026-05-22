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
7. [ ] Background task runtime
8. [ ] Plugin health checks
9. [ ] Runtime capabilities registry
10. [ ] Internal event system

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
- [ ] lazy providers
- [ ] scoped dependencies
- [ ] async providers
- [ ] singleton lifecycle
- [ ] transient services
- [ ] provider factories
- [ ] typed resolution
- [ ] plugin isolation
- [ ] module namespaces

## DependencyProvider - controlled dependency lifecycle
- [ ] SingletonProvider
- [ ] FactoryProvider
- [ ] AsyncProvider
- [ ] ScopedProvider


## Target for now:
1) new transport layer
```
template_app/
├── bootstrap/
│   ├── kernel/              # core runtime (NO FastAPI dependency)
│   ├── runtime/             # lifecycle, state
│   ├── modules/             # plugin system
│   ├── transport/           # abstraction + implementations
│   │   ├── http/
│   │   ├── kafka/
│   │   ├── grpc/
│   │   ├── cli/
│   │   └── manager.py
│   ├── launcher/            # kernel run http/kafka/grpc/cli
│   ├── config/              # unified config
│   └── bootstrap.py         # single entrypoint
│
├── asgi.py (thin)
├── cli.py  (thin)
└── main.py (optional)
```

2) a lot of renames to separate concerns

```text
template_app/
├── kernel/              ← EVERYTHING CORE
│
│   ├── bootstrap.py     ← composition root
│   ├── kernel.py        ← RuntimeKernel
│   ├── context.py       ← KernelContext
│   ├── state.py         ← KernelState
│   ├── lifecycle/
│   ├── messaging/
│   ├── modules/
│   ├── transport/
│   ├── infrastructure/
│   └── container/
│
├── transports/          ← concrete transport implementations
│   ├── http/
│   ├── grpc/
│   ├── kafka/
│   └── cli/
│
├── app/
├── domain/
├── config/
└── deploy/
```
