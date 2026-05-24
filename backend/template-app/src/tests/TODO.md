test package version:

when installed:
if not _version exist -> version is 0.0.0

when installed -> python template_app:version
when installed -> python template_app.__version__
when installed -> template_app --version or template_app -v

when is not installed:
test that it is installed or not

test version is the same that in _version.py
test _version.py exist in installation in site_packages


## What have been tested until now:

### Smoke

- importability;
- package entrypoint;
- ASGI entrypoint;
- local main;
- boot safety.

### Contracts

- runtime contracts;
- registry contracts;
- module contracts;
- kernel contracts;
- architecture invariants.

### Unit

- lifecycle execution;
- registry behavior;
- orchestration logic.

### Integration

- FastAPI integration;
- lifespan execution;
- routes;
- runtime API.

### Test resulting coverage:

- import safety
- runtime bootstrap
- module loading
- lifecycle orchestration
- transport integration
- kernel isolation
- no runtime leakage into FastAPI
- startup/shutdown execution
- plugin registration

## Testing strategy update duet to introducing pluggable transports.

1. kernel is independent from transport
2. transport can be connected dynamically
3. FastAPI doesn't own lifecycle
4. launcher orchestrates lifecycle
5. transports are interchangeable
6. modules are sandboxed
7. runtime survives without HTTP
8. kernel startup/shutdown transport-agnostic
