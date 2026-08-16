import pytest

from template_app.runtime.container import Container


@pytest.mark.asyncio
async def test_nested_scopes(container: Container) -> None:
    async with container.scope() as parent:
        assert container._manager._context.current_context.scope_id == parent

        async with container.scope() as child:
            assert parent != child
            assert container._manager._context.current_context.scope_id == child

        assert container._manager._context.current_context.scope_id == parent

    assert container._manager._context.current_context.scope_id is None
