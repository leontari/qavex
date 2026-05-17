"""
API package containing versioned HTTP route definitions.

Whole dumb.

Each version subpackage (e.g., v1) exposes routers grouped by domain
(auth, users, etc.). The top-level router aggregates all API versions
for inclusion in the FastAPI application.
"""
