from sqlalchemy import Column, String, Text, DateTime, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


class NotificationType(str, enum.Enum):
    ACTIVITY_REQUEST = "activity_request"
    REQUEST_APPROVED = "request_approved"
    REQUEST_REJECTED = "request_rejected"
    NEW_VOUCH = "new_vouch"
    EVENT_REMINDER = "event_reminder"
    BOOKING_CONFIRMED = "booking_confirmed"
    CIRCLE_INVITATION = "circle_invitation"


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(200))
    message = Column(Text)
    payload = Column(JSON)
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="notifications")