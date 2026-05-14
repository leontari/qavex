"""
Application startup orchestration.

This module coordinates initialization of runtime infrastructure and
background orchestration systems.

Startup responsibilities include:

- database initialization
- Redis initialization
- Kafka initialization
- scheduler startup
- health runtime warmup
- runtime state transitions
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from template_app.core.lifecycle.state import (
    LifecycleStage,
)
from template_app.health.scheduler.loop import (
    HealthScheduler,
)

logger = logging.getLogger(__name__)


async def startup(
    app: FastAPI,
) -> None:
    """
    Execute application startup sequence.

    Args:
        app:
            FastAPI application instance.
    """
    runtime_state = app.state.runtime_state

    runtime_state.stage = LifecycleStage.STARTING

    logger.info(
        "Application startup initiated.",
    )

    scheduler: HealthScheduler = app.state.health_scheduler

    await scheduler.start()

    runtime_state.stage = LifecycleStage.RUNNING

    runtime_state.startup_complete = True

    logger.info(
        "Application startup completed.",
    )
