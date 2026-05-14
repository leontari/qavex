"""
Scheduler execution policies.

This module defines runtime scheduling policies controlling:

- refresh intervals
- concurrency limits
- stale cache detection
- scheduler timeouts
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SchedulerPolicy:
    """
    Runtime policy for the health scheduler.

    Attributes:
        refresh_interval_seconds:
            Background refresh interval.

        concurrency_limit:
            Maximum number of concurrent plugin executions.

        stale_after_seconds:
            Maximum allowed cache staleness.

        startup_timeout_seconds:
            Maximum startup warmup duration.

    """

    refresh_interval_seconds: int = 10

    concurrency_limit: int = 10

    stale_after_seconds: int = 30

    startup_timeout_seconds: int = 60
