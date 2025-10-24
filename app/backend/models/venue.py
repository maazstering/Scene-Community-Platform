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
    JSON,
    Numeric,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


class VenueAvailability(str, enum.Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    BLOCKED = "blocked"


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class Venue(Base):
    __tablename__ = "venues"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    address = Column(Text, nullable=False)
    city = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float, default=0.0)
    price_band = Column(String(10))
    amenities = Column(JSON)
    rules = Column(Text)
    hourly_rate_pkr = Column(Numeric(10, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    slots = relationship("VenueSlot", back_populates="venue")
    bookings = relationship("VenueBooking", back_populates="venue")


class VenueSlot(Base):
    __tablename__ = "venue_slots"
    id = Column(String, primary_key=True, default=generate_uuid)
    venue_id = Column(String, ForeignKey("venues.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    price_pkr = Column(Numeric(10, 2), nullable=False)
    availability = Column(Enum(VenueAvailability), default=VenueAvailability.AVAILABLE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    venue = relationship("Venue", back_populates="slots")
    bookings = relationship("VenueBooking", back_populates="slot")


class VenueBooking(Base):
    __tablename__ = "venue_bookings"
    id = Column(String, primary_key=True, default=generate_uuid)
    venue_id = Column(String, ForeignKey("venues.id"), nullable=False)
    slot_id = Column(String, ForeignKey("venue_slots.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    participants_count = Column(Integer, nullable=False)
    total_amount_pkr = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    booking_reference = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    venue = relationship("Venue", back_populates="bookings")
    slot = relationship("VenueSlot", back_populates="bookings")
    user = relationship("User", back_populates="venue_bookings")