from fastapi import APIRouter, Depends, HTTPException
from app.backend.schemas.activity import (
    ActivityResponse,
    ActivityCreate,
    ActivityRequestResponse,
    ActivityRequestCreate,
    ActivityRequestUpdate,
)
from app.backend.api.deps import get_current_active_user
from app.backend.models.user import User

router = APIRouter()


@router.get("", response_model=list[ActivityResponse])
async def get_activities():
    """List all activities"""
    return []


@router.post("", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity: ActivityCreate, current_user: User = Depends(get_current_active_user)
):
    """Create a new activity"""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: str):
    """Get activity details"""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post(
    "/{activity_id}/requests", response_model=ActivityRequestResponse, status_code=201
)
async def request_to_join_activity(
    activity_id: str,
    request_data: ActivityRequestCreate,
    current_user: User = Depends(get_current_active_user),
):
    """Request to join an activity"""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{activity_id}/requests", response_model=list[ActivityRequestResponse])
async def get_activity_requests(
    activity_id: str, current_user: User = Depends(get_current_active_user)
):
    """Get join requests for an activity (host only)"""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.patch(
    "/{activity_id}/requests/{request_id}", response_model=ActivityRequestResponse
)
async def update_activity_request(
    activity_id: str,
    request_id: str,
    update_data: ActivityRequestUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """Approve or reject a join request (host only)"""
    raise HTTPException(status_code=501, detail="Not implemented")