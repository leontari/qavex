A pluggable module`s initializing flow

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
