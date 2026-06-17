from __future__ import annotations

import asyncio

from template_app.runtime.container.container import Container
from template_app.runtime.container.models.namespace import Namespace


class Service: ...


async def test_singleton_concurrent_resolution(
    container: Container,
    namespace: Namespace,
) -> None:
    results = await asyncio.gather(
        container.resolve(Service),
        container.resolve(Service),
        container.resolve(Service),
    )

    assert results[0] is results[1]
    assert results[1] is results[2]


async def test_scoped_concurrent_resolution(
    container: Container,
) -> None:
    async with container.scope():

        results = await asyncio.gather(
            container.resolve(Service),
            container.resolve(Service),
            container.resolve(Service),
        )

        assert results[0] is results[1]
        assert results[1] is results[2]


async def test_scoped_isolation(
    container,
):
    async with container.scope():
        first = await container.resolve(Service)

    async with container.scope():
        second = await container.resolve(Service)

    assert first is not second


async def test_transient_always_new(
    container,
):
    first = await container.resolve(Service)
    second = await container.resolve(Service)

    assert first is not second
