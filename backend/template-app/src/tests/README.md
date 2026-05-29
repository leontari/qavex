# MENTAL MODEL

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
