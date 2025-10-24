import random
from datetime import datetime, timedelta

random.seed(42)


def get_demo_users():
    """Generates 20 deterministic demo users from Pakistan."""
    names = [
        ("Ahmed", "Khan"),
        ("Fatima", "Ali"),
        ("Usman", "Tariq"),
        ("Ayesha", "Malik"),
        ("Bilal", "Hussain"),
        ("Sana", "Rizvi"),
        ("Imran", "Sheikh"),
        ("Zainab", "Butt"),
        ("Ali", "Raza"),
        ("Hina", "Javed"),
        ("Saad", "Anwar"),
        ("Maria", "Qureshi"),
        ("Faisal", "Mirza"),
        ("Nida", "Yasir"),
        ("Kamran", "Akmal"),
        ("Rabia", "Mughal"),
        ("Adnan", "Siddiqui"),
        ("Saba", "Qamar"),
        ("Haris", "Sohail"),
        ("Mahira", "Khan"),
    ]
    cities = ["Karachi", "Lahore", "Islamabad"]
    activities = ["paddle", "cricket", "tt", "hiking", "food", "gaming", "art"]
    circles = ["Uni", "Work", "Family", "Gym"]
    users = []
    for i, (first, last) in enumerate(names):
        user_id = f"user_{i + 1}"
        users.append(
            {
                "id": user_id,
                "name": f"{first} {last}",
                "avatar": f"https://api.dicebear.com/9.x/notionists/svg?seed={first.lower()}{i}",
                "city": random.choice(cities),
                "activities": random.sample(activities, k=random.randint(2, 4)),
                "vouches_count": random.randint(0, 25),
                "circles": random.sample(circles, k=random.randint(1, 2)),
            }
        )
    return users


def get_demo_venues():
    """Generates 6 deterministic demo venues."""
    return [
        {
            "id": "venue_1",
            "name": "Nishter Park Paddle Courts",
            "activity_types": ["paddle", "tennis"],
            "rating": 4.8,
            "price_band": "$$",
            "distance_km": 2.5,
            "amenities": ["lights", "cafe", "parking"],
            "next_slots": [
                (datetime.now() + timedelta(hours=i)).isoformat() for i in range(2, 6)
            ],
        },
        {
            "id": "venue_2",
            "name": "Model Town Cricket Ground",
            "activity_types": ["cricket"],
            "rating": 4.5,
            "price_band": "$$$",
            "distance_km": 5.1,
            "amenities": ["nets", "pavilion", "parking"],
            "next_slots": [
                (datetime.now() + timedelta(days=1, hours=i)).isoformat()
                for i in range(14, 18)
            ],
        },
        {
            "id": "venue_3",
            "name": "Saddar Table Tennis Club",
            "activity_types": ["tt"],
            "rating": 4.2,
            "price_band": "$",
            "distance_km": 1.2,
            "amenities": ["AC", "coaching"],
            "next_slots": [
                (datetime.now() + timedelta(hours=i)).isoformat() for i in [1, 3, 4]
            ],
        },
        {
            "id": "venue_4",
            "name": "F-9 Park Padel Courts",
            "activity_types": ["paddle"],
            "rating": 4.9,
            "price_band": "$$$",
            "distance_km": 8.3,
            "amenities": ["pro-shop", "juice-bar", "lockers"],
            "next_slots": [
                (datetime.now() + timedelta(days=2, hours=i)).isoformat()
                for i in range(17, 21)
            ],
        },
        {
            "id": "venue_5",
            "name": "DHA Phase 6 Futsal",
            "activity_types": ["football"],
            "rating": 4.6,
            "price_band": "$$",
            "distance_km": 4.5,
            "amenities": ["turf", "lights", "bibs"],
            "next_slots": [
                (datetime.now() + timedelta(hours=i)).isoformat() for i in range(19, 23)
            ],
        },
        {
            "id": "venue_6",
            "name": "Lahore Gymkhana Golf Club",
            "activity_types": ["golf"],
            "rating": 4.7,
            "price_band": "$$$",
            "distance_km": 6.8,
            "amenities": ["caddies", "restaurant", "pro-shop"],
            "next_slots": [
                (datetime.now() + timedelta(days=3, hours=i)).isoformat()
                for i in range(8, 12)
            ],
        },
    ]


def get_demo_activities():
    """Generates 12 deterministic demo activities."""
    titles = [
        "Morning Cricket Match",
        "Evening Paddle Session",
        "Hike to Trail 5",
        "Food walk in Anarkali",
        "Competitive TT Tournament",
        "Weekend Long Drive",
        "Photography session at Badshahi Mosque",
        "Open Mic Night",
        "Beach Cleanup Drive",
        "Casual Football Game",
        "Art Gallery Visit",
        "Board Games Cafe Meetup",
    ]
    types = [
        "cricket",
        "paddle",
        "hiking",
        "food",
        "tt",
        "driving",
        "photography",
        "music",
        "community",
        "football",
        "art",
        "gaming",
    ]
    visibilities = [
        "Public",
        "Public",
        "Public",
        "Circles",
        "Public",
        "Friends",
        "Public",
        "Public",
        "InviteOnly",
        "Public",
        "Circles",
        "Public",
    ]
    activities = []
    for i in range(12):
        start_time = datetime.now() + timedelta(
            days=random.randint(1, 10), hours=random.randint(1, 12)
        )
        capacity = random.choice([4, 6, 8, 10, 12])
        host_id = f"user_{random.randint(1, 20)}"
        visibility = visibilities[i % len(visibilities)]
        activities.append(
            {
                "id": f"activity_{i + 1}",
                "host_user_id": host_id,
                "activity_type": types[i % len(types)],
                "title": titles[i % len(titles)],
                "description": f"Join {host_id} for a fun and exciting session. All skill levels welcome!",
                "datetime_start": start_time.isoformat(),
                "duration": random.choice([60, 90, 120]),
                "location_text": f"{random.choice(['Clifton', 'Gulberg', 'F-10 Markaz'])}, {random.choice(['Karachi', 'Lahore', 'Islamabad'])}",
                "lat": 33.6844 + (random.random() - 0.5) * 0.1,
                "lon": 73.0479 + (random.random() - 0.5) * 0.1,
                "capacity": capacity,
                "current_participants": random.randint(1, capacity - 1),
                "visibility": visibility,
                "circle_scope": "Uni" if visibility == "Circles" else None,
                "share_slug": f"activity-slug-{i + 1}",
            }
        )
    return activities


def get_demo_events():
    """Generates 4 deterministic demo events."""
    return [
        {
            "id": "event_1",
            "host_user_id": "user_5",
            "title": "Startup Summit 2024",
            "description": "The premier event for tech entrepreneurs in Pakistan.",
            "start_time": (datetime.now() + timedelta(days=30)).isoformat(),
            "venue_name": "Expo Center Lahore",
            "city": "Lahore",
            "capacity": 500,
            "spots_taken": 150,
            "visibility": "Public",
            "ticketed": True,
            "ticket_price_pkr": 2500,
            "share_slug": "startup-summit-24",
        },
        {
            "id": "event_2",
            "host_user_id": "user_12",
            "title": "Coke Food Festival",
            "description": "A celebration of food and music.",
            "start_time": (datetime.now() + timedelta(days=15)).isoformat(),
            "venue_name": "Beach Park",
            "city": "Karachi",
            "capacity": 2000,
            "spots_taken": 800,
            "visibility": "Public",
            "ticketed": True,
            "ticket_price_pkr": 1000,
            "share_slug": "coke-food-fest-khi",
        },
        {
            "id": "event_3",
            "host_user_id": "user_8",
            "title": "Exclusive Rooftop Concert",
            "description": "An intimate acoustic night under the stars.",
            "start_time": (datetime.now() + timedelta(days=7)).isoformat(),
            "venue_name": "Avari Towers Rooftop",
            "city": "Islamabad",
            "capacity": 50,
            "spots_taken": 45,
            "visibility": "InviteOnly",
            "ticketed": True,
            "ticket_price_pkr": 5000,
            "share_slug": "rooftop-acoustic-exclusive",
        },
        {
            "id": "event_4",
            "host_user_id": "user_18",
            "title": "Community Book Swap",
            "description": "Bring a book, take a book. Meet fellow readers.",
            "start_time": (datetime.now() + timedelta(days=5)).isoformat(),
            "venue_name": "The Last Word",
            "city": "Lahore",
            "capacity": 100,
            "spots_taken": 30,
            "visibility": "Public",
            "ticketed": False,
            "share_slug": "lahore-book-swap",
        },
    ]


def get_demo_join_intents():
    """Generates 10 deterministic demo join intents."""
    intents = []
    intent_types = [
        "Party",
        "Live music",
        "Paddle tourney",
        "Movie night",
        "Food crawl",
    ]
    when_options = ["Tonight", "This weekend", "Today"]
    party_sizes = ["Solo", "+1", "Group of 3"]
    vibe_tags_options = [
        ["chill", "rooftop"],
        ["club", "cosplay"],
        ["sports"],
        ["cinema"],
        ["streetfood"],
    ]
    budget_options = ["Free", "Under PKR 2k", "Premium"]
    for i in range(10):
        user_id = f"user_{random.randint(1, 20)}"
        intent_type = intent_types[i % len(intent_types)]
        intents.append(
            {
                "id": f"intent_{i + 1}",
                "user_id": user_id,
                "intent_type": intent_type,
                "activities": [intent_type.lower().split()[0]],
                "when": random.choice(when_options),
                "city": random.choice(["Karachi", "Lahore", "Islamabad"]),
                "radius_km": random.choice([5, 10, 15]),
                "party_size": random.choice(party_sizes),
                "vibe_tags": random.choice(vibe_tags_options),
                "budget": random.choice(budget_options),
                "created_at": (datetime.now() - timedelta(hours=i)).isoformat(),
            }
        )
    return intents


def get_demo_circles():
    """Generates deterministic demo circles."""
    return [
        {
            "id": "circle_1",
            "owner_user_id": "user_1",
            "name": "Karachi Paddle Club",
            "member_ids": [f"user_{i}" for i in [1, 3, 5, 7, 9]],
        },
        {
            "id": "circle_2",
            "owner_user_id": "user_2",
            "name": "LUMS Alumni",
            "member_ids": [f"user_{i}" for i in [2, 4, 6, 8, 10]],
        },
        {
            "id": "circle_3",
            "owner_user_id": "user_11",
            "name": "Islamabad Hikers",
            "member_ids": [f"user_{i}" for i in [11, 13, 15, 17, 19]],
        },
        {
            "id": "circle_4",
            "owner_user_id": "user_14",
            "name": "Foodies of Lahore",
            "member_ids": [f"user_{i}" for i in [12, 14, 16, 18, 20]],
        },
    ]