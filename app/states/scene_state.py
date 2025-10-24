import reflex as rx
from typing import Optional, TypedDict
from datetime import datetime
from enum import Enum
from app.data import seed


class JoinIntent(TypedDict):
    id: str
    user_id: str
    intent_type: str
    activities: list[str]
    when: str
    city: str
    radius_km: int
    party_size: str
    vibe_tags: list[str]
    budget: str
    created_at: str


class VisibilityScope(str, Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    CIRCLES = "circles"
    INVITE_ONLY = "invite_only"


class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"


class OrderStatus(str, Enum):
    CREATED = "created"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    FAILED = "failed"
    REFUNDED = "refunded"


class VenueAvailability(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    BLOCKED = "blocked"


class GeoPoint(TypedDict):
    lat: float
    lng: float


class Activity(TypedDict):
    id: str
    host_user_id: str
    activity_type: str
    title: str
    description: str
    datetime_start: str
    duration: int
    location_text: str
    geo_point: GeoPoint
    capacity: int
    current_participants: int
    visibility_scope: str
    status: str
    share_slug: str
    created_at: str


import uuid
import secrets


class SceneState(rx.State):
    """Main state for Scene - Production-ready social app for Pakistan"""

    current_user_id: str = "user_1"
    is_authenticated: bool = True
    users: dict[str, dict] = {}
    venues: dict[str, dict] = {}
    activities: dict[str, dict] = {}
    events: dict[str, dict] = {}
    join_intents: dict[str, JoinIntent] = {}
    circles: dict[str, dict] = {}
    user_vouches: dict[str, list[dict]] = {}
    activity_requests: dict[str, list[dict]] = {}
    join_requests: list[dict] = []
    invitations: dict[str, list[dict]] = {}
    event_tickets: dict[str, list[dict]] = {}
    venue_slots: dict[str, list[dict]] = {}
    venue_bookings: dict[str, list[dict]] = {}
    circle_members: dict[str, list[str]] = {}
    orders: dict[str, dict] = {}
    payment_providers: list[str] = ["payfast", "jazzcash", "easypaisa", "pay_at_venue"]
    notifications: dict[str, list[dict]] = {}
    current_page: str = "home"
    loading: bool = False
    error_message: str = ""
    success_message: str = ""
    activity_filters: dict[str, str] = {
        "activity_type": "",
        "date_range": "",
        "radius_km": "10",
        "min_vouches": "0",
        "visibility": "public",
    }
    selected_activity_filter: str = ""
    radius_km: int = 5
    activity_posts: dict[str, dict] = {}
    selected_activity_id: str = ""
    selected_event_id: str = ""
    show_join_request_modal: bool = False
    join_request_note: str = ""
    show_request_modal: bool = False
    selected_activity_for_request: str = ""
    selected_event_for_request: str = ""
    request_note_input: str = ""

    @rx.event
    def on_load(self):
        self._load_demo_data()
        if not self.current_user_id:
            self.current_user_id = "user_1"

    @rx.event
    def on_load_detail(self):
        self._load_demo_data()
        activity_id = self.router.page.params.get("activity_id", "")
        event_id = self.router.page.params.get("event_id", "")
        if activity_id:
            self.selected_activity_id = activity_id
            self.current_page = "activity_detail"
        elif event_id:
            self.selected_event_id = event_id
            self.current_page = "event_detail"
        else:
            return rx.redirect("/scene")

    def _load_demo_data(self):
        """Initialize with Pakistan-focused demo data from seed file"""
        if self.users:
            return
        self.users = {u["id"]: u for u in seed.get_demo_users()}
        self.venues = {v["id"]: v for v in seed.get_demo_venues()}
        self.activities = {a["id"]: a for a in seed.get_demo_activities()}
        self.events = {e["id"]: e for e in seed.get_demo_events()}
        self.circles = {c["id"]: c for c in seed.get_demo_circles()}
        self.join_intents = {ji["id"]: ji for ji in seed.get_demo_join_intents()}
        self.activity_posts = self.activities

    @rx.var
    def current_user(self) -> dict:
        """Get current authenticated user"""
        if self.current_user_id and self.current_user_id in self.users:
            user = self.users[self.current_user_id]
            if "avatar" not in user:
                user["avatar"] = (
                    f"https://api.dicebear.com/9.x/notionists/svg?seed={user['name'].lower().replace(' ', '')}"
                )
            return user
        return {}

    @rx.var
    def user_vouch_count(self) -> int:
        """Get vouch count for current user"""
        user = self.current_user
        if user:
            return user.get("vouches_count", 0)
        return 0

    @rx.var
    def filtered_activities(self) -> list[Activity]:
        """Get filtered activity posts"""
        activities = self.list_public_activities()
        if self.selected_activity_filter:
            activities = [
                a
                for a in activities
                if a["activity_type"] == self.selected_activity_filter
            ]
        if self.activity_filters["activity_type"]:
            activities = [
                a
                for a in activities
                if a.get("activity_type") == self.activity_filters["activity_type"]
            ]
        if self.activity_filters["visibility"]:
            activities = [
                a
                for a in activities
                if a.get("visibility", "").lower()
                == self.activity_filters["visibility"].lower()
            ]
        activities.sort(key=lambda x: x.get("datetime_start", ""), reverse=False)
        return activities

    @rx.event
    def list_public_activities(self) -> list[dict]:
        return [a for a in self.activities.values() if a["visibility"] == "Public"]

    @rx.event
    def find_user_by_email(self, email: str) -> dict | None:
        return None

    @rx.event
    def list_places_by_activity(self, activity: str) -> list[dict]:
        return [v for v in self.venues.values() if activity in v["activity_types"]]

    @rx.event
    def get_activity_by_id(self, activity_id: str) -> dict | None:
        return self.activities.get(activity_id)

    @rx.event
    def get_event_by_id(self, event_id: str) -> dict | None:
        return self.events.get(event_id)

    @rx.var
    def selected_activity(self) -> dict:
        return self.activities.get(self.selected_activity_id, {})

    @rx.var
    def selected_event(self) -> dict:
        return self.events.get(self.selected_event_id, {})

    @rx.var
    def selected_activity_host(self) -> dict:
        activity = self.selected_activity
        if activity and activity.get("host_user_id"):
            return self.users.get(activity["host_user_id"], {})
        return {}

    @rx.var
    def selected_event_host(self) -> dict:
        event = self.selected_event
        if event and event.get("host_user_id"):
            return self.users.get(event["host_user_id"], {})
        return {}

    @rx.var
    def selected_activity_time(self) -> str:
        activity = self.selected_activity
        dt_start = activity.get("datetime_start", "")
        duration = activity.get("duration", 0)
        if not dt_start:
            return ""
        return f"{dt_start[:16].replace('T', ' ')} ({duration} mins)"

    @rx.var
    def selected_event_time(self) -> str:
        event = self.selected_event
        dt_start = event.get("start_time", "")
        if not dt_start:
            return ""
        return f"{dt_start[:16].replace('T', ' ')}"

    @rx.var
    def selected_activity_capacity_percentage(self) -> str:
        activity = self.selected_activity
        current = activity.get("current_participants", 0)
        total = activity.get("capacity", 1)
        if total == 0:
            return "0%"
        return f"{current / total * 100}%"

    @rx.var
    def selected_event_capacity_percentage(self) -> str:
        event = self.selected_event
        current = event.get("spots_taken", 0)
        total = event.get("capacity", 1)
        if total == 0:
            return "0%"
        return f"{current / total * 100}%"

    @rx.var
    def activity_types(self) -> list[str]:
        """Get available activity types"""
        return sorted(list(set((a["activity_type"] for a in self.activities.values()))))

    @rx.var
    def selected_activity_for_request_details(self) -> dict | None:
        return self.activities.get(self.selected_activity_for_request)

    @rx.var
    def selected_event_for_request_details(self) -> dict | None:
        return self.events.get(self.selected_event_for_request)

    @rx.event
    def set_current_user_id(self, user_id: str):
        self.current_user_id = user_id

    @rx.event
    def set_current_page(self, page: str):
        """Navigate to different pages"""
        self.current_page = page

    @rx.event
    def set_activity_filter(self, filter_type: str, value: str):
        """Update activity filters"""
        if filter_type == "selected_activity_filter":
            self.selected_activity_filter = value
        else:
            self.activity_filters[filter_type] = value

    @rx.event
    def clear_filters(self):
        """Clear all activity filters"""
        self.activity_filters = {
            "activity_type": "",
            "date_range": "",
            "radius_km": "10",
            "min_vouches": "0",
            "visibility": "public",
        }

    @rx.event
    def create_activity_post(self, form_data: dict):
        """Create a new activity post"""
        activity_id = f"activity_{len(self.activity_posts) + 1}"
        new_activity = {
            "id": activity_id,
            "host_user_id": self.current_user_id,
            "activity_type": form_data.get("activity_type", ""),
            "title": form_data.get("title", ""),
            "description": form_data.get("description", ""),
            "datetime_start": form_data.get("datetime_start", ""),
            "duration": int(form_data.get("duration", 60)),
            "location_text": form_data.get("location_text", ""),
            "capacity": int(form_data.get("capacity", 5)),
            "current_participants": 1,
            "visibility_scope": form_data.get(
                "visibility_scope", VisibilityScope.PUBLIC
            ),
            "status": "open",
            "share_slug": f"{form_data.get('title', '').lower().replace(' ', '-')}-{activity_id}",
            "created_at": datetime.now().isoformat(),
        }
        self.activity_posts[activity_id] = new_activity
        self.activities[activity_id] = new_activity
        self.success_message = (
            f"Activity '{new_activity['title']}' created successfully!"
        )

    @rx.event
    def set_selected_activity_id(self, activity_id: str):
        self.selected_activity_id = activity_id

    @rx.event
    def set_selected_event_id(self, event_id: str):
        self.selected_event_id = event_id

    @rx.event
    def create_join_request(self, request_type: str, target_id: str, note: str):
        """Create a join request for an activity or event."""
        request_id = str(uuid.uuid4())
        requester_id = self.current_user_id
        if any(
            (
                r["target_id"] == target_id and r["requester_user_id"] == requester_id
                for r in self.join_requests
            )
        ):
            self.error_message = "You have already sent a request."
            return
        new_request = {
            "id": request_id,
            "request_type": request_type,
            "target_id": target_id,
            "requester_user_id": requester_id,
            "note": note,
            "status": RequestStatus.PENDING,
            "created_at": datetime.now().isoformat(),
        }
        target = None
        if request_type == "activity":
            target = self.activities.get(target_id)
        elif request_type == "event":
            target = self.events.get(target_id)
        if target:
            is_public = target.get("visibility") == "Public"
            if is_public:
                if target.get("current_participants", 0) < target.get("capacity", 0):
                    new_request["status"] = RequestStatus.APPROVED
                    if request_type == "activity":
                        self.activities[target_id]["current_participants"] += 1
                    self.success_message = "Request approved and you have been added!"
                else:
                    new_request["status"] = RequestStatus.WAITLISTED
                    self.success_message = (
                        "This is full, but you have been added to the waitlist."
                    )
            else:
                self.success_message = "Request sent to host for approval."
        self.join_requests.append(new_request)

    @rx.event
    def open_request_modal(self, item_type: str, item_id: str):
        if item_type == "activity":
            self.selected_activity_for_request = item_id
        else:
            self.selected_event_for_request = item_id
        self.show_request_modal = True

    @rx.event
    def close_request_modal(self):
        self.show_request_modal = False
        self.request_note_input = ""
        self.selected_activity_for_request = ""
        self.selected_event_for_request = ""

    @rx.event
    def submit_join_request(self):
        item_type = "activity" if self.selected_activity_for_request else "event"
        item_id = self.selected_activity_for_request or self.selected_event_for_request
        note = self.request_note_input
        self.close_request_modal()
        return SceneState.create_join_request(item_type, item_id, note)

    @rx.event
    def join_activity_request(self, activity_id: str, note: str = ""):
        """Request to join an activity"""
        if activity_id not in self.activity_requests:
            self.activity_requests[activity_id] = []
        existing_request = any(
            (
                req["requester_user_id"] == self.current_user_id
                for req in self.activity_requests[activity_id]
            )
        )
        if existing_request:
            self.error_message = "You have already requested to join this activity"
            return
        request_id = f"req_{len(self.activity_requests[activity_id]) + 1}"
        new_request = {
            "id": request_id,
            "activity_post_id": activity_id,
            "requester_user_id": self.current_user_id,
            "note": note,
            "status": RequestStatus.PENDING,
            "created_at": datetime.now().isoformat(),
        }
        self.activity_requests[activity_id].append(new_request)
        self.success_message = "Join request sent! Waiting for host approval."

    @rx.event
    def approve_activity_request(self, activity_id: str, request_id: str):
        """Approve a join request (host only)"""
        if activity_id not in self.activity_requests:
            return
        activity = self.activity_posts.get(activity_id)
        if not activity or activity["host_user_id"] != self.current_user_id:
            self.error_message = "Only the host can approve requests"
            return
        for request in self.activity_requests[activity_id]:
            if request["id"] == request_id:
                request["status"] = RequestStatus.APPROVED
                request["decided_at"] = datetime.now().isoformat()
                request["decided_by"] = self.current_user_id
                activity["current_participants"] += 1
                self.success_message = "Request approved!"
                break

    @rx.event
    def approve_join_request(self, request_id: str):
        """Approve a pending join request (host only)"""
        for request in self.join_requests:
            if request["id"] == request_id:
                target_id = request["target_id"]
                target = self.activities.get(target_id)
                if not target or target["host_user_id"] != self.current_user_id:
                    self.error_message = "Only the host can approve."
                    return
                if target["current_participants"] < target["capacity"]:
                    request["status"] = RequestStatus.APPROVED
                    target["current_participants"] += 1
                    self.success_message = "Request approved."
                else:
                    request["status"] = RequestStatus.WAITLISTED
                    self.success_message = "Capacity full. User added to waitlist."
                break

    @rx.event
    def reject_join_request(self, request_id: str):
        """Reject a pending join request (host only)"""
        for request in self.join_requests:
            if request["id"] == request_id:
                target_id = request["target_id"]
                target = self.activities.get(target_id)
                if not target or target["host_user_id"] != self.current_user_id:
                    self.error_message = "Only the host can reject."
                    return
                request["status"] = RequestStatus.REJECTED
                self.success_message = "Request rejected."
                break

    @rx.event
    def send_event_invitation(self, event_id: str, user_id: str):
        """Send an invitation to an event."""
        if event_id not in self.invitations:
            self.invitations[event_id] = []
        if any((inv["user_id"] == user_id for inv in self.invitations[event_id])):
            self.error_message = "Invitation already sent to this user."
            return
        new_invitation = {
            "id": str(uuid.uuid4()),
            "event_id": event_id,
            "user_id": user_id,
            "inviter_id": self.current_user_id,
            "status": "sent",
            "created_at": datetime.now().isoformat(),
        }
        self.invitations[event_id].append(new_invitation)
        self.success_message = f"Invitation sent to {self.users[user_id]['name']}!"

    @rx.event
    def create_join_intent(self, form_data: dict):
        """Create an 'I want to join' intent post."""
        intent_id = str(uuid.uuid4())
        new_intent: JoinIntent = {
            "id": intent_id,
            "user_id": self.current_user_id,
            "intent_type": form_data.get("intent_type", ""),
            "activities": form_data.get("activities", []),
            "when": form_data.get("when", ""),
            "city": form_data.get("city", ""),
            "radius_km": int(form_data.get("radius_km", 5)),
            "party_size": form_data.get("party_size", "Solo"),
            "vibe_tags": form_data.get("vibe_tags", []),
            "budget": form_data.get("budget", ""),
            "created_at": datetime.now().isoformat(),
        }
        self.join_intents[intent_id] = new_intent
        self.success_message = "Your join intent has been posted!"

    @rx.event
    def create_vouch(self, user_id: str, text: str):
        """Create a vouch for another user"""
        if user_id == self.current_user_id:
            self.error_message = "You cannot vouch for yourself"
            return
        if user_id not in self.user_vouches:
            self.user_vouches[user_id] = []
        existing_vouch = any(
            (
                vouch["giver_user_id"] == self.current_user_id
                for vouch in self.user_vouches[user_id]
            )
        )
        if existing_vouch:
            self.error_message = "You have already vouched for this user"
            return
        vouch_id = f"vouch_{len(self.user_vouches[user_id]) + 1}"
        new_vouch = {
            "id": vouch_id,
            "giver_user_id": self.current_user_id,
            "receiver_user_id": user_id,
            "text": text,
            "created_at": datetime.now().isoformat(),
        }
        self.user_vouches[user_id].append(new_vouch)
        self.success_message = f"Vouch created for {self.users[user_id]['name']}!"

    @rx.event
    def book_venue_slot(self, venue_id: str, slot_time: str, participants: int):
        """Book a venue slot"""
        venue = self.venues.get(venue_id)
        if not venue:
            self.error_message = "Venue not found"
            return
        booking_id = f"booking_{len(self.venue_bookings.get(venue_id, [])) + 1}"
        new_booking = {
            "id": booking_id,
            "venue_id": venue_id,
            "user_id": self.current_user_id,
            "slot_time": slot_time,
            "participants_count": participants,
            "total_amount": venue["hourly_rate"] * participants,
            "currency": "PKR",
            "status": "confirmed",
            "payment_status": "pending",
            "created_at": datetime.now().isoformat(),
        }
        if venue_id not in self.venue_bookings:
            self.venue_bookings[venue_id] = []
        self.venue_bookings[venue_id].append(new_booking)
        self.success_message = f"Venue booked! Total: PKR {new_booking['total_amount']}"

    @rx.event
    def set_error_message(self, message: str):
        """Set error message"""
        self.error_message = message

    @rx.event
    def set_success_message(self, message: str):
        """Set success message"""
        self.success_message = message

    @rx.event
    def clear_messages(self):
        """Clear all messages"""
        self.error_message = ""
        self.success_message = ""