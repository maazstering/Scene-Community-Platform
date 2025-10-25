import reflex as rx
from typing import Any
from app.states.scene_state import SceneState
from app.states.base_state import BaseState
from app.utils.api_client import api_client
import uuid
import secrets
from datetime import datetime
import logging


class WizardState(rx.State):
    show_create_modal: bool = False
    create_type: str = ""
    current_step: int = 0
    form_data: dict[str, str | int | bool] = {}
    is_publishing: bool = False
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
        self.is_publishing = False

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

    async def _upload_file(self, files: list[rx.UploadFile], field_name: str):
        if not files:
            return rx.toast.error("No file selected.")
        file = files[0]
        upload_data = await file.read()
        file_path = rx.get_upload_dir() / file.name
        with file_path.open("wb") as f:
            f.write(upload_data)
        self.form_data[field_name] = file.name
        return rx.toast.success(f"Uploaded {file.name}")

    @rx.event
    async def handle_banner_upload(self, files: list[rx.UploadFile]):
        yield (await self._upload_file(files, "banner_url"))

    @rx.event
    async def handle_poster_upload(self, files: list[rx.UploadFile]):
        yield (await self._upload_file(files, "poster_url"))

    @rx.event
    async def publish_activity(self):
        self.is_publishing = True
        try:
            scene_state = await self.get_state(SceneState)
            base_state = await self.get_state(BaseState)
            datetime_start = f"{self.form_data.get('date', '')}T{self.form_data.get('start_time', '')}:00"
            payload = {
                "activity_type_id": self.form_data.get("activity_type_id", "paddle"),
                "title": self.form_data.get("title", ""),
                "description": self.form_data.get("description", ""),
                "datetime_start": datetime_start,
                "duration": int(self.form_data.get("duration", 60)),
                "location_text": self.form_data.get("location_text", ""),
                "capacity": int(self.form_data.get("capacity", 2)),
                "visibility_scope": self.form_data.get("visibility_scope", "public"),
                "allow_waitlist": bool(self.form_data.get("allow_waitlist", True)),
                "banner_url": self.form_data.get("banner_url"),
            }
            new_activity = await api_client.post(
                "/api/v1/activities", token=base_state.access_token, data=payload
            )
            scene_state.activities[new_activity["id"]] = new_activity
            scene_state.success_message = (
                f"Activity '{new_activity['title']}' published!"
            )
            self.close_create_modal()
            yield rx.redirect(f"/activity/{new_activity['id']}")
            yield rx.set_clipboard(f"/activity/{new_activity['share_slug']}")
            yield rx.toast.success("Share link copied to clipboard!")
        except Exception as e:
            logging.exception(f"Failed to publish activity: {e}")
            yield rx.toast.error("Failed to publish activity. Please check all fields.")
        finally:
            self.is_publishing = False

    @rx.event
    async def publish_event(self):
        self.is_publishing = True
        try:
            scene_state = await self.get_state(SceneState)
            base_state = await self.get_state(BaseState)
            start_time = f"{self.form_data.get('date', '')}T{self.form_data.get('start_time', '')}:00"
            payload = {
                "title": self.form_data.get("title", ""),
                "description": self.form_data.get("description", ""),
                "start_time": start_time,
                "venue_name": self.form_data.get("venue_name", ""),
                "city": self.form_data.get("city", ""),
                "capacity": int(self.form_data.get("capacity", 10)),
                "visibility_scope": self.form_data.get("visibility_scope", "public"),
                "ticketed": bool(self.form_data.get("ticketed", False)),
                "poster_url": self.form_data.get("poster_url"),
            }
            new_event = await api_client.post(
                "/api/v1/events", token=base_state.access_token, data=payload
            )
            scene_state.events[new_event["id"]] = new_event
            scene_state.success_message = f"Event '{new_event['title']}' published!"
            self.close_create_modal()
            yield rx.redirect(f"/event/{new_event['id']}")
            yield rx.set_clipboard(f"/event/{new_event['share_slug']}")
            yield rx.toast.success("Share link copied to clipboard!")
        except Exception as e:
            logging.exception(f"Failed to publish event: {e}")
            yield rx.toast.error("Failed to publish event. Please check all fields.")
        finally:
            self.is_publishing = False