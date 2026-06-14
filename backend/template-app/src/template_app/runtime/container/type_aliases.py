from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeAlias

from template_app.runtime.container.type_vars import T

Factory = Callable[[object], T | Awaitable[T]]

ProviderResult: TypeAlias = T | Awaitable[T]
