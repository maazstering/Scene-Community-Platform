from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Integer,
    Boolean,
    Enum,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


class ActivityStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"


class VisibilityScope(str, enum.Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    CIRCLES = "circles"
    INVITE_ONLY = "invite_only"


class ActivityType(Base):
    __tablename__ = "activity_types"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False)
    icon = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    activities = relationship("Activity", back_populates="activity_type")


class Activity(Base):
    __tablename__ = "activities"
    id = Column(String, primary_key=True, default=generate_uuid)
    host_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    activity_type_id = Column(String, ForeignKey("activity_types.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    datetime_start = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer)
    location_text = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    capacity = Column(Integer, nullable=False)
    current_participants = Column(Integer, default=1)
    visibility_scope = Column(Enum(VisibilityScope), default=VisibilityScope.PUBLIC)
    circle_scope_id = Column(String, ForeignKey("circles.id"))
    allow_waitlist = Column(Boolean, default=True)
    status = Column(Enum(ActivityStatus), default=ActivityStatus.OPEN)
    share_slug = Column(String(100), unique=True, index=True)
    og_image_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    host = relationship("User", back_populates="hosted_activities")
    activity_type = relationship("ActivityType", back_populates="activities")
    requests = relationship("ActivityRequest", back_populates="activity")
    circle_scope = relationship("Circle")


class ActivityRequest(Base):
    __tablename__ = "activity_requests"
    id = Column(String, primary_key=True, default=generate_uuid)
    activity_id = Column(String, ForeignKey("activities.id"), nullable=False)
    requester_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    note = Column(Text)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    decided_by_user_id = Column(String, ForeignKey("users.id"))
    decided_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    activity = relationship("Activity", back_populates="requests")
    requester = relationship(
        "User",
        foreign_keys=[requester_user_id],
        back_populates="made_activity_requests",
    )
    decided_by = relationship("User", foreign_keys=[decided_by_user_id])