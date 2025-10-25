from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.backend.api.deps import get_db, get_current_active_user
from app.backend.crud import event as crud_event
from app.backend.schemas.event import EventResponse, EventCreate
from app.backend.models.user import User

router = APIRouter()


@router.get("", response_model=list[EventResponse])
async def get_events(db: Session = Depends(get_db)):
    """List all events"""
    events = crud_event.event["get_multi"](db)
    return events


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new event"""
    event = crud_event.event["create"](
        db, obj_in=event_in, host_user_id=current_user.id
    )
    return event


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str, db: Session = Depends(get_db)):
    """Get event details"""
    event = crud_event.event["get"](db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/{event_id}/requests", response_model=dict, status_code=201)
async def request_to_join_event(
    event_id: str, current_user: User = Depends(get_current_active_user)
):
    """Request to join an event"""
    raise HTTPException(status_code=501, detail="Not implemented")