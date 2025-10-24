from fastapi import APIRouter, Depends, HTTPException
from app.backend.schemas.user import VouchResponse, VouchCreate
from app.backend.api.deps import get_current_active_user
from app.backend.models.user import User

router = APIRouter()


@router.post("", response_model=VouchResponse, status_code=201)
async def create_vouch(
    vouch_in: VouchCreate, current_user: User = Depends(get_current_active_user)
):
    """Create a new vouch for another user."""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("", response_model=list[VouchResponse])
async def get_my_vouches(current_user: User = Depends(get_current_active_user)):
    """Get vouches given by the current user."""
    return []