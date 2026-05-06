from fastapi import APIRouter

from .health import router as health_router
from .metrics import router as metrics_router

observability_router = APIRouter(include_in_schema=False)

for r in [health_router, metrics_router]:
    observability_router.include_router(r)
