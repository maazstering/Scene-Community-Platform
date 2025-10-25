from fastapi import APIRouter, Depends, HTTPException
from app.backend.api.deps import get_current_active_user
from app.backend.schemas.user import UserResponse, UserUpdate, VouchResponse
from app.backend.models.user import User
from app.backend.data.memory_store import memory_store

router = APIRouter()


@router.get("", response_model=list[UserResponse])
async def get_users():
    """List all users (for demo user switcher)"""
    users = memory_store.get_users()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get user profile"""
    user = memory_store.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """Update user profile"""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{user_id}/vouches", response_model=list[VouchResponse])
async def get_user_vouches(user_id: str):
    """Get vouches for a user"""
    return []