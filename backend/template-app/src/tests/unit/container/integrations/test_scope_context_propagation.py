import pytest

from template_app.runtime.container.models.scope import DependencyScope


@pytest.mark.asyncio
async def test_scope_context_propagation(container, scope_id):
    class ScopedService:
        pass

    class Provider:
        async def provide(self, resolver):
            return ScopedService()

    container.register(
        contract=ScopedService,
        provider=Provider(),
        scope=DependencyScope.SCOPED,
    )

    async with container.scope() as scope_id:
        context_scope = container._manager._context.current_scope

        assert context_scope == scope_id

        service = await container.resolve(ScopedService)

        assert service is not None
