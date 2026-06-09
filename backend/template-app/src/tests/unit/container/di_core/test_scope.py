from template_app.runtime.container.runtime.scope import ScopeContext, ScopeID

class Dummy:
    pass


def test_scope_set_get():
    scope = ScopeContext(id=ScopeID.new())

    scope.set(("ns", Dummy), 123)

    assert scope.get(("ns", Dummy)) == 123
    assert scope.contains(("ns", Dummy))


def test_scope_clear():
    scope = ScopeContext(id=ScopeID.new())

    scope.set(("ns", Dummy), 123)
    scope.clear()

    assert not scope.contains(("ns", Dummy))
