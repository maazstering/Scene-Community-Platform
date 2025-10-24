from fastapi import APIRouter, Depends, HTTPException
from app.backend.schemas.event import EventResponse, EventCreate
from app.backend.api.deps import get_current_active_user
from app.backend.models.user import User

router = APIRouter()


@router.get("", response_model=list[EventResponse])
async def get_events():
    """List all events"""
    return []


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    event: EventCreate, current_user: User = Depends(get_current_active_user)
):
    """Create a new event"""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    """Get event details"""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{event_id}/requests", response_model=dict, status_code=201)
async def request_to_join_event(
    event_id: str, current_user: User = Depends(get_current_active_user)
):
    """Request to join an event"""
    raise HTTPException(status_code=501, detail="Not implemented")