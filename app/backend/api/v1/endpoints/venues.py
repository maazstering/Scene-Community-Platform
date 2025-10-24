from fastapi import APIRouter, HTTPException
from app.backend.schemas.venue import VenueResponse, VenueSlotResponse

router = APIRouter()


@router.get("", response_model=list[VenueResponse])
async def get_venues():
    """List all venues"""
    return []


@router.get("/{venue_id}", response_model=VenueResponse)
async def get_venue(venue_id: str):
    """Get venue details"""
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{venue_id}/slots", response_model=list[VenueSlotResponse])
async def get_venue_slots(venue_id: str):
    """Get available slots for a venue"""
    return []