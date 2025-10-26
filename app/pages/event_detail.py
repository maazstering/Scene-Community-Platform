import reflex as rx
from app.states.scene_state import SceneState


def event_detail_page() -> rx.Component:
    return rx.cond(
        SceneState.selected_event_id == "",
        rx.el.div(
            rx.el.p(
                "Event not found or not selected.",
                class_name="text-center text-gray-500",
            ),
            rx.el.button(
                "Go back",
                on_click=lambda: rx.redirect("/scene"),
                class_name="mt-4 px-4 py-2 bg-teal-500 rounded-lg",
            ),
            class_name="max-w-6xl mx-auto py-12 px-4 md:px-6 text-center",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("arrow-left", class_name="mr-2"),
                "Back to Events",
                href="/scene",
                on_click=lambda: SceneState.set_current_page("activities"),
                class_name="flex items-center text-teal-400 hover:underline mb-6 cursor-pointer",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=SceneState.selected_event_host.get("avatar"),
                                class_name="h-12 w-12 rounded-full",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    SceneState.selected_event_host.get("name"),
                                    class_name="font-bold text-white",
                                ),
                                rx.el.p(
                                    f"{SceneState.selected_event_host.get('vouches_count', 0)} vouches",
                                    class_name="text-sm text-gray-400",
                                ),
                                class_name="ml-4",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="bg-gray-800/50 p-4 rounded-xl border border-gray-700 mb-6",
                    ),
                    rx.el.h1(
                        SceneState.selected_event.get("title"),
                        class_name="text-3xl font-bold text-white mb-4",
                    ),
                    rx.el.p(
                        SceneState.selected_event.get("description"),
                        class_name="text-gray-300 leading-relaxed mb-6",
                    ),
                    rx.el.div(
                        rx.cond(
                            SceneState.selected_event.get("ticketed"),
                            rx.el.button(
                                rx.icon("ticket", class_name="mr-2"),
                                f"Buy Ticket - PKR {SceneState.selected_event.get('ticket_price_pkr')}",
                                class_name="flex items-center w-full justify-center px-6 py-3 bg-purple-500 text-white rounded-lg font-semibold text-lg hover:bg-purple-400 transition-colors",
                            ),
                            rx.el.button(
                                rx.icon("circle_plus", class_name="mr-2"),
                                "Request to Join",
                                on_click=lambda: SceneState.open_request_modal(
                                    "event", SceneState.selected_event_id
                                ),
                                class_name="flex items-center w-full justify-center px-6 py-3 bg-teal-500 text-white rounded-lg font-semibold text-lg hover:bg-teal-400 transition-colors",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("share-2", class_name="mr-2"),
                            "Share",
                            on_click=rx.set_clipboard(
                                f"/e/{SceneState.selected_event.get('share_slug')}"
                            ),
                            class_name="flex items-center w-full justify-center px-6 py-3 bg-gray-700 text-white rounded-lg font-semibold hover:bg-gray-600 transition-colors",
                        ),
                        class_name="grid grid-cols-2 gap-4 mt-8",
                    ),
                    class_name="w-full lg:w-2/3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("clock", class_name="h-5 w-5 text-gray-400"),
                            rx.el.div(
                                rx.el.p(
                                    "Date & Time", class_name="text-sm text-gray-400"
                                ),
                                rx.el.p(
                                    SceneState.selected_event_time,
                                    class_name="text-white font-medium",
                                ),
                                class_name="ml-3",
                            ),
                            class_name="flex items-center mb-4",
                        ),
                        rx.el.div(
                            rx.icon("map-pin", class_name="h-5 w-5 text-gray-400"),
                            rx.el.div(
                                rx.el.p("Venue", class_name="text-sm text-gray-400"),
                                rx.el.p(
                                    f"{SceneState.selected_event.get('venue_name', '')}, {SceneState.selected_event.get('city', '')}",
                                    class_name="text-white font-medium",
                                ),
                                class_name="ml-3",
                            ),
                            class_name="flex items-center mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("Capacity", class_name="text-sm text-gray-400"),
                                rx.el.p(
                                    f"{SceneState.selected_event.get('spots_taken', 0)}/{SceneState.selected_event.get('capacity', 1)} spots filled",
                                    class_name="text-white font-medium",
                                ),
                                class_name="flex justify-between items-center mb-2",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    style={
                                        "width": SceneState.selected_event_capacity_percentage
                                    },
                                    class_name="h-2 bg-purple-500 rounded-full",
                                ),
                                class_name="w-full bg-gray-700 rounded-full h-2",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.icon("eye", class_name="h-5 w-5 text-gray-400"),
                            rx.el.div(
                                rx.el.p(
                                    "Visibility", class_name="text-sm text-gray-400"
                                ),
                                rx.el.p(
                                    SceneState.selected_event.get("visibility_scope"),
                                    class_name="text-white font-medium capitalize",
                                ),
                                class_name="ml-3",
                            ),
                            class_name="flex items-center mb-6",
                        ),
                    ),
                    class_name="bg-gray-800/50 p-6 rounded-xl border border-gray-700 w-full lg:w-1/3",
                ),
                class_name="flex flex-col lg:flex-row gap-8",
            ),
            class_name="max-w-6xl mx-auto py-12 px-4 md:px-6",
        ),
    )