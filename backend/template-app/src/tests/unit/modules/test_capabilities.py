import pytest
from fastapi import APIRouter

from template_app.bootstrap.modules.capabilities import (
    ModuleCapability,
)
from tests.factories.module_context import (
    build_module_context,
)


def test_router_capability_required() -> None:

    context = build_module_context(
        frozenset(),
    )

    with pytest.raises(PermissionError):

        context.register_router(
            APIRouter(),
        )


def test_event_bus_capability_required() -> None:

    context = build_module_context(
        frozenset(),
    )

    with pytest.raises(PermissionError):

        _ = context.event_bus


def test_dependency_capability_required() -> None:

    context = build_module_context(
        frozenset(),
    )

    with pytest.raises(PermissionError):

        context.register_dependency(  # type: ignore[arg-type]
            object(),
        )


def test_infrastructure_capability_required() -> None:

    context = build_module_context(
        frozenset(),
    )

    with pytest.raises(PermissionError):

        context.get_provider(
            "cache",
        )


def test_capability_allows_router_registration() -> None:

    context = build_module_context(
        frozenset({
            ModuleCapability.ROUTER,
        }),
    )

    context.register_router(
        APIRouter(),
    )
