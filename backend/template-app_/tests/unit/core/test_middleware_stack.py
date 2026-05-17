def test_middleware_registered(app):
    middleware = [
        m.cls.__name__
        for m in app.user_middleware
    ]

    assert "CORSMiddleware" in middleware
