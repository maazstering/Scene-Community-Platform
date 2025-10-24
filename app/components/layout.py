import reflex as rx
from app.states.base_state import BaseState


def main_layout(child: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.nav(
                rx.el.a(
                    rx.el.span("Scene", class_name="sr-only"),
                    rx.icon("users", class_name="h-8 w-auto text-teal-400"),
                    href="/",
                ),
                rx.cond(
                    BaseState.is_authenticated,
                    rx.el.div(
                        rx.el.button(
                            "Sign Out",
                            on_click=BaseState.logout,
                            class_name="text-sm font-semibold leading-6 text-white",
                        ),
                        class_name="flex flex-1 justify-end",
                    ),
                    rx.el.div(class_name="flex flex-1 justify-end"),
                ),
                class_name="flex items-center justify-between p-6 lg:px-8",
                aria_label="Global",
            ),
            class_name="absolute inset-x-0 top-0 z-50",
        ),
        rx.el.main(child, class_name="flex-1 flex items-center justify-center"),
        rx.el.div(
            rx.el.div(
                class_name="relative left-[calc(50%+3rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 bg-gradient-to-tr from-[#80ff8d] to-[#00796b] opacity-30 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]",
                style={
                    "clipPath": "polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%) "
                },
            ),
            class_name="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]",
            aria_hidden="true",
        ),
        class_name="bg-gray-900 min-h-screen flex flex-col font-['JetBrains_Mono'] selection:bg-teal-500/30 isolate",
    )