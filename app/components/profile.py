import reflex as rx
from app.states.profile_state import ProfileState
from app.states.wizard_state import WizardState


def profile_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=ProfileState.me.get("avatar_url", "/placeholder.svg"),
                class_name="h-20 w-20 rounded-full border-4 border-gray-800",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        ProfileState.me.get("name", "User"),
                        class_name="text-2xl font-bold text-white",
                    ),
                    rx.cond(
                        ProfileState.me.get("verified_flag", False),
                        rx.icon(
                            "shield-check", class_name="h-6 w-6 text-teal-400 ml-2"
                        ),
                    ),
                    class_name="flex items-center",
                ),
                rx.el.p(ProfileState.me.get("city", ""), class_name="text-gray-400"),
                class_name="ml-4",
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            "Edit Profile",
            on_click=lambda: rx.toast.info("Not implemented"),
            class_name="px-4 py-2 text-sm font-semibold text-white bg-gray-700 rounded-lg",
        ),
        class_name="flex items-center justify-between p-4 bg-gray-900 sticky top-0 z-10 border-b border-gray-800",
    )


def stat_pill(label: str, value: rx.Var[int]) -> rx.Component:
    return rx.el.div(
        rx.el.span(value, class_name="text-lg font-bold text-white"),
        rx.el.span(label, class_name="text-xs text-gray-400"),
        class_name="flex flex-col items-center justify-center p-3 bg-gray-800 rounded-lg",
    )


def overview_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Overview", class_name="text-lg font-semibold text-white mb-3"),
        rx.el.div(
            stat_pill("Vouches Rx", ProfileState.vouches_received.length()),
            stat_pill("Vouches Given", ProfileState.vouches_given.length()),
            stat_pill("Circles", ProfileState.circles.length()),
            stat_pill("Hosted Items", ProfileState.hosted_items_count),
            class_name="grid grid-cols-2 sm:grid-cols-4 gap-3",
        ),
        class_name="p-4 bg-gray-800/50 rounded-xl border border-gray-700",
    )


def _vouch_item(vouch: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=vouch.get("giver_avatar_url", "/placeholder.svg"),
                class_name="h-10 w-10 rounded-full",
            ),
            rx.el.div(
                rx.el.p(vouch.get("giver_name"), class_name="font-semibold text-white"),
                rx.el.p(
                    vouch.get("short_text", ""), class_name="text-sm text-gray-400"
                ),
                class_name="ml-3",
            ),
            class_name="flex items-center",
        ),
        rx.el.span(
            vouch.get("created_at").to_string()[:10], class_name="text-xs text-gray-500"
        ),
        class_name="flex items-center justify-between p-3 bg-gray-800 rounded-lg",
    )


def vouch_list() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Vouches", class_name="text-lg font-semibold text-white mb-3"),
        rx.el.div(
            rx.el.button(
                f"Received ({ProfileState.vouches_received.length()})",
                on_click=lambda: ProfileState.set_vouch_tab("received"),
                class_name=rx.cond(
                    ProfileState.vouch_tab == "received",
                    "px-4 py-2 text-sm font-semibold text-teal-400 bg-teal-500/10 border-b-2 border-teal-400",
                    "px-4 py-2 text-sm text-gray-400",
                ),
            ),
            rx.el.button(
                f"Given ({ProfileState.vouches_given.length()})",
                on_click=lambda: ProfileState.set_vouch_tab("given"),
                class_name=rx.cond(
                    ProfileState.vouch_tab == "given",
                    "px-4 py-2 text-sm font-semibold text-teal-400 bg-teal-500/10 border-b-2 border-teal-400",
                    "px-4 py-2 text-sm text-gray-400",
                ),
            ),
            class_name="flex border-b border-gray-700",
        ),
        rx.el.div(
            rx.match(
                ProfileState.vouch_tab,
                (
                    "received",
                    rx.cond(
                        ProfileState.vouches_received.length() == 0,
                        rx.el.p(
                            "No vouches received yet.",
                            class_name="text-gray-500 text-center p-6",
                        ),
                        rx.el.div(
                            rx.foreach(ProfileState.vouches_received, _vouch_item),
                            class_name="space-y-2",
                        ),
                    ),
                ),
                (
                    "given",
                    rx.cond(
                        ProfileState.vouches_given.length() == 0,
                        rx.el.p(
                            "You haven't given any vouches yet.",
                            class_name="text-gray-500 text-center p-6",
                        ),
                        rx.el.div(
                            rx.foreach(ProfileState.vouches_given, _vouch_item),
                            class_name="space-y-2",
                        ),
                    ),
                ),
            ),
            class_name="p-4",
        ),
        class_name="bg-gray-800/50 rounded-xl border border-gray-700",
    )


def circles_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Circles", class_name="text-lg font-semibold text-white mb-3"),
        rx.cond(
            ProfileState.circles.length() == 0,
            rx.el.p(
                "Not a member of any circles yet.",
                class_name="text-gray-500 text-center p-6",
            ),
            rx.el.div(
                rx.foreach(
                    ProfileState.circles,
                    lambda circle: rx.el.span(
                        circle.get("name", "Unnamed Circle"),
                        class_name="px-3 py-1 bg-gray-700 text-white text-sm rounded-full",
                    ),
                ),
                class_name="flex flex-wrap gap-2",
            ),
        ),
        class_name="p-4 bg-gray-800/50 rounded-xl border border-gray-700",
    )


def my_activities_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("My Activities", class_name="text-lg font-semibold text-white mb-3"),
        rx.cond(
            ProfileState.my_activities_open.length() == 0,
            rx.el.p(
                "You haven't hosted any open activities yet.",
                class_name="text-gray-500 text-center p-6",
            ),
            rx.el.div(
                rx.foreach(
                    ProfileState.my_activities_open,
                    lambda activity: rx.el.a(
                        rx.el.p(activity.get("title"), class_name="text-white"),
                        href=f"/activity/{activity.get('id')}",
                        class_name="block p-3 bg-gray-800 rounded-lg hover:bg-gray-700",
                    ),
                ),
                class_name="space-y-2",
            ),
        ),
        rx.el.button(
            "Create Activity",
            on_click=WizardState.open_create_modal,
            class_name="mt-4 w-full p-3 bg-teal-500 text-white rounded-lg font-semibold",
        ),
        class_name="p-4 bg-gray-800/50 rounded-xl border border-gray-700",
    )


def my_events_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("My Events", class_name="text-lg font-semibold text-white mb-3"),
        rx.cond(
            ProfileState.my_events_upcoming.length() == 0,
            rx.el.p(
                "You don't have any upcoming events.",
                class_name="text-gray-500 text-center p-6",
            ),
            rx.el.div(
                rx.foreach(
                    ProfileState.my_events_upcoming,
                    lambda event: rx.el.a(
                        rx.el.p(event.get("title"), class_name="text-white"),
                        href=f"/event/{event.get('id')}",
                        class_name="block p-3 bg-gray-800 rounded-lg hover:bg-gray-700",
                    ),
                ),
                class_name="space-y-2",
            ),
        ),
        class_name="p-4 bg-gray-800/50 rounded-xl border border-gray-700",
    )


def my_bookings_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("My Bookings", class_name="text-lg font-semibold text-white mb-3"),
        rx.el.div(
            rx.el.button(
                "Upcoming",
                on_click=lambda: ProfileState.set_booking_tab("upcoming"),
                class_name=rx.cond(
                    ProfileState.booking_tab == "upcoming",
                    "px-4 py-2 text-sm font-semibold text-teal-400 bg-teal-500/10 border-b-2 border-teal-400",
                    "px-4 py-2 text-sm text-gray-400",
                ),
            ),
            rx.el.button(
                "Past",
                on_click=lambda: ProfileState.set_booking_tab("past"),
                class_name=rx.cond(
                    ProfileState.booking_tab == "past",
                    "px-4 py-2 text-sm font-semibold text-teal-400 bg-teal-500/10 border-b-2 border-teal-400",
                    "px-4 py-2 text-sm text-gray-400",
                ),
            ),
            class_name="flex border-b border-gray-700",
        ),
        rx.el.div(
            rx.match(
                ProfileState.booking_tab,
                (
                    "upcoming",
                    rx.cond(
                        ProfileState.my_bookings_upcoming.length() == 0,
                        rx.el.p(
                            "No upcoming bookings.",
                            class_name="text-gray-500 text-center p-6",
                        ),
                        rx.el.div(
                            rx.foreach(
                                ProfileState.my_bookings_upcoming,
                                lambda booking: rx.el.div(
                                    rx.el.p(booking.get("venue_name"))
                                ),
                            ),
                            class_name="space-y-2",
                        ),
                    ),
                ),
                (
                    "past",
                    rx.cond(
                        ProfileState.my_bookings_past.length() == 0,
                        rx.el.p(
                            "No past bookings.",
                            class_name="text-gray-500 text-center p-6",
                        ),
                        rx.el.div(
                            rx.foreach(
                                ProfileState.my_bookings_past,
                                lambda booking: rx.el.div(
                                    rx.el.p(booking.get("venue_name"))
                                ),
                            ),
                            class_name="space-y-2",
                        ),
                    ),
                ),
            ),
            class_name="p-4",
        ),
        class_name="p-4 bg-gray-800/50 rounded-xl border border-gray-700",
    )


def quick_actions_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Quick Actions", class_name="text-lg font-semibold text-white mb-3"),
        rx.el.div(
            rx.el.button(
                "Edit Profile",
                on_click=lambda: rx.toast.info("Not Implemented"),
                class_name="w-full p-3 bg-gray-700 rounded-lg text-left",
            ),
            rx.el.button(
                "Edit Activities & Availability",
                on_click=lambda: rx.toast.info("Not Implemented"),
                class_name="w-full p-3 bg-gray-700 rounded-lg text-left",
            ),
            rx.el.button(
                "Privacy & Circles",
                on_click=lambda: rx.toast.info("Not Implemented"),
                class_name="w-full p-3 bg-gray-700 rounded-lg text-left",
            ),
            class_name="grid grid-cols-1 gap-3",
        ),
        class_name="p-4 bg-gray-800/50 rounded-xl border border-gray-700",
    )