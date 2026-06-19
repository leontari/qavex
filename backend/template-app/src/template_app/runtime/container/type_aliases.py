"""Typing aliases."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeAlias

from .type_vars import T

Factory = Callable[[object], T | Awaitable[T]]

ProviderResult: TypeAlias = T | Awaitable[T]
