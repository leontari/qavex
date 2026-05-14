"""
Built-in health check providers.

This package contains infrastructure-specific health plugins used by the
runtime health orchestration subsystem.

Providers encapsulate health logic for:

- databases
- caches
- message brokers
- external APIs
- internal platform services

Each provider implements the `HealthCheckPlugin` contract and is designed
for async concurrent execution by the background scheduler.
"""

from __future__ import annotations

from template_app.health.providers.database import (
    DatabaseHealthPlugin,
)
from template_app.health.providers.external_api import (
    ExternalAPIHealthPlugin,
)
from template_app.health.providers.kafka import (
    KafkaHealthPlugin,
)
from template_app.health.providers.redis import (
    RedisHealthPlugin,
)

__all__ = [
    "DatabaseHealthPlugin",
    "ExternalAPIHealthPlugin",
    "KafkaHealthPlugin",
    "RedisHealthPlugin",
]
