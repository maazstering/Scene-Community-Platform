import reflex as rx
from app.states.base_state import BaseState


def _auth_form_input(name: str, placeholder: str, type: str = "text") -> rx.Component:
    return rx.el.div(
        rx.el.label(
            name.replace("_", " ").title(),
            class_name="text-sm font-medium text-gray-300 mb-2",
        ),
        rx.el.input(
            placeholder=placeholder,
            name=name,
            type=type,
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white",
        ),
        class_name="mb-4",
    )


def login_form() -> rx.Component:
    return rx.el.form(
        _auth_form_input("phone_or_email", "you@example.com", "email"),
        _auth_form_input("password", "••••••••", "password"),
        rx.el.button(
            "Sign In",
            type="submit",
            class_name="w-full p-3 bg-teal-500 text-white rounded-lg font-semibold hover:bg-teal-400 transition-colors",
            is_loading=BaseState.loading,
        ),
        on_submit=BaseState.login,
        class_name="mt-6",
    )


def signup_form() -> rx.Component:
    return rx.el.form(
        _auth_form_input("name", "e.g. Ahmed Khan"),
        _auth_form_input("phone_or_email", "you@example.com", "email"),
        _auth_form_input("password", "••••••••", "password"),
        _auth_form_input("invite_code", "Optional invite code"),
        rx.el.button(
            "Sign Up",
            type="submit",
            class_name="w-full p-3 bg-teal-500 text-white rounded-lg font-semibold hover:bg-teal-400 transition-colors",
            is_loading=BaseState.loading,
        ),
        on_submit=BaseState.signup,
        class_name="mt-6",
    )


def login_modal() -> rx.Component:
    return rx.cond(
        ~BaseState.is_authenticated,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            rx.cond(
                                BaseState.auth_mode == "login",
                                "Sign in to Scene",
                                "Create an Account",
                            ),
                            class_name="text-2xl font-bold text-white text-center",
                        ),
                        rx.cond(
                            BaseState.error_message != "",
                            rx.el.div(
                                BaseState.error_message,
                                class_name="mt-4 p-3 bg-red-500/20 text-red-400 rounded-lg text-sm text-center",
                            ),
                        ),
                        rx.match(
                            BaseState.auth_mode,
                            ("login", login_form()),
                            ("signup", signup_form()),
                            rx.el.div(),
                        ),
                        rx.el.div(
                            rx.cond(
                                BaseState.auth_mode == "login",
                                rx.fragment(
                                    "Don't have an account? ",
                                    rx.el.button(
                                        "Sign up",
                                        on_click=lambda: BaseState.set_auth_mode(
                                            "signup"
                                        ),
                                        class_name="font-semibold text-teal-400 hover:underline",
                                    ),
                                ),
                                rx.fragment(
                                    "Already have an account? ",
                                    rx.el.button(
                                        "Log in",
                                        on_click=lambda: BaseState.set_auth_mode(
                                            "login"
                                        ),
                                        class_name="font-semibold text-teal-400 hover:underline",
                                    ),
                                ),
                            ),
                            class_name="text-center text-sm text-gray-400 mt-6",
                        ),
                        class_name="p-8",
                    ),
                    class_name="relative bg-gray-900/80 backdrop-blur-md border border-teal-500/20 rounded-2xl shadow-2xl w-full max-w-md",
                ),
                class_name="flex items-center justify-center min-h-screen p-4",
            ),
            class_name="fixed inset-0 bg-black/70 z-50 flex items-center justify-center",
        ),
    )