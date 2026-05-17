1. [x] Module bootstrap protocol
2. [x] Dynamic module registry
3. [x] Unified lifecycle registry
    - redesigning: Hexagonal Runtime Architecture
4. [x] Infrastructure providers
5. [ ] Event bus abstraction
6. [ ] Command/query execution layer
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
TODO: now we have FastAPI DI Container, Runtime DI Container, Infra DI Container
