from app.data import seed
import uuid
from datetime import datetime


class MemoryStore:
    def __init__(self):
        self._users = {u["id"]: u for u in seed.get_demo_users()}
        self._activities = self._transform_activities(seed.get_demo_activities())
        self._events = self._transform_events(seed.get_demo_events())
        self._venues = self._transform_venues(seed.get_demo_venues())
        self._circles = {c["id"]: c for c in seed.get_demo_circles()}
        self._activity_requests = {}

    def _transform_activities(self, activities_data):
        transformed = {}
        for a in activities_data:
            activity_id = a["id"]
            transformed[activity_id] = {
                "id": activity_id,
                "host_user_id": a["host_user_id"],
                "activity_type_id": a["activity_type"],
                "title": a["title"],
                "description": a["description"],
                "datetime_start": a["datetime_start"],
                "duration": a["duration"],
                "location_text": a["location_text"],
                "latitude": a.get("lat"),
                "longitude": a.get("lon"),
                "capacity": a["capacity"],
                "current_participants": a["current_participants"],
                "visibility_scope": a["visibility"].lower(),
                "circle_scope_id": a.get("circle_scope"),
                "allow_waitlist": True,
                "status": "open",
                "share_slug": a["share_slug"],
                "created_at": datetime.now().isoformat(),
            }
        return transformed

    def _transform_events(self, events_data):
        transformed = {}
        for e in events_data:
            event_id = e["id"]
            transformed[event_id] = {
                "id": event_id,
                "host_user_id": e["host_user_id"],
                "title": e["title"],
                "description": e["description"],
                "start_time": e["start_time"],
                "end_time": None,
                "venue_name": e["venue_name"],
                "address": None,
                "city": e["city"],
                "capacity": e["capacity"],
                "spots_taken": e["spots_taken"],
                "visibility_scope": e["visibility"].lower(),
                "ticketed": e["ticketed"],
                "status": "published",
                "share_slug": e["share_slug"],
                "created_at": datetime.now().isoformat(),
            }
        return transformed

    def _transform_venues(self, venues_data):
        transformed = {}
        for v in venues_data:
            venue_id = v["id"]
            transformed[venue_id] = {
                "id": venue_id,
                "name": v["name"],
                "description": f"A great place for {', '.join(v.get('activity_types', []))} in Karachi.",
                "address": v["name"],
                "city": "Karachi",
                "latitude": None,
                "longitude": None,
                "rating": v.get("rating", 4.0),
                "price_band": v.get("price_band"),
                "amenities": {amenity: True for amenity in v.get("amenities", [])},
                "rules": "Be respectful of the space and other members.",
                "hourly_rate_pkr": None,
                "is_active": True,
            }
        return transformed

    def get_users(self):
        return list(self._users.values())

    def get_user_by_id(self, user_id: str):
        return self._users.get(user_id)

    def get_user_by_email(self, email: str):
        for user in self._users.values():
            if user.get("email") == email:
                return user
        return None

    def create_user(self, name: str, email: str):
        new_id = f"user_{len(self._users) + 1}"
        new_user = {
            "id": new_id,
            "name": name,
            "email": email,
            "avatar_url": f"https://api.dicebear.com/9.x/notionists/svg?seed={name.lower().replace(' ', '')}",
            "city": "Karachi",
            "bio": "New to Scene!",
            "vouches_count": 0,
            "activities_count": 0,
            "is_active": True,
            "verified_flag": False,
            "created_at": datetime.utcnow(),
        }
        self._users[new_id] = new_user
        return new_user

    def get_activities(self):
        return [
            {
                **activity,
                "datetime_start": datetime.fromisoformat(activity["datetime_start"]),
                "created_at": datetime.fromisoformat(activity["created_at"]),
            }
            for activity in self._activities.values()
        ]

    def get_activity_by_id(self, activity_id: str):
        return self._activities.get(activity_id)

    def create_activity(self, activity_in, host_user_id):
        activity_id = str(uuid.uuid4())
        new_activity = activity_in.model_dump()
        new_activity["id"] = activity_id
        new_activity["host_user_id"] = host_user_id
        new_activity["current_participants"] = 1
        new_activity["status"] = "open"
        new_activity["share_slug"] = f"activity-slug-{activity_id[:6]}"
        new_activity["created_at"] = datetime.utcnow()
        new_activity["datetime_start"] = activity_in.datetime_start
        storage_activity = new_activity.copy()
        storage_activity["datetime_start"] = new_activity["datetime_start"].isoformat()
        storage_activity["created_at"] = new_activity["created_at"].isoformat()
        self._activities[activity_id] = storage_activity
        new_activity["activity_type"] = self._activities[activity_id].get(
            "activity_type_id"
        )
        return new_activity

    def get_events(self):
        return [
            {
                **event,
                "start_time": datetime.fromisoformat(event["start_time"]),
                "created_at": datetime.fromisoformat(event["created_at"]),
            }
            for event in self._events.values()
        ]

    def get_event_by_id(self, event_id: str):
        return self._events.get(event_id)

    def create_event(self, event_in, host_user_id):
        event_id = str(uuid.uuid4())
        new_event = event_in.model_dump()
        new_event.update(
            {
                "id": event_id,
                "host_user_id": host_user_id,
                "spots_taken": 0,
                "status": "published",
                "share_slug": f"event-slug-{event_id[:6]}",
                "created_at": datetime.utcnow(),
                "start_time": event_in.start_time,
            }
        )
        storage_event = new_event.copy()
        storage_event["start_time"] = new_event["start_time"].isoformat()
        storage_event["created_at"] = new_event["created_at"].isoformat()
        self._events[event_id] = storage_event
        return new_event

    def get_venues(self):
        return list(self._venues.values())

    def get_circles(self):
        return list(self._circles.values())

    def get_circle_by_id(self, circle_id: str):
        return self._circles.get(circle_id)

    def create_circle(self, circle_in, owner_id: str):
        circle_id = str(uuid.uuid4())
        new_circle = circle_in.dict()
        new_circle.update(
            {"id": circle_id, "owner_user_id": owner_id, "member_ids": [owner_id]}
        )
        self._circles[circle_id] = new_circle
        return new_circle


memory_store = MemoryStore()