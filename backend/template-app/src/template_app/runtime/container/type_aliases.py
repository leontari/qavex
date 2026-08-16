"""Typing aliases."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeAlias

from .contracts import DependencyResolver
from .type_vars import T

Factory = Callable[[DependencyResolver], T | Awaitable[T]]

ProviderResult: TypeAlias = T | Awaitable[T]
