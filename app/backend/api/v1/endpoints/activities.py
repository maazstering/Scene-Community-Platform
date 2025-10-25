from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.backend.api.deps import get_db, get_current_active_user
from app.backend.crud import activity as crud_activity
from app.backend.schemas.activity import (
    ActivityResponse,
    ActivityCreate,
    ActivityRequestResponse,
    ActivityRequestCreate,
    ActivityRequestUpdate,
)
from app.backend.models.user import User

router = APIRouter()


@router.get("", response_model=list[ActivityResponse])
async def get_activities(db: Session = Depends(get_db)):
    """List all activities"""
    activities = crud_activity.activity["get_multi"](db)
    return activities


@router.post("", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity_in: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new activity"""
    activity = crud_activity.activity["create"](
        db, obj_in=activity_in, host_user_id=current_user.id
    )
    return activity


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: str, db: Session = Depends(get_db)):
    """Get activity details"""
    activity = crud_activity.activity["get"](db, id=activity_id)
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