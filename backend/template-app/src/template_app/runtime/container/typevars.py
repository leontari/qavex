from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeAlias, TypeVar

from template_app.runtime.container.contracts import DependencyResolver

T = TypeVar("T")

Factory = Callable[[DependencyResolver], T | Awaitable[T]]

ProviderResult: TypeAlias = T | Awaitable[T]
