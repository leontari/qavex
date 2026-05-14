from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from template_app.core_.dependencies import get_auth_service, get_user_service
from template_app.services.auth_service import AuthService
from template_app.services.user_service import UserService

router = APIRouter()


# -----------------------------
# Request / Response Models
# -----------------------------


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -----------------------------
# Auth Endpoints
# -----------------------------


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Authenticate a user and return a JWT access token.

    This endpoint validates user credentials using the UserService,
    and if successful, issues a signed JWT token via AuthService.
    """
    user = await user_service.authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = auth_service.create_access_token(user_id=user.id)
    return TokenResponse(access_token=token)
