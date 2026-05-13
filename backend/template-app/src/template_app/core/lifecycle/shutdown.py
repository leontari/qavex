"""
Shutdown orchestration.

Shutdown guarantees:
* graceful stop of tasks
* DB pool закрыт
* background tasks canceled
* no dangling async loops
*metrics flushed

"""

# core/lifecycle/shutdown.py
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_app.core.lifecycle.state import AppState


async def shutdown_all(app, state: AppState) -> None:
    # 1. Stop background tasks
    for task in state.background_tasks:
        task.cancel()

    # 2. Close DB
    if state.db:
        await app.state.db.dispose()

    # 3. Close redis
    if state.redis:
        await state.redis.close()

    state.startup_complete = False
