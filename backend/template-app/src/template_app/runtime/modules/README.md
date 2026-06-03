# Module

Can NOT do:
- use kernel
- mutate runtime
- read private state

Can do:
- register router
- work with lifecycle
- use event bus
- use infrastructure

## A pluggable module`s initializing flow

```
discover_modules()
    ↓
activate_module()
    ↓
module.setup()
```

## A pluggable module`s pipeline
```text
Manifest
  ↓
Activation layer
  ↓
Module.setup(context)
```
