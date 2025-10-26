from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.backend.api.deps import get_current_active_user
from app.backend.schemas.activity import (
    ActivityCreate,
    ActivityRequestResponse,
    ActivityRequestCreate,
    ActivityRequestUpdate,
    ActivityResponse,
)
from app.backend.models.user import User
from app.backend.data.memory_store import memory_store

router = APIRouter()


@router.get("", response_model=list[dict])
async def get_activities(host_id: Optional[str] = None, status: Optional[str] = None):
    """List all activities"""
    activities = memory_store.get_activities()
    if host_id == "me":
        return [a for a in activities if a["host_user_id"] == "user_1"]
    if status:
        return [a for a in activities if a.get("status") == status]
    return activities


@router.post("", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity_in: ActivityCreate, current_user: dict = Depends(get_current_active_user)
):
    """Create a new activity"""
    activity = memory_store.create_activity(
        activity_in=activity_in, host_user_id=current_user["id"]
    )
    return activity


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: str):
    """Get activity details"""
    activity = memory_store.get_activity_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


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