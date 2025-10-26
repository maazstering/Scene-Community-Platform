import reflex as rx
from app.states.profile_state import ProfileState
from app.components.scene_layout import scene_layout
from app.components.profile import (
    profile_header,
    overview_section,
    vouch_list,
    circles_section,
    my_activities_section,
    my_events_section,
    my_bookings_section,
    quick_actions_section,
)


def skeleton_loader() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="h-24 bg-gray-800 rounded-xl animate-pulse"),
        rx.el.div(class_name="h-48 bg-gray-800 rounded-xl animate-pulse"),
        rx.el.div(class_name="h-32 bg-gray-800 rounded-xl animate-pulse"),
        rx.el.div(class_name="h-32 bg-gray-800 rounded-xl animate-pulse"),
        class_name="space-y-4 p-4",
    )


def profile_content() -> rx.Component:
    return rx.el.div(
        overview_section(),
        vouch_list(),
        circles_section(),
        my_activities_section(),
        my_events_section(),
        my_bookings_section(),
        quick_actions_section(),
        class_name="space-y-4 p-4",
    )


def profile_dashboard() -> rx.Component:
    return scene_layout(
        rx.el.div(
            rx.cond(ProfileState.me, profile_header()),
            rx.cond(ProfileState.loading, skeleton_loader(), profile_content()),
            class_name="max-w-2xl mx-auto",
        )
    )