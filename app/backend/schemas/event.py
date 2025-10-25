from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..models.event import EventStatus, VisibilityScope


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    venue_name: str
    address: Optional[str] = None
    city: str
    capacity: Optional[int] = None
    visibility_scope: VisibilityScope = VisibilityScope.PUBLIC
    ticketed: bool = False


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: str
    host_user_id: str
    spots_taken: int
    status: EventStatus
    share_slug: str
    created_at: datetime

    class Config:
        from_attributes = True


class TicketTierResponse(BaseModel):
    id: str
    event_id: str
    name: str
    description: Optional[str] = None
    price_pkr: Decimal
    qty_total: int
    qty_sold: int

    class Config:
        from_attributes = True