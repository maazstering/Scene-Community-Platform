from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.backend.api.deps import get_db, get_current_active_user
from app.backend.crud import user as crud_user
from app.backend.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.backend.schemas.user import UserCreate, UserResponse
from app.backend.models.user import User
from app.backend.core.security import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return tokens."""
    user = crud_user.user["get_by_email"](db, email=request.phone_or_email)
    if not user:
        user_in = UserCreate(email=request.phone_or_email, name=request.name)
        user = crud_user.user["create"](db, obj_in=user_in)
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
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
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user."""
    return current_user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token."""
    raise HTTPException(status_code=501, detail="Not implemented")