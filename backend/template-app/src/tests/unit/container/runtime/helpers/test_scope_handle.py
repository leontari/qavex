import pytest

from template_app.runtime.container.runtime.helpers.context_manager import (
    ResolutionContextManager,
)
from template_app.runtime.container.runtime.helpers.scope import ScopeHandle
from template_app.runtime.container.runtime.scope_manager import ScopeManager


@pytest.mark.asyncio
async def test_scope_handle_creates_scope(
    scope_manager: ScopeManager,
    context_manager: ResolutionContextManager,
) -> None:

    handle = ScopeHandle(scope_manager, context_manager)

    async with handle as scope_id:
        assert scope_manager.exists(scope_id)
        assert context_manager.current_scope == scope_id


@pytest.mark.asyncio
async def test_scope_handle_closes_scope(
    scope_manager: ScopeManager,
    context_manager: ResolutionContextManager,
) -> None:
    handle = ScopeHandle(scope_manager, context_manager)

    async with handle as scope_id:
        pass

    assert not scope_manager.exists(scope_id)
    assert context_manager.current_scope is None


@pytest.mark.asyncio
async def test_scope_handle_cleanup_on_exception(
    scope_manager: ScopeManager,
    context_manager: ResolutionContextManager,
) -> None:
    handle = ScopeHandle(scope_manager, context_manager)

    with pytest.raises(RuntimeError):
        async with handle as scope_id:
            raise RuntimeError()

    assert not scope_manager.exists(scope_id)
    assert context_manager.current_scope is None
