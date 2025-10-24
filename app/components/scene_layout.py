import reflex as rx
from app.states.scene_state import SceneState
from app.states.wizard_state import WizardState
from app.components.create_wizard import create_wizard_modal
from app.components.request_modal import request_to_join_modal


def scene_header() -> rx.Component:
    """Modern dark header with Scene branding"""
    return rx.el.header(
        rx.el.nav(
            rx.el.div(
                rx.icon("sparkles", class_name="h-8 w-8 text-teal-400"),
                rx.el.span("Scene", class_name="ml-2 text-xl font-bold text-white"),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("home", class_name="h-5 w-5"),
                    "Home",
                    on_click=lambda: SceneState.set_current_page("home"),
                    class_name=rx.cond(
                        SceneState.current_page == "home",
                        "flex items-center gap-2 px-4 py-2 rounded-xl bg-teal-500/20 text-teal-400 font-medium transition-all duration-200",
                        "flex items-center gap-2 px-4 py-2 rounded-xl text-gray-400 hover:text-white hover:bg-gray-800/50 font-medium transition-all duration-200",
                    ),
                ),
                rx.el.button(
                    rx.icon("calendar", class_name="h-5 w-5"),
                    "Activities",
                    on_click=lambda: SceneState.set_current_page("activities"),
                    class_name=rx.cond(
                        SceneState.current_page == "activities",
                        "flex items-center gap-2 px-4 py-2 rounded-xl bg-teal-500/20 text-teal-400 font-medium transition-all duration-200",
                        "flex items-center gap-2 px-4 py-2 rounded-xl text-gray-400 hover:text-white hover:bg-gray-800/50 font-medium transition-all duration-200",
                    ),
                ),
                rx.el.button(
                    rx.icon("map-pin", class_name="h-5 w-5"),
                    "Venues",
                    on_click=lambda: SceneState.set_current_page("venues"),
                    class_name=rx.cond(
                        SceneState.current_page == "venues",
                        "flex items-center gap-2 px-4 py-2 rounded-xl bg-teal-500/20 text-teal-400 font-medium transition-all duration-200",
                        "flex items-center gap-2 px-4 py-2 rounded-xl text-gray-400 hover:text-white hover:bg-gray-800/50 font-medium transition-all duration-200",
                    ),
                ),
                rx.el.button(
                    rx.icon("users", class_name="h-5 w-5"),
                    "Profile",
                    on_click=lambda: SceneState.set_current_page("profile"),
                    class_name=rx.cond(
                        SceneState.current_page == "profile",
                        "flex items-center gap-2 px-4 py-2 rounded-xl bg-teal-500/20 text-teal-400 font-medium transition-all duration-200",
                        "flex items-center gap-2 px-4 py-2 rounded-xl text-gray-400 hover:text-white hover:bg-gray-800/50 font-medium transition-all duration-200",
                    ),
                ),
                class_name="hidden md:flex items-center gap-1",
            ),
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        SceneState.users.values(),
                        lambda user: rx.el.option(user["name"], value=user["id"]),
                    ),
                    value=SceneState.current_user_id,
                    on_change=SceneState.set_current_user_id,
                    class_name="bg-gray-800 text-white border-none rounded-md text-sm p-1 mr-4",
                ),
                rx.image(
                    src=SceneState.current_user.get("avatar", "/placeholder.svg"),
                    class_name="h-8 w-8 rounded-full",
                ),
                rx.el.span(
                    SceneState.current_user.get("name", "Guest"),
                    class_name="hidden sm:block ml-2 text-sm font-medium text-gray-300",
                ),
                rx.el.div(
                    rx.icon("award", class_name="h-4 w-4 text-yellow-500"),
                    rx.el.span(
                        SceneState.user_vouch_count,
                        class_name="text-xs font-bold text-yellow-500",
                    ),
                    class_name="flex items-center gap-1 ml-2",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between px-6 py-4 border-b border-gray-800/50",
        ),
        class_name="bg-gray-900/95 backdrop-blur-sm sticky top-0 z-50",
    )


def bottom_nav() -> rx.Component:
    """Bottom navigation for mobile view with a central create button."""
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("home", class_name="h-6 w-6"),
                on_click=lambda: SceneState.set_current_page("home"),
                class_name="flex flex-col items-center justify-center text-gray-400 hover:text-teal-400 transition-colors w-full",
            ),
            rx.el.button(
                rx.icon("calendar", class_name="h-6 w-6"),
                on_click=lambda: SceneState.set_current_page("activities"),
                class_name="flex flex-col items-center justify-center text-gray-400 hover:text-teal-400 transition-colors w-full",
            ),
            rx.el.div(class_name="w-16"),
            rx.el.button(
                rx.icon("map-pin", class_name="h-6 w-6"),
                on_click=lambda: SceneState.set_current_page("venues"),
                class_name="flex flex-col items-center justify-center text-gray-400 hover:text-teal-400 transition-colors w-full",
            ),
            rx.el.button(
                rx.icon("user", class_name="h-6 w-6"),
                on_click=lambda: SceneState.set_current_page("profile"),
                class_name="flex flex-col items-center justify-center text-gray-400 hover:text-teal-400 transition-colors w-full",
            ),
            class_name="flex items-center justify-around h-16 bg-gray-900/90 backdrop-blur-sm w-full",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-8 w-8 text-white"),
            on_click=WizardState.open_create_modal,
            class_name="absolute -top-6 left-1/2 -translate-x-1/2 flex items-center justify-center h-16 w-16 rounded-full bg-teal-500 shadow-lg hover:bg-teal-400 transition-transform hover:scale-105",
        ),
        class_name="fixed bottom-0 left-0 right-0 z-40 md:hidden",
    )


def scene_footer() -> rx.Component:
    """Dark themed footer"""
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("sparkles", class_name="h-6 w-6 text-teal-400"),
                    rx.el.span("Scene", class_name="ml-2 text-lg font-bold text-white"),
                    class_name="flex items-center",
                ),
                rx.el.p(
                    "Your community for activities, events, and venues in Pakistan.",
                    class_name="mt-2 text-sm text-gray-400 max-w-md",
                ),
                class_name="mb-8 md:mb-0",
            ),
            rx.el.div(
                rx.el.h4("Features", class_name="text-white font-semibold mb-4"),
                rx.el.ul(
                    rx.el.li("Find Activity Partners", class_name="text-gray-400 mb-2"),
                    rx.el.li("Host Events", class_name="text-gray-400 mb-2"),
                    rx.el.li("Book Venues", class_name="text-gray-400 mb-2"),
                    rx.el.li("Vouch System", class_name="text-gray-400 mb-2"),
                ),
            ),
            rx.el.div(
                rx.el.h4("Support", class_name="text-white font-semibold mb-4"),
                rx.el.ul(
                    rx.el.li("Help Center", class_name="text-gray-400 mb-2"),
                    rx.el.li("Community Guidelines", class_name="text-gray-400 mb-2"),
                    rx.el.li("Safety Tips", class_name="text-gray-400 mb-2"),
                    rx.el.li("Contact Us", class_name="text-gray-400 mb-2"),
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto px-6 py-12",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "© 2024 Scene Pakistan. Made with ❤️ for the community.",
                    class_name="text-gray-400 text-sm",
                ),
                class_name="max-w-6xl mx-auto px-6 py-6 border-t border-gray-800 text-center",
            )
        ),
        class_name="bg-gray-900 mt-20",
    )


def scene_layout(content: rx.Component) -> rx.Component:
    """Main layout wrapper with dark theme"""
    return rx.el.div(
        create_wizard_modal(),
        request_to_join_modal(),
        scene_header(),
        rx.cond(
            SceneState.error_message != "",
            rx.el.div(
                rx.el.div(
                    rx.icon("circle_x", class_name="h-5 w-5 text-red-400"),
                    rx.el.span(
                        SceneState.error_message, class_name="ml-2 text-sm font-medium"
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        on_click=SceneState.clear_messages,
                        class_name="ml-auto text-red-400 hover:text-red-300",
                    ),
                    class_name="flex items-center p-4 bg-red-500/10 border border-red-500/20 rounded-xl",
                ),
                class_name="max-w-6xl mx-auto px-6 py-4",
            ),
        ),
        rx.cond(
            SceneState.success_message != "",
            rx.el.div(
                rx.el.div(
                    rx.icon("check_check", class_name="h-5 w-5 text-green-400"),
                    rx.el.span(
                        SceneState.success_message,
                        class_name="ml-2 text-sm font-medium",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        on_click=SceneState.clear_messages,
                        class_name="ml-auto text-green-400 hover:text-green-300",
                    ),
                    class_name="flex items-center p-4 bg-green-500/10 border border-green-500/20 rounded-xl",
                ),
                class_name="max-w-6xl mx-auto px-6 py-4",
            ),
        ),
        rx.el.main(content, class_name="flex-1 min-h-screen"),
        scene_footer(),
        bottom_nav(),
        class_name="bg-gray-900 text-white font-['JetBrains_Mono'] min-h-screen flex flex-col",
    )