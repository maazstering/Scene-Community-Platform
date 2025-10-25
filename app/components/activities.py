import reflex as rx
from app.states.scene_state import SceneState


def activity_card(activity: dict) -> rx.Component:
    """Individual activity card with modern design"""
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=rx.cond(
                        activity["banner_url"],
                        rx.get_upload_url(activity["banner_url"]),
                        "/placeholder.svg",
                    ),
                    class_name="absolute inset-0 w-full h-full object-cover",
                ),
                rx.el.div(
                    class_name="absolute inset-0 bg-gradient-to-t from-black/80 via-black/50 to-transparent"
                ),
                class_name="absolute inset-0 rounded-t-2xl overflow-hidden",
            ),
            rx.el.div(
                rx.el.div(
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
                                class_name="px-2 py-1 bg-gray-800/80 text-gray-300 rounded-lg text-xs font-medium",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    rx.el.h3(
                        activity["title"],
                        class_name="text-lg font-bold text-white mb-2",
                    ),
                    rx.el.p(
                        activity["description"],
                        class_name="text-gray-400 text-sm mb-4 line-clamp-2",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("map-pin", class_name="h-4 w-4 text-gray-500"),
                            rx.el.span(
                                activity["location_text"],
                                class_name="ml-1 text-sm text-gray-400",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.div(
                            rx.icon("clock", class_name="h-4 w-4 text-gray-500"),
                            rx.el.span(
                                activity["datetime_start"][:16].replace("T", " "),
                                class_name="ml-1 text-sm text-gray-400",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.p(
                        f"Hosted by {SceneState.users[activity['host_user_id']]['name']}",
                        class_name="text-xs text-gray-500 mt-2",
                    ),
                    class_name="mt-auto",
                ),
                class_name="relative z-10 flex flex-col h-full p-5",
            ),
            class_name="relative h-72",
        ),
        href=f"/activity/{activity['id']}",
        class_name="bg-gray-900/50 rounded-2xl border border-gray-800 shadow-lg hover:border-teal-500/50 transition-all duration-300 flex flex-col overflow-hidden",
    )