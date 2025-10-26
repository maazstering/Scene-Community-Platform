import reflex as rx
from typing import Optional
from app.utils.api_client import api_client
from app.states.base_state import BaseState
import logging


class ProfileState(rx.State):
    """State for the user profile dashboard."""

    me: Optional[dict] = None
    vouches_received: list[dict] = []
    vouches_given: list[dict] = []
    circles: list[dict] = []
    my_activities_open: list[dict] = []
    my_activities_past: list[dict] = []
    my_events_upcoming: list[dict] = []
    my_events_past: list[dict] = []
    my_bookings_upcoming: list[dict] = []
    my_bookings_past: list[dict] = []
    loading: bool = True
    vouch_tab: str = "received"
    booking_tab: str = "upcoming"

    @rx.event
    async def on_profile_load(self):
        """Fetch all data for the profile page in parallel."""
        self.loading = True
        base_state = await self.get_state(BaseState)
        if not base_state.is_authenticated:
            yield rx.redirect("/")
            return
        try:
            self.me = await api_client.get(
                "/api/v1/auth/me", token=base_state.access_token
            )
            if not self.me:
                raise Exception("Failed to fetch user profile")
            user_id = self.me["id"]
            self.vouches_received = await api_client.get(
                f"/api/v1/users/{user_id}/vouches",
                token=base_state.access_token,
                params={"direction": "received"},
            )
            self.vouches_given = await api_client.get(
                f"/api/v1/users/{user_id}/vouches",
                token=base_state.access_token,
                params={"direction": "given"},
            )
            self.my_activities_open = await api_client.get(
                "/api/v1/activities",
                token=base_state.access_token,
                params={"host_id": "me", "status": "open"},
            )
            self.my_events_upcoming = await api_client.get(
                "/api/v1/events",
                token=base_state.access_token,
                params={"host_id": "me", "status": "upcoming"},
            )
            self.circles = await api_client.get(
                "/api/v1/circles", token=base_state.access_token
            )
            self.my_bookings_upcoming = []
            self.my_bookings_past = []
        except Exception as e:
            logging.exception(f"Error loading profile data: {e}")
            yield rx.toast.error("Could not load profile data.")
        finally:
            self.loading = False

    @rx.var
    def hosted_items_count(self) -> int:
        return len(self.my_activities_open) + len(self.my_events_upcoming)

    @rx.event
    def set_vouch_tab(self, tab: str):
        self.vouch_tab = tab

    @rx.event
    def set_booking_tab(self, tab: str):
        self.booking_tab = tab