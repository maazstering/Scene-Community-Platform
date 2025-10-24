import reflex as rx
from typing import Any
from app.states.scene_state import SceneState
import uuid
import secrets
from datetime import datetime


class WizardState(rx.State):
    show_create_modal: bool = False
    create_type: str = ""
    current_step: int = 0
    form_data: dict[str, str | int] = {}
    ACTIVITY_STEPS = [
        "Details",
        "Time",
        "Location",
        "Capacity",
        "Visibility",
        "Preview",
    ]
    activity_types = [
        "paddle",
        "cricket",
        "tt",
        "hiking",
        "football",
        "food",
        "gaming",
        "art",
    ]
    EVENT_STEPS = [
        "Details",
        "Time & Venue",
        "Capacity",
        "Visibility",
        "Ticketing",
        "Preview",
    ]

    @rx.var
    def wizard_steps(self) -> list[str]:
        return (
            self.ACTIVITY_STEPS if self.create_type == "activity" else self.EVENT_STEPS
        )

    @rx.var
    def is_first_step(self) -> bool:
        return self.current_step == 0

    @rx.var
    def is_last_step(self) -> bool:
        return self.current_step == len(self.wizard_steps) - 1

    @rx.event
    def open_create_modal(self):
        self.show_create_modal = True
        self.current_step = 0
        self.create_type = ""
        self.form_data = {}

    @rx.event
    def close_create_modal(self):
        self.show_create_modal = False

    @rx.event
    def set_create_type(self, create_type: str):
        self.create_type = create_type

    @rx.event
    def next_step(self):
        if not self.is_last_step:
            self.current_step += 1

    @rx.event
    def prev_step(self):
        if not self.is_first_step:
            self.current_step -= 1

    @rx.event
    def update_form_field(self, field_name: str, value: Any):
        self.form_data[field_name] = value

    @rx.event
    async def publish_activity(self):
        scene_state = await self.get_state(SceneState)
        activity_id = str(uuid.uuid4())
        new_activity = {
            "id": activity_id,
            "host_user_id": scene_state.current_user_id,
            "activity_type": self.form_data.get("activity_type", ""),
            "title": self.form_data.get("title", ""),
            "description": self.form_data.get("description", ""),
            "datetime_start": f"{self.form_data.get('date', '')}T{self.form_data.get('start_time', '')}",
            "duration": int(self.form_data.get("duration", 60)),
            "location_text": self.form_data.get("location_text", ""),
            "capacity": int(self.form_data.get("capacity", 2)),
            "current_participants": 1,
            "visibility": self.form_data.get("visibility", "Public"),
            "circle_scope": self.form_data.get("circle_scope")
            if self.form_data.get("visibility") == "Circles"
            else None,
            "share_slug": secrets.token_urlsafe(6),
            "created_at": datetime.now().isoformat(),
        }
        scene_state.activities[activity_id] = new_activity
        scene_state.success_message = (
            f"Activity '{new_activity['title']}' published! Share link copied."
        )
        self.close_create_modal()
        return rx.set_clipboard(f"/a/{new_activity['share_slug']}")

    @rx.event
    async def publish_event(self):
        scene_state = await self.get_state(SceneState)
        event_id = str(uuid.uuid4())
        new_event = {
            "id": event_id,
            "host_user_id": scene_state.current_user_id,
            "title": self.form_data.get("title", ""),
            "description": self.form_data.get("description", ""),
            "start_time": f"{self.form_data.get('date', '')}T{self.form_data.get('start_time', '')}",
            "venue_name": self.form_data.get("venue_name", ""),
            "city": scene_state.venues.get(
                self.form_data.get("venue_name", ""), {}
            ).get("city", ""),
            "capacity": int(self.form_data.get("capacity", 2)),
            "spots_taken": 0,
            "visibility": self.form_data.get("visibility", "Public"),
            "ticketed": self.form_data.get("ticketed", False),
            "ticket_price_pkr": int(self.form_data.get("price_pkr", 0))
            if self.form_data.get("ticketed")
            else None,
            "share_slug": secrets.token_urlsafe(6),
        }
        scene_state.events[event_id] = new_event
        scene_state.success_message = (
            f"Event '{new_event['title']}' published! Share link copied."
        )
        self.close_create_modal()
        return rx.set_clipboard(f"/e/{new_event['share_slug']}")