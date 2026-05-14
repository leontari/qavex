"""
Background health scheduling subsystem.

This package provides:

- periodic async refresh loops
- concurrent health execution
- cached probe orchestration
- scheduler runtime state
- timeout isolation
- concurrency limiting

The scheduler transforms the health system from:

    request-driven execution

into:

    state-driven orchestration.

Health endpoints must read cached scheduler state rather than directly
executing infrastructure checks during HTTP requests.
"""

from __future__ import annotations

from template_app.health.scheduler.cache import (
    HealthStateCache,
)
from template_app.health.scheduler.executor import (
    HealthExecutor,
)
from template_app.health.scheduler.loop import (
    HealthScheduler,
)
from template_app.health.scheduler.policies import (
    SchedulerPolicy,
)
from template_app.health.scheduler.state import (
    CachedHealthResult,
)

__all__ = [
    "CachedHealthResult",
    "HealthExecutor",
    "HealthScheduler",
    "HealthStateCache",
    "SchedulerPolicy",
]
