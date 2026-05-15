def test_dependency_overrides_empty(app):
    assert app.dependency_overrides == {}
