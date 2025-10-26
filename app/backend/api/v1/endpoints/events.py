from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.backend.api.deps import get_current_active_user
from app.backend.schemas.event import EventResponse, EventCreate
from app.backend.models.user import User
from app.backend.data.memory_store import memory_store

router = APIRouter()


@router.get("", response_model=list[dict])
async def get_events(host_id: Optional[str] = None, status: Optional[str] = None):
    """List all events"""
    events = memory_store.get_events()
    if host_id == "me":
        return [e for e in events if e["host_user_id"] == "user_1"]
    if status:
        return events
    return events


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    event_in: EventCreate, current_user: dict = Depends(get_current_active_user)
):
    """Create a new event"""
    event = memory_store.create_event(
        event_in=event_in, host_user_id=current_user["id"]
    )
    return event


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    """Get event details"""
    event = memory_store.get_event_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{event_id}/requests", response_model=dict, status_code=201)
async def request_to_join_event(
    event_id: str, current_user: User = Depends(get_current_active_user)
):
    """Request to join an event"""
    raise HTTPException(status_code=501, detail="Not implemented")