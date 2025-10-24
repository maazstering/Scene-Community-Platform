from fastapi import APIRouter
from app.backend.api.v1.endpoints import (
    auth,
    users,
    activities,
    events,
    venues,
    vouches,
    circles,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(venues.router, prefix="/venues", tags=["venues"])
api_router.include_router(vouches.router, prefix="/vouches", tags=["vouches"])
api_router.include_router(circles.router, prefix="/circles", tags=["circles"])