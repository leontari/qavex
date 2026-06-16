from tkinter.font import names

import pytest

from template_app.runtime.container.container import Container
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.models.scope import (
    DependencyScope,
    ScopeID,
)


@pytest.mark.asyncio
async def test_scope_context_propagation(
    container: Container,
    scope_id: ScopeID,
    namespace: Namespace,
) -> None:
    class ScopedService:
        pass

    class Provider:
        async def provide(self, resolver):
            return ScopedService()

    container.register(
        contract=ScopedService,
        provider=Provider(),
        scope=DependencyScope.SCOPED,
        namespace=namespace,
    )

    async with container.scope() as scope_id:
        context_scope = container._manager._context.current_scope

        assert context_scope == scope_id

        service = await container.resolve(ScopedService, namespace=namespace)

        assert service is not None
