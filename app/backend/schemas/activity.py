from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.activity import ActivityStatus, RequestStatus, VisibilityScope


class ActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    datetime_start: datetime
    duration: int
    location_text: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: int
    visibility_scope: VisibilityScope = VisibilityScope.PUBLIC
    circle_scope_id: Optional[str] = None
    allow_waitlist: bool = True
    banner_url: Optional[str] = None


class ActivityCreate(ActivityBase):
    activity_type_id: str


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    datetime_start: Optional[datetime] = None
    duration: Optional[int] = None
    location_text: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[ActivityStatus] = None


class ActivityResponse(ActivityBase):
    id: str
    host_user_id: str
    current_participants: int
    status: ActivityStatus
    share_slug: str
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityRequestCreate(BaseModel):
    note: Optional[str] = None


class ActivityRequestResponse(BaseModel):
    id: str
    activity_id: str
    requester_user_id: str
    requester_name: str
    requester_avatar_url: Optional[str] = None
    requester_vouches_count: int = 0
    note: Optional[str] = None
    status: RequestStatus
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityRequestUpdate(BaseModel):
    status: RequestStatus
    note: Optional[str] = None


class ActivityTypeResponse(BaseModel):
    id: str
    name: str
    icon: Optional[str] = None

    class Config:
        from_attributes = True