from runtime.container.scope import ScopeManager


def test_create_scope() -> None:
    manager = ScopeManager()

    scope = manager.create()

    assert manager.exists(scope.id)


def test_close_scope() -> None:
    manager = ScopeManager()

    scope = manager.create()

    manager.close(scope.id)

    assert not manager.exists(scope.id)
