import pytest

from template_app.runtime.container.container import Container


@pytest.mark.asyncio
async def test_nested_scopes(container: Container) -> None:
    async with container.scope() as parent:
        assert container._manager._context.current_scope == parent

        async with container.scope() as child:
            assert parent != child
            assert container._manager._context.current_scope == child

        assert container._manager._context.current_scope == parent

    assert container._manager._context.current_scope is None
