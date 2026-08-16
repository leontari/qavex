import pytest

from template_app.runtime.container.runtime.resolution import (
    ResolutionManager,
)
from template_app.runtime.container.runtime.scope import (
    ScopeHandle,
    ScopeManager,
)


@pytest.mark.asyncio
async def test_scope_handle_creates_scope(
    scope_manager: ScopeManager,
    context_manager: ResolutionManager,
) -> None:

    handle = ScopeHandle(scope_manager, context_manager)

    async with handle as scope_id:
        assert scope_manager.exists(scope_id)
        assert context_manager.current_context.scope_id == scope_id


@pytest.mark.asyncio
async def test_scope_handle_closes_scope(
    scope_manager: ScopeManager,
    context_manager: ResolutionManager,
) -> None:
    handle = ScopeHandle(scope_manager, context_manager)

    async with handle as scope_id:
        pass

    assert not scope_manager.exists(scope_id)
    assert context_manager.current_context is None


@pytest.mark.asyncio
async def test_scope_handle_cleanup_on_exception(
    scope_manager: ScopeManager,
    context_manager: ResolutionManager,
) -> None:
    handle = ScopeHandle(scope_manager, context_manager)

    with pytest.raises(RuntimeError):
        async with handle as scope_id:
            raise RuntimeError()

    assert not scope_manager.exists(scope_id)
    assert context_manager.current_context is None
