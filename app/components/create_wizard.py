import reflex as rx
from app.states.wizard_state import WizardState
from app.states.scene_state import SceneState


def wizard_progress_indicator() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            WizardState.wizard_steps,
            lambda step, index: rx.el.div(
                rx.el.div(
                    rx.el.span(index + 1),
                    class_name=rx.cond(
                        WizardState.current_step >= index,
                        "flex items-center justify-center w-8 h-8 rounded-full bg-teal-500 text-white font-bold",
                        "flex items-center justify-center w-8 h-8 rounded-full bg-gray-700 text-gray-400 font-bold",
                    ),
                ),
                rx.el.span(
                    step,
                    class_name=rx.cond(
                        WizardState.current_step >= index,
                        "mt-2 text-xs text-white",
                        "mt-2 text-xs text-gray-500",
                    ),
                ),
                class_name="flex flex-col items-center",
            ),
        ),
        class_name="flex justify-between items-start mb-8 px-4",
    )


def create_activity_step_1() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Activity Type", class_name="text-sm font-medium text-gray-300 mb-2"
        ),
        rx.el.select(
            rx.foreach(
                WizardState.activity_types,
                lambda type: rx.el.option(type.title(), value=type),
            ),
            on_change=lambda value: WizardState.update_form_field(
                "activity_type", value
            ),
            default_value=WizardState.form_data.get("activity_type", "").to_string(),
            placeholder="Select an activity type...",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        rx.el.label("Title", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.input(
            on_change=lambda value: WizardState.update_form_field("title", value),
            default_value=WizardState.form_data.get("title", ""),
            placeholder="e.g., Morning Paddle Session",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        rx.el.label("Description", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.textarea(
            on_change=lambda value: WizardState.update_form_field("description", value),
            default_value=WizardState.form_data.get("description", "").to_string(),
            placeholder="Any details like skill level, what to bring, etc.",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white h-24",
        ),
        class_name="flex flex-col",
    )


def create_activity_step_2() -> rx.Component:
    return rx.el.div(
        rx.el.label("Date", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.input(
            type="date",
            on_change=lambda value: WizardState.update_form_field("date", value),
            default_value=WizardState.form_data.get("date", ""),
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        rx.el.label("Start Time", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.input(
            type="time",
            on_change=lambda value: WizardState.update_form_field("start_time", value),
            default_value=WizardState.form_data.get("start_time", ""),
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        rx.el.label(
            "Duration (minutes)", class_name="text-sm font-medium text-gray-300 mb-2"
        ),
        rx.el.input(
            type="number",
            on_change=lambda value: WizardState.update_form_field("duration", value),
            default_value=WizardState.form_data.get("duration", "").to_string(),
            placeholder="e.g., 90",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white",
        ),
        class_name="flex flex-col",
    )


def create_activity_step_3() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Location Description", class_name="text-sm font-medium text-gray-300 mb-2"
        ),
        rx.el.input(
            on_change=lambda value: WizardState.update_form_field(
                "location_text", value
            ),
            default_value=WizardState.form_data.get("location_text", ""),
            placeholder="e.g., Model Town Park, Block C",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        class_name="flex flex-col",
    )


def create_activity_step_4() -> rx.Component:
    return rx.el.div(
        rx.el.label("Capacity", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.input(
            type="number",
            on_change=lambda value: WizardState.update_form_field("capacity", value),
            default_value=WizardState.form_data.get("capacity", "").to_string(),
            placeholder="e.g., 4",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        class_name="flex flex-col",
    )


def create_activity_step_5() -> rx.Component:
    return rx.el.div(
        rx.el.label("Visibility", class_name="text-sm font-medium text-gray-300 mb-4"),
        rx.el.div(
            rx.foreach(
                ["Public", "Friends", "Circles", "InviteOnly"],
                lambda option: rx.el.button(
                    option,
                    on_click=lambda: WizardState.update_form_field(
                        "visibility", option
                    ),
                    class_name=rx.cond(
                        WizardState.form_data.get("visibility") == option,
                        "p-3 bg-teal-500 text-white rounded-lg font-semibold w-full",
                        "p-3 bg-gray-700 text-gray-300 rounded-lg w-full hover:bg-gray-600",
                    ),
                ),
            ),
            class_name="grid grid-cols-2 gap-2",
        ),
        class_name="flex flex-col",
    )


def create_activity_step_6() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Preview", class_name="text-lg font-bold text-white mb-4"),
        rx.el.div(
            rx.el.p(
                "Title: ",
                WizardState.form_data.get("title", ""),
                class_name="text-white",
            ),
            rx.el.p(
                "Activity: ",
                WizardState.form_data.get("activity_type", "").to_string(),
                class_name="text-gray-400 capitalize",
            ),
            rx.el.p(
                "When: ",
                f"{WizardState.form_data.get('date', '')} at {WizardState.form_data.get('start_time', '')}",
                class_name="text-gray-400",
            ),
            rx.el.p(
                "Location: ",
                WizardState.form_data.get("location_text", ""),
                class_name="text-gray-400",
            ),
            rx.el.p(
                "Capacity: ",
                WizardState.form_data.get("capacity", ""),
                class_name="text-gray-400",
            ),
            rx.el.p(
                "Visibility: ",
                WizardState.form_data.get("visibility", ""),
                class_name="text-gray-400",
            ),
            class_name="space-y-2 p-4 bg-gray-800 rounded-lg",
        ),
        class_name="flex flex-col",
    )


def create_activity_wizard_content() -> rx.Component:
    return rx.el.div(
        wizard_progress_indicator(),
        rx.el.div(
            rx.match(
                WizardState.current_step,
                (0, create_activity_step_1()),
                (1, create_activity_step_2()),
                (2, create_activity_step_3()),
                (3, create_activity_step_4()),
                (4, create_activity_step_5()),
                (5, create_activity_step_6()),
                rx.el.p("Invalid step"),
            ),
            class_name="p-4",
        ),
        class_name="flex-grow overflow-y-auto",
    )


def create_event_wizard_content() -> rx.Component:
    return rx.el.div(rx.el.p("Event creation coming soon!"))


def wizard_footer() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Back",
            on_click=WizardState.prev_step,
            class_name="px-6 py-3 bg-gray-700 text-white rounded-lg font-semibold",
            disabled=WizardState.is_first_step,
        ),
        rx.cond(
            WizardState.is_last_step,
            rx.el.button(
                "Publish",
                on_click=rx.cond(
                    WizardState.create_type == "activity",
                    WizardState.publish_activity,
                    WizardState.publish_event,
                ),
                class_name="px-6 py-3 bg-teal-500 text-white rounded-lg font-semibold",
            ),
            rx.el.button(
                "Next",
                on_click=WizardState.next_step,
                class_name="px-6 py-3 bg-teal-500 text-white rounded-lg font-semibold",
            ),
        ),
        class_name="flex justify-between p-4 border-t border-gray-700",
    )


def create_wizard_modal() -> rx.Component:
    """Modal for creating a new activity or event."""
    return rx.el.div(
        rx.cond(
            WizardState.show_create_modal,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.cond(
                            WizardState.create_type == "",
                            rx.el.div(
                                rx.el.h2(
                                    "What would you like to create?",
                                    class_name="text-2xl font-bold text-white mb-6 text-center",
                                ),
                                rx.el.div(
                                    rx.el.button(
                                        "Create Activity",
                                        on_click=lambda: WizardState.set_create_type(
                                            "activity"
                                        ),
                                        class_name="w-full p-4 bg-teal-500 text-white rounded-lg font-semibold text-lg hover:bg-teal-400",
                                    ),
                                    rx.el.button(
                                        "Create Event",
                                        on_click=lambda: WizardState.set_create_type(
                                            "event"
                                        ),
                                        class_name="w-full p-4 bg-purple-500 text-white rounded-lg font-semibold text-lg hover:bg-purple-400",
                                    ),
                                    class_name="space-y-4",
                                ),
                                rx.el.button(
                                    rx.icon("x", class_name="h-6 w-6"),
                                    on_click=WizardState.close_create_modal,
                                    class_name="absolute top-4 right-4 text-gray-400 hover:text-white",
                                ),
                                class_name="relative p-8",
                            ),
                            rx.el.div(
                                rx.cond(
                                    WizardState.create_type == "activity",
                                    create_activity_wizard_content(),
                                    create_event_wizard_content(),
                                ),
                                wizard_footer(),
                                class_name="flex flex-col h-full",
                            ),
                        ),
                        class_name="bg-gray-800 rounded-t-2xl shadow-2xl flex flex-col h-[85vh] w-full max-w-lg mx-auto",
                    ),
                    class_name="fixed inset-x-0 bottom-0 z-50",
                ),
                rx.el.div(
                    on_click=WizardState.close_create_modal,
                    class_name="fixed inset-0 bg-black/60 z-40",
                ),
            ),
        )
    )