# Improvements

to reorganize and try the following ideas

## Modular Runtime Architecture

```text
template_app/
│
├── runtime/
│   │
│   ├── minimal/
│   │   ├── __init__.py
│   │   ├── bootstrap.py
│   │   ├── runtime.py
│   │   ├── lifecycle.py
│   │   ├── health.py
│   │   ├── metrics.py
│   │   └── logging.py
│   │
│   ├── enhanced/
│   │   ├── __init__.py
│   │   ├── bootstrap.py
│   │   ├── runtime.py
│   │   ├── scheduler.py
│   │   ├── dependency_graph.py
│   │   ├── degradation.py
│   │   ├── readiness.py
│   │   ├── caching.py
│   │   └── policies.py
│   │
│   ├── control_plane/
│   │   ├── __init__.py
│   │   ├── bootstrap.py
│   │   ├── runtime.py
│   │   ├── events/
│   │   ├── reconciliation/
│   │   ├── state_engine/
│   │   ├── decision_engine/
│   │   ├── orchestration/
│   │   └── routing/
│   │
│   ├── shared/
│   │   ├── __init__.py
│   │   ├── contracts.py
│   │   ├── state.py
│   │   ├── health.py
│   │   ├── readiness.py
│   │   ├── metrics.py
│   │   └── lifecycle.py
│   │
│   └── factory.py
```

## Core Architectural Principle

Each runtime level extends the previous one.

### 1. runtime/minimal/

#### Purpose

For:

- CRUD services
- simple APIs
- low-risk microservices

#### Provides

```text
- logging
- lifecycle
- metrics
- health endpoints
- readiness
- basic observability
```

```text
# runtime/minimal/runtime.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MinimalRuntime:
    """
    Lightweight runtime profile.

    Intended for standard CRUD-style services.
    """

    name: str
```


```text
# runtime/minimal/bootstrap.py
from __future__ import annotations

from template_app.runtime.minimal.runtime import (
    MinimalRuntime,
)


def bootstrap_minimal_runtime() -> MinimalRuntime:
    """
    Bootstrap minimal runtime profile.
    """
    return MinimalRuntime(
        name="minimal",
    )
```

```text
# runtime/minimal/init.py
"""
Minimal runtime profile.

Provides:

- health
- readiness
- metrics
- logging
- lifecycle
"""

from __future__ import annotations

from template_app.runtime.minimal.bootstrap import (
    bootstrap_minimal_runtime,
)
from template_app.runtime.minimal.runtime import (
    MinimalRuntime,
)

__all__ = [
    "MinimalRuntime",
    "bootstrap_minimal_runtime",
]
```

### 2. runtime/enhanced/

### Purpose

For:

- business-critical services
- async workers
- orchestration services

### Adds

```text
- dependency graph
- scheduler
- degradation handling
- cached readiness
- concurrent probes
- circuit breakers
```

```text
# runtime/enhanced/runtime.py
from __future__ import annotations

from dataclasses import dataclass

from template_app.runtime.minimal.runtime import (
    MinimalRuntime,
)


@dataclass(slots=True)
class EnhancedRuntime(MinimalRuntime):
    """
    Enhanced runtime profile.

    Adds dependency-aware runtime orchestration.
    """

    dependency_graph_enabled: bool = True

    scheduler_enabled: bool = True
```

```text
# runtime/enhanced/bootstrap.py
from __future__ import annotations

from template_app.runtime.enhanced.runtime import (
    EnhancedRuntime,
)


def bootstrap_enhanced_runtime() -> EnhancedRuntime:
    """
    Bootstrap enhanced runtime profile.
    """
    return EnhancedRuntime(
        name="enhanced",
    )
```

```text
# runtime/enhanced/init.py
"""
Enhanced runtime profile.

Provides:

- dependency graph execution
- cached health checks
- scheduler
- degradation handling
- concurrent probes
"""

from __future__ import annotations

from template_app.runtime.enhanced.bootstrap import (
    bootstrap_enhanced_runtime,
)
from template_app.runtime.enhanced.runtime import (
    EnhancedRuntime,
)

__all__ = [
    "EnhancedRuntime",
    "bootstrap_enhanced_runtime",
]
```

### 3. runtime/control_plane/

#### Purpose

ONLY for:

- API gateways
- orchestration runtimes
- platform services
- routing services

#### Adds

- runtime event bus
- state synthesis
- reconciliation loop
- runtime decision engine
- routing intelligence
- runtime orchestration

```text
# runtime/control_plane/runtime.py
from __future__ import annotations

from dataclasses import dataclass

from template_app.runtime.enhanced.runtime import (
    EnhancedRuntime,
)


@dataclass(slots=True)
class ControlPlaneRuntime(EnhancedRuntime):
    """
    Full runtime orchestration platform.

    Intended ONLY for:
    - gateways
    - orchestration services
    - platform runtimes
    """

    reconciliation_enabled: bool = True

    event_bus_enabled: bool = True

    state_engine_enabled: bool = True
```

```text
# runtime/control_plane/bootstrap.py
# from __future__ import annotations

from template_app.runtime.control_plane.runtime import (
    ControlPlaneRuntime,
)


def bootstrap_control_plane_runtime() -> ControlPlaneRuntime:
    """
    Bootstrap full control-plane runtime.
    """
    return ControlPlaneRuntime(
        name="control_plane",
    )
```

```text
# runtime/control_plane/init.py
 """
Full runtime control-plane profile.

Provides:

- reconciliation loop
- runtime event bus
- decision engine
- state synthesis
- orchestration runtime
"""

from __future__ import annotations

from template_app.runtime.control_plane.bootstrap import (
    bootstrap_control_plane_runtime,
)
from template_app.runtime.control_plane.runtime import (
    ControlPlaneRuntime,
)

__all__ = [
    "ControlPlaneRuntime",
    "bootstrap_control_plane_runtime",
]
```

### 4. runtime/shared/

#### Purpose

Shared abstractions across ALL runtime profiles.

#### Contains
- protocols
- contracts
- runtime models
- health contracts
- lifecycle abstractions

```text
# runtime/shared/contracts.py
from __future__ import annotations

from typing import Protocol


class Runtime(Protocol):
    """
    Base runtime contract.
    """

    name: str
```

### 5. runtime/factory.py

#### IMPORTANT

This becomes the unified runtime selector.

```text
# runtime/factory.py
from __future__ import annotations

from enum import StrEnum

from template_app.runtime.control_plane import (
    bootstrap_control_plane_runtime,
)
from template_app.runtime.enhanced import (
    bootstrap_enhanced_runtime,
)
from template_app.runtime.minimal import (
    bootstrap_minimal_runtime,
)


class RuntimeProfile(StrEnum):
    """
    Runtime profile selection.
    """

    MINIMAL = "minimal"

    ENHANCED = "enhanced"

    CONTROL_PLANE = "control_plane"


def bootstrap_runtime(
    profile: RuntimeProfile,
):
    """
    Bootstrap selected runtime profile.
    """

    if profile == RuntimeProfile.MINIMAL:
        return bootstrap_minimal_runtime()

    if profile == RuntimeProfile.ENHANCED:
        return bootstrap_enhanced_runtime()

    if profile == RuntimeProfile.CONTROL_PLANE:
        return bootstrap_control_plane_runtime()

    msg = f"Unsupported runtime profile: {profile}"

    raise ValueError(msg)
```

### Example Usage

#### CRUD Service

```text
runtime = bootstrap_runtime(
    RuntimeProfile.MINIMAL,
)
```

#### Important Worker

```
runtime = bootstrap_runtime(
    RuntimeProfile.ENHANCED,
)
```

#### Gateway / Platform Service
```
runtime = bootstrap_runtime(
    RuntimeProfile.CONTROL_PLANE,
)
```

### Final Production Recommendation

#### Minimal Runtime

Use in:

- 80% of services

#### Enhanced Runtime

Use in:

- critical business services
- async workers
- orchestration services
- Control Plane Runtime

#### Use ONLY in:

- gateways
- routing layers
- internal platform services
- runtime orchestration services

#### Most Important Architectural Win

Avoid:

`every service = giant platform runtime`

while still having:

`one unified runtime framework`

with progressive capability escalation.
