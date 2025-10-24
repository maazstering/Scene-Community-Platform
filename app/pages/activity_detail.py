import reflex as rx
from app.states.scene_state import SceneState


def activity_detail_page() -> rx.Component:
    return rx.cond(
        SceneState.selected_activity_id == "",
        rx.el.div(
            rx.el.p(
                "Activity not found or not selected.",
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
                "Back to Activities",
                href="/scene",
                on_click=lambda: SceneState.set_current_page("activities"),
                class_name="flex items-center text-teal-400 hover:underline mb-6 cursor-pointer",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=SceneState.selected_activity_host.get("avatar"),
                                class_name="h-12 w-12 rounded-full",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    SceneState.selected_activity_host.get("name"),
                                    class_name="font-bold text-white",
                                ),
                                rx.el.p(
                                    f"{SceneState.selected_activity_host.get('vouches_count', 0)} vouches",
                                    class_name="text-sm text-gray-400",
                                ),
                                class_name="ml-4",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="bg-gray-800/50 p-4 rounded-xl border border-gray-700 mb-6",
                    ),
                    rx.el.h1(
                        SceneState.selected_activity.get("title"),
                        class_name="text-3xl font-bold text-white mb-2",
                    ),
                    rx.el.span(
                        SceneState.selected_activity.get("activity_type")
                        .to_string()
                        .capitalize(),
                        class_name="px-2 py-1 bg-teal-500/20 text-teal-400 text-sm font-medium rounded-full mb-4 inline-block",
                    ),
                    rx.el.p(
                        SceneState.selected_activity.get("description"),
                        class_name="text-gray-300 leading-relaxed mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("circle_plus", class_name="mr-2"),
                            "Request to Join",
                            on_click=lambda: SceneState.open_request_modal(
                                "activity", SceneState.selected_activity_id
                            ),
                            class_name="flex items-center w-full justify-center px-6 py-3 bg-teal-500 text-white rounded-lg font-semibold text-lg hover:bg-teal-400 transition-colors",
                        ),
                        rx.el.button(
                            rx.icon("share-2", class_name="mr-2"),
                            "Share",
                            on_click=rx.set_clipboard(
                                f"/a/{SceneState.selected_activity.get('share_slug')}"
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
                                rx.el.p("Time", class_name="text-sm text-gray-400"),
                                rx.el.p(
                                    SceneState.selected_activity_time,
                                    class_name="text-white font-medium",
                                ),
                                class_name="ml-3",
                            ),
                            class_name="flex items-center mb-4",
                        ),
                        rx.el.div(
                            rx.icon("map-pin", class_name="h-5 w-5 text-gray-400"),
                            rx.el.div(
                                rx.el.p("Location", class_name="text-sm text-gray-400"),
                                rx.el.p(
                                    SceneState.selected_activity.get("location_text"),
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
                                    f"{SceneState.selected_activity.get('current_participants', 0)}/{SceneState.selected_activity.get('capacity', 1)} spots taken",
                                    class_name="text-white font-medium",
                                ),
                                class_name="flex justify-between items-center mb-2",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    style={
                                        "width": SceneState.selected_activity_capacity_percentage
                                    },
                                    class_name="h-2 bg-teal-500 rounded-full",
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
                                    SceneState.selected_activity.get("visibility"),
                                    class_name="text-white font-medium",
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