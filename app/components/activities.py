import reflex as rx
from app.states.scene_state import SceneState


def activity_card(activity: dict) -> rx.Component:
    """Individual activity card with modern design"""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    rx.cond(
                        activity["activity_type"] == "hiking",
                        "mountain",
                        rx.cond(
                            activity["activity_type"] == "food",
                            "utensils",
                            rx.cond(
                                activity["activity_type"] == "football",
                                "football",
                                "calendar",
                            ),
                        ),
                    ),
                    class_name="h-5 w-5 text-teal-400",
                ),
                rx.el.span(
                    activity["activity_type"].title(),
                    class_name="ml-2 text-sm font-medium text-teal-400 capitalize",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.span(
                    f"{activity['current_participants']}/{activity['capacity']}",
                    class_name="px-2 py-1 bg-gray-800 text-gray-300 rounded-lg text-xs font-medium",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.h3(activity["title"], class_name="text-lg font-bold text-white mb-2"),
        rx.el.p(
            activity["description"],
            class_name="text-gray-400 text-sm mb-4 line-clamp-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(
                    activity["location_text"], class_name="ml-1 text-sm text-gray-400"
                ),
                class_name="flex items-center mb-2",
            ),
            rx.el.div(
                rx.icon("clock", class_name="h-4 w-4 text-gray-500"),
                rx.el.span(
                    activity["datetime_start"][:16].replace("T", " "),
                    class_name="ml-1 text-sm text-gray-400",
                ),
                class_name="flex items-center",
            ),
            class_name="grid grid-cols-2 gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"Hosted by {SceneState.users[activity['host_user_id']]['name']}",
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.a(
                    "Details",
                    href=f"/activity/{activity['id']}",
                    class_name="text-sm text-teal-400 hover:underline",
                ),
                rx.el.button(
                    "Request to Join",
                    on_click=lambda: SceneState.open_request_modal(
                        "activity", activity["id"]
                    ),
                    class_name="px-4 py-2 bg-teal-500 text-white rounded-lg text-sm font-semibold hover:bg-teal-400 transition-colors",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between mt-4 pt-4 border-t border-gray-800",
        ),
        class_name="bg-gray-900/50 p-5 rounded-2xl border border-gray-800 shadow-lg hover:border-teal-500/50 transition-all duration-300",
    )