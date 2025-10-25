from fastapi import APIRouter, Depends, HTTPException
from app.backend.api.deps import get_current_active_user
from app.backend.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.backend.schemas.user import UserResponse
from app.backend.models.user import User
from app.backend.core.security import create_access_token, create_refresh_token
from app.backend.data.memory_store import memory_store

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Authenticate user and return tokens."""
    user = memory_store.get_user_by_email(email=request.phone_or_email)
    if not user:
        if request.name:
            user = memory_store.create_user(
                name=request.name, email=request.phone_or_email
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")
    access_token = create_access_token(subject=user["id"])
    refresh_token = create_refresh_token(subject=user["id"])
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800,
    }


@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)."""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_active_user)):
    """Get current authenticated user."""
    return current_user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token."""
    raise HTTPException(status_code=501, detail="Not implemented")