from fastapi import APIRouter, Depends, HTTPException
from app.backend.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.backend.schemas.user import UserResponse
from app.backend.api.deps import get_current_active_user
from app.backend.models.user import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Simplified login for demo purposes."""
    return {
        "access_token": "stub_access_token",
        "refresh_token": "stub_refresh_token",
        "token_type": "bearer",
        "expires_in": 1800,
    }


@router.post("/logout")
async def logout():
    """Logout user (stub)."""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token."""
    raise HTTPException(status_code=501, detail="Not implemented")