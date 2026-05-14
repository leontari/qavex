def test_routes_registered(app):
    paths = sorted(route.path for route in app.routes)

    assert paths == [
        "/health",
        "/live",
        "/ready",
        "/api/v1/users",
    ]
