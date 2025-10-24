from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    avatar_url = Column(Text)
    city = Column(String(100))
    bio = Column(Text)
    verified_flag = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    given_vouches = relationship(
        "Vouch", foreign_keys="Vouch.giver_user_id", back_populates="giver"
    )
    received_vouches = relationship(
        "Vouch", foreign_keys="Vouch.receiver_user_id", back_populates="receiver"
    )
    hosted_activities = relationship("Activity", back_populates="host")
    activity_requests = relationship("ActivityRequest", back_populates="requester")
    hosted_events = relationship("Event", back_populates="host")
    orders = relationship("Order", back_populates="user")
    venue_bookings = relationship("VenueBooking", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    owned_circles = relationship("Circle", back_populates="owner")
    circle_memberships = relationship("CircleMember", back_populates="user")


class UserActivityPreference(Base):
    __tablename__ = "user_activity_preferences"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    activity_type_id = Column(String, ForeignKey("activity_types.id"), nullable=False)
    skill_level = Column(String(20), default="beginner")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User")
    activity_type = relationship("ActivityType")