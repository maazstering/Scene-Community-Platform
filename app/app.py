import reflex as rx
import reflex as rx
from app.states.base_state import BaseState
from app.states.scene_state import SceneState
from app.components.layout import main_layout
from app.pages.scene import scene
from app.components.login import login_modal


def index() -> rx.Component:
    return main_layout(
        rx.fragment(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("sparkles", class_name="h-16 w-16 text-teal-400"),
                        class_name="mx-auto flex h-24 w-24 items-center justify-center rounded-full bg-gray-800/80 border border-teal-500/20 shadow-lg",
                    ),
                    rx.el.h1(
                        "Welcome to Scene",
                        class_name="mt-8 text-4xl font-bold tracking-tight text-white sm:text-5xl",
                    ),
                    rx.el.p(
                        "Your community for activities, events, and venues in Pakistan.",
                        class_name="mt-6 text-lg leading-8 text-gray-400",
                    ),
                    class_name="mx-auto max-w-2xl text-center",
                ),
                class_name="relative isolate px-6 pt-14 lg:px-8",
            ),
            rx.cond(~BaseState.is_authenticated, login_modal()),
        )
    )


from app.backend.main import app as backend_app

app = rx.App(
    theme=rx.theme(appearance="light", accent_color="teal", radius="large"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
    api_transformer=backend_app,
)
app.add_page(index, on_load=BaseState.check_auth)
from app.states.profile_state import ProfileState
from app.pages.profile import profile_dashboard

app.add_page(scene, route="/scene", on_load=[BaseState.check_auth, SceneState.on_load])
app.add_page(
    profile_dashboard,
    route="/profile",
    on_load=[BaseState.check_auth, ProfileState.on_profile_load],
)
app.add_page(
    scene,
    route="/activity/[activity_id]",
    on_load=[BaseState.check_auth, SceneState.on_load_detail],
)
app.add_page(
    scene,
    route="/event/[event_id]",
    on_load=[BaseState.check_auth, SceneState.on_load_detail],
)