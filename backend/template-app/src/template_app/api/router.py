from fastapi import APIRouter
from template_app.api.v1.users import router as users_router

api_router = APIRouter(prefix="/api")

api_router.include_router(users_router, prefix="/users")
