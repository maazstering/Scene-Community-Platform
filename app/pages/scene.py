import reflex as rx
from app.states.scene_state import SceneState
from app.components.scene_layout import scene_layout
from app.components.activities import activity_card
from app.pages.activity_detail import activity_detail_page
from app.pages.event_detail import event_detail_page


def section_header(title: str, subtitle: str) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-xl font-bold text-white"),
        rx.el.p(subtitle, class_name="text-sm text-gray-400"),
        class_name="mb-4 px-6 md:px-0",
    )


def for_you_people_card(user: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(src=user["avatar"], class_name="h-16 w-16 rounded-full"),
            rx.el.div(
                rx.el.h4(user["name"], class_name="font-semibold text-white"),
                rx.el.p(
                    f"{user['vouches_count']} vouches",
                    class_name="text-sm text-gray-400",
                ),
                class_name="ml-4",
            ),
            class_name="flex items-center",
        ),
        rx.el.div(
            rx.el.button(
                "Shortlist", class_name="px-3 py-1 text-xs bg-gray-700 rounded-md"
            ),
            rx.el.button(
                "Request to play", class_name="px-3 py-1 text-xs bg-teal-500 rounded-md"
            ),
            class_name="flex gap-2 mt-3",
        ),
        class_name="bg-gray-800/50 p-4 rounded-xl border border-gray-700 w-64 flex-shrink-0",
    )


def join_intent_card(intent: dict) -> rx.Component:
    user = SceneState.users[intent["user_id"]]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(src=user["avatar"], class_name="h-10 w-10 rounded-full"),
                rx.el.div(
                    rx.el.h4(user["name"], class_name="font-semibold text-white"),
                    rx.el.p(
                        f"{user['vouches_count']} vouches",
                        class_name="text-xs text-gray-400",
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                "Invite to event", class_name="px-3 py-1 text-xs bg-teal-500 rounded-md"
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.p(
                f"Wants to join: {intent['intent_type']} {intent['when']}",
                class_name="font-semibold text-white mt-3",
            ),
            rx.el.p(
                f"Within {intent['radius_km']}km of {intent['city']}",
                class_name="text-sm text-gray-400",
            ),
            class_name="mt-2",
        ),
        rx.el.div(
            rx.foreach(
                intent["vibe_tags"],
                lambda tag: rx.el.span(
                    tag, class_name="px-2 py-1 bg-gray-700 text-xs rounded-full"
                ),
            ),
            rx.el.span(
                intent["party_size"],
                class_name="px-2 py-1 bg-gray-700 text-xs rounded-full",
            ),
            rx.el.span(
                intent["budget"],
                class_name="px-2 py-1 bg-purple-500/20 text-purple-400 text-xs rounded-full",
            ),
            class_name="flex gap-2 mt-3 flex-wrap",
        ),
        class_name="bg-gray-800/50 p-4 rounded-xl border border-gray-700 w-full",
    )


def home_dashboard() -> rx.Component:
    return rx.el.div(
        section_header("For You — People", "Activity partners matched to you"),
        rx.el.div(
            rx.foreach(SceneState.users.values(), for_you_people_card),
            class_name="flex gap-4 overflow-x-auto p-4 -m-4 mb-8",
        ),
        rx.el.div(
            section_header(
                "Open-to-Join — People", "People looking to join activities and events"
            ),
            rx.el.button(
                "I'm free to join",
                class_name="text-sm bg-teal-500/80 px-3 py-1 rounded-md mb-4 ml-6 md:ml-0",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.div(
            rx.foreach(SceneState.join_intents.values(), join_intent_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 px-6 md:px-0 mb-8",
        ),
        section_header(
            "Public Activities", "Open activity posts you can request to join"
        ),
        activities_dashboard(),
        class_name="max-w-6xl mx-auto py-8",
    )


def activities_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Activities", class_name="text-2xl font-bold text-white"),
            rx.el.p(
                "Find and join activities hosted by the community.",
                class_name="text-gray-400 mt-1",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.foreach(SceneState.filtered_activities, activity_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 px-6 md:px-0",
        ),
    )


def venues_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Venues Dashboard", class_name="text-2xl font-bold text-white mb-6"),
        rx.el.p("Discover and book venues.", class_name="text-gray-400"),
        class_name="p-6",
    )


from app.pages.profile import profile_dashboard


def scene() -> rx.Component:
    return scene_layout(
        rx.match(
            SceneState.current_page,
            ("home", home_dashboard()),
            ("activities", activities_dashboard()),
            ("venues", venues_dashboard()),
            ("profile", profile_dashboard()),
            ("activity_detail", activity_detail_page()),
            ("event_detail", event_detail_page()),
            home_dashboard(),
        )
    )