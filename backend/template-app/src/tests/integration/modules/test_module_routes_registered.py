from __future__ import annotations

from fastapi.routing import APIRoute

from template_app.asgi import app


def test_health_route_registered() -> None:
    paths = {
        route.path
        for route in app.routes
        if isinstance(route, APIRoute)
    }

    assert "/health" in paths


# def test_runtime_route_registered() -> None:
#     paths = {
#         route.path
#         for route in app.routes
#         if isinstance(route, APIRoute)
#     }
#
#     assert "/runtime" in paths
