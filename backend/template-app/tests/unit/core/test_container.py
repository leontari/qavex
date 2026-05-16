from __future__ import annotations

import pytest

from template_app.bootstrap.container import Container


def test_container_registers_dependency() -> None:
    container = Container()

    dependency = object()

    container.register("service", dependency)

    assert container.resolve("service") is dependency


def test_container_contains_dependency() -> None:
    container = Container()

    container.register("service", object())

    assert container.contains("service")


def test_container_raises_for_missing_dependency() -> None:
    container = Container()

    with pytest.raises(LookupError):
        container.resolve("missing")
