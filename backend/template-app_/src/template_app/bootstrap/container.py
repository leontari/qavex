"""
DI Container.

Latter can be changed for something like:
- dishka
- punq
- lagom
- dependency-injector

"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Container:
    database: object | None = None
    redis: object | None = None
    kafka: object | None = None
