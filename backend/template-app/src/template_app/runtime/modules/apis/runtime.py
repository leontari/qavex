from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from fastapi import APIRouter

    from template_app.runtime.container.container import Container
    from template_app.runtime.container.contracts import DependencyProvider
    from template_app.runtime.lifecycle.hooks import LifecycleHook
    from template_app.runtime.lifecycle.registry import LifecycleRegistry


@dataclass(slots=True)
class ModuleRuntimeAPI:
    """
    Restricted runtime API exposed to modules.

    Modules should only use ModuleRuntimeAPI.
    Modules MUST NOT access RuntimeKernel directly.
    No transport imports allowed.

    FastAPI is removed from runtime kernel.
    Runtime works in the next modes:
      - headless
      - Kafka-only mode
      - gRPC mode
      - CLI mode

    HTTP router registration exists only in HTTP transport.
    """

    container: Container
    lifecycle_registry: LifecycleRegistry

    register_router: Callable[[APIRouter], None]

    def register_router(self, router: APIRouter) -> None:  # noqa: ARG002
        msg = "Router registration requires HTTP transport."
        raise RuntimeError(msg)

    ################
    # lifecycle API
    ################

    def register_startup_hook(self, hook: LifecycleHook) -> None:
        self.lifecycle_registry.register_startup(hook)

    def register_shutdown_hook(self, hook: LifecycleHook) -> None:
        self.lifecycle_registry.register_shutdown(hook)

    #################
    # dependency API
    #################

    def register_dependency(self, provider: DependencyProvider) -> None:
        self.container.register(provider)
