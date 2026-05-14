"""
Application shutdown orchestration.

This module coordinates graceful shutdown of runtime-managed resources and
background orchestration systems.

Shutdown responsibilities include:

- stopping background schedulers
- closing HTTP clients
- stopping Kafka producers
- closing Redis connections
- disposing SQLAlchemy engines
- task cancellation
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from template_app.core_.lifecycle.state import (
    LifecycleStage,
)
from template_app.health.scheduler.loop import (
    HealthScheduler,
)

logger = logging.getLogger(__name__)


async def shutdown(
    app: FastAPI,
) -> None:
    """
    Execute graceful application shutdown.

    Args:
        app:
            FastAPI application instance.
    """
    runtime_state = app.state.runtime_state

    runtime_state.stage = LifecycleStage.STOPPING

    logger.info(
        "Application shutdown initiated.",
    )

    scheduler: HealthScheduler = app.state.health_scheduler

    await scheduler.stop()

    task_manager = app.state.task_manager

    await task_manager.shutdown()

    runtime_state.stage = LifecycleStage.STOPPED

    runtime_state.shutdown_complete = True

    logger.info(
        "Application shutdown completed.",
    )
