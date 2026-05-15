"""
Health aggregation logic.

Aggregation logic (READY / HEALTH core)
"""

from __future__ import annotations

import asyncio

from template_app.services.health.checks import check_database
from template_app.services.health.checks import check_external_api
from template_app.services.health.checks import check_migrations
from template_app.services.health.checks import check_redis
from template_app.services.health.registry import registry
from template_app.services.health.timeout import run_with_timeout

registry.register("database", check_database)
registry.register("redis", check_redis)
registry.register("external_api", check_external_api)
registry.register("migrations", check_migrations)


async def get_readiness_state() -> dict:
    """
    Execute all readiness checks.

    Returns:
        Aggregated readiness state.

    """
    results = await asyncio.gather(*[
        run_with_timeout(check) for _, check in registry.items()
    ])

    checks = {
        name: result
        for (name, _), result in zip(registry.items(), results, strict=False)
    }

    return {
        "status": "ready" if all(checks.values()) else "not_ready",
        "checks": checks,
    }


async def get_full_health() -> dict:
    """
    Return full system health snapshot.

    Returns:
        Deep health diagnostics.

    """
    readiness = await get_readiness_state()

    return {
        "system": readiness,
        "mode": "deep_health",
    }
