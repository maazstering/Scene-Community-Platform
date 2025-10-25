from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.backend.api.deps import get_db, get_current_active_user
from app.backend.crud import user as crud_user
from app.backend.schemas.user import UserResponse, UserUpdate, VouchResponse
from app.backend.models.user import User

router = APIRouter()


@router.get("", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    """List all users (for demo user switcher)"""
    users = crud_user.user["get_multi"](db, limit=100)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user profile"""
    user = crud_user.user["get"](db, id=user_id)
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