from __future__ import annotations

import pytest
from fastapi import APIRouter

from template_app.runtime.modules.capabilities import (
    ModuleCapability,
)
from tests.factories.module_context import (
    build_module_context,
)
from tests.fakes.providers import (
    FakeDependencyProvider,
)


# def test_router_capability_required() -> None:
#     context = build_module_context(
#         capabilities=frozenset(),
#     )
#
#     with pytest.raises(PermissionError):
#         context.register_router(
#             APIRouter(),
#         )
#
#
# def test_event_bus_capability_required() -> None:
#     context = build_module_context(
#         capabilities=frozenset(),
#     )
#
#     with pytest.raises(PermissionError):
#         _ = context.event_bus

#
# def test_dependency_capability_required() -> None:
#     context = build_module_context(
#         capabilities=frozenset(),
#     )
#
#     with pytest.raises(PermissionError):
#         context.register_dependency(
#             FakeDependencyProvider(
#                 value="test",
#             ),
#         )
#
#
# def test_infrastructure_capability_required() -> None:
#     context = build_module_context(
#         capabilities=frozenset(),
#     )
#
#     with pytest.raises(PermissionError):
#         context.get_provider(
#             "cache",
#         )
#
#
def test_capability_allows_router_registration() -> None:
    context = build_module_context(
        capabilities=frozenset({
            ModuleCapability.ROUTER,
        }),
    )

    context.register_router(
        APIRouter(),
    )
