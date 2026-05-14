"""
Runtime state synthesis engine.

Responsible for:

- runtime truth generation
- state classification
- transition emission
- runtime snapshot persistence
"""

from __future__ import annotations

from template_app.platform.state_engine.engine import (
    RuntimeStateEngine,
)
from template_app.platform.state_engine.policies import (
    RuntimeStatePolicy,
)
from template_app.platform.state_engine.snapshots import (
    RuntimeSnapshot,
)
from template_app.platform.state_engine.state_store import (
    RuntimeStateStore,
)
from template_app.platform.state_engine.transitions import (
    RuntimeStatus,
)

__all__ = [
    "RuntimeStateEngine",
    "RuntimeStatePolicy",
    "RuntimeSnapshot",
    "RuntimeStateStore",
    "RuntimeStatus",
]
