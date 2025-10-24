from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..models.venue import VenueAvailability, BookingStatus, PaymentStatus


class VenueBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[float] = 0.0
    price_band: Optional[str] = None
    amenities: Optional[dict[str, bool | str | int | float | None]] = None
    rules: Optional[str] = None
    hourly_rate_pkr: Optional[Decimal] = None
    is_active: bool = True


class VenueResponse(VenueBase):
    id: str

    class Config:
        from_attributes = True


class VenueSlotResponse(BaseModel):
    id: str
    venue_id: str
    start_time: datetime
    end_time: datetime
    price_pkr: Decimal
    availability: VenueAvailability

    class Config:
        from_attributes = True


class VenueBookingResponse(BaseModel):
    id: str
    venue_id: str
    slot_id: str
    user_id: str
    participants_count: int
    total_amount_pkr: Decimal
    status: BookingStatus
    payment_status: PaymentStatus

    class Config:
        from_attributes = True