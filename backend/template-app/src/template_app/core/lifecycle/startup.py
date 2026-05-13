"""Startup orchestration.

Startup guarantees:
* DB pool создан
* Redis/Kafka (если есть) инициализированы
* health subsystem запущен
* cached probes прогреты
* circuit breakers инициализированы
* observability активирована

"""

# core/lifecycle/startup.py
from __future__ import annotations

from fastapi import FastAPI
from template_app.core.lifecycle.state import AppState


engine = create_db_engine(settings)

session_factory = create_session_factory(engine)

app.state.db_engine = engine
app.state.session_factory = session_factory


async def startup_all(app: FastAPI, state: AppState) -> None:
    # 1. DB
    state.db = app.state.db_engine

    # 2. Redis (если есть)
    if hasattr(app.state, "redis"):
        state.redis = app.state.redis

    # 3. Warmup health system
    await warmup_health_checks(state)

    # 4. Background tasks
    await start_background_tasks(app, state)

    state.startup_complete = True
