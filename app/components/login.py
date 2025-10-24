import reflex as rx
from app.states.base_state import BaseState


def login_modal() -> rx.Component:
    return rx.cond(
        ~BaseState.is_authenticated,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Sign in to Scene",
                            class_name="text-2xl font-bold text-white text-center",
                        ),
                        rx.el.p(
                            "Enter your details to join the community.",
                            class_name="text-sm text-gray-400 text-center mt-2",
                        ),
                        rx.el.form(
                            rx.el.div(
                                rx.el.label(
                                    "Phone or Email",
                                    class_name="text-sm font-medium text-gray-300 mb-2",
                                ),
                                rx.el.input(
                                    placeholder="you@example.com",
                                    name="phone_or_email",
                                    type="email",
                                    class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
                                ),
                                rx.el.label(
                                    "Your Name",
                                    class_name="text-sm font-medium text-gray-300 mb-2",
                                ),
                                rx.el.input(
                                    placeholder="e.g. Ahmed Khan",
                                    name="name",
                                    class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-6",
                                ),
                                rx.el.button(
                                    "Sign In",
                                    type="submit",
                                    class_name="w-full p-3 bg-teal-500 text-white rounded-lg font-semibold hover:bg-teal-400 transition-colors",
                                ),
                                class_name="flex flex-col mt-6",
                            ),
                            on_submit=BaseState.login,
                        ),
                        class_name="p-8",
                    ),
                    class_name="relative bg-gray-900/80 backdrop-blur-md border border-teal-500/20 rounded-2xl shadow-2xl w-full max-w-md",
                ),
                class_name="flex items-center justify-center min-h-screen p-4",
            ),
            class_name="fixed inset-0 bg-black/70 z-50",
        ),
    )