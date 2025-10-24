import reflex as rx
from app.states.scene_state import SceneState


def request_to_join_modal() -> rx.Component:
    """Modal for requesting to join an activity or event."""
    return rx.el.div(
        rx.cond(
            SceneState.show_request_modal,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Request to Join",
                            class_name="text-2xl font-bold text-white mb-2 text-center",
                        ),
                        rx.el.p(
                            "Send a note to the host with your request.",
                            class_name="text-sm text-gray-400 mb-6 text-center",
                        ),
                        rx.el.textarea(
                            placeholder="e.g. I'm a beginner, hope that's okay!",
                            on_change=SceneState.set_request_note_input,
                            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white h-24 mb-6",
                            default_value=SceneState.request_note_input,
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancel",
                                on_click=SceneState.close_request_modal,
                                class_name="w-full p-3 bg-gray-700 text-white rounded-lg font-semibold hover:bg-gray-600",
                            ),
                            rx.el.button(
                                "Send Request",
                                on_click=SceneState.submit_join_request,
                                class_name="w-full p-3 bg-teal-500 text-white rounded-lg font-semibold hover:bg-teal-400",
                            ),
                            class_name="grid grid-cols-2 gap-4",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6"),
                            on_click=SceneState.close_request_modal,
                            class_name="absolute top-4 right-4 text-gray-400 hover:text-white",
                        ),
                        class_name="relative bg-gray-900/80 backdrop-blur-md border border-teal-500/20 rounded-2xl shadow-2xl w-full max-w-md p-8",
                    ),
                    class_name="flex items-center justify-center min-h-screen p-4",
                ),
                rx.el.div(
                    on_click=SceneState.close_request_modal,
                    class_name="fixed inset-0 bg-black/70 z-50",
                ),
            ),
        )
    )