from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Integer,
    Boolean,
    Enum,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"


class OrderStatus(str, enum.Enum):
    CREATED = "created"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    FAILED = "failed"
    REFUNDED = "refunded"


class VisibilityScope(str, enum.Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    CIRCLES = "circles"
    INVITE_ONLY = "invite_only"


class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True, default=generate_uuid)
    host_user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    venue_name = Column(String(200))
    address = Column(Text)
    city = Column(String(100))
    capacity = Column(Integer)
    spots_taken = Column(Integer, default=0)
    visibility_scope = Column(Enum(VisibilityScope), default=VisibilityScope.PUBLIC)
    ticketed = Column(Boolean, default=False)
    status = Column(Enum(EventStatus), default=EventStatus.DRAFT)
    share_slug = Column(String(100), unique=True, index=True)
    og_image_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    host = relationship("User", back_populates="hosted_events")
    ticket_tiers = relationship("TicketTier", back_populates="event")
    orders = relationship("Order", back_populates="event")


class TicketTier(Base):
    __tablename__ = "ticket_tiers"
    id = Column(String, primary_key=True, default=generate_uuid)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price_pkr = Column(Numeric(10, 2), nullable=False)
    qty_total = Column(Integer, nullable=False)
    qty_sold = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    event = relationship("Event", back_populates="ticket_tiers")


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    event_id = Column(String, ForeignKey("events.id"))
    venue_booking_id = Column(String, ForeignKey("venue_bookings.id"))
    amount_pkr = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="PKR")
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED)
    payment_provider = Column(String(50))
    provider_reference = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="orders")
    event = relationship("Event", back_populates="orders")