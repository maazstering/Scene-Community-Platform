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


def _upload_component(id: str, handler: rx.event.EventHandler) -> rx.Component:
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.icon("cloud_upload", class_name="w-8 h-8 text-gray-400"),
                rx.el.p(
                    "Drag and drop or click to upload",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-600 rounded-lg cursor-pointer hover:bg-gray-700/50",
            ),
            id=id,
            multiple=False,
            accept={"image/jpeg": [".jpg", ".jpeg"], "image/png": [".png"]},
            max_files=1,
            class_name="w-full",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files(id),
                lambda file: rx.el.div(
                    rx.el.p(file, class_name="text-sm text-white"),
                    rx.el.button(
                        "Upload",
                        on_click=handler(rx.upload_files(upload_id=id)),
                        class_name="ml-4 px-2 py-1 text-xs bg-teal-500 rounded",
                    ),
                    class_name="flex items-center justify-between p-2 mt-2 bg-gray-700 rounded-lg",
                ),
            ),
            class_name="mt-2",
        ),
        class_name="mb-4",
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
                "activity_type_id", value
            ),
            default_value=WizardState.form_data.get("activity_type_id", "").to_string(),
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
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white h-24 mb-4",
        ),
        rx.el.label(
            "Banner Image", class_name="text-sm font-medium text-gray-300 mb-2"
        ),
        _upload_component("activity_banner_upload", WizardState.handle_banner_upload),
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
        rx.el.label(
            "Allow Waitlist?", class_name="text-sm font-medium text-gray-300 mb-2"
        ),
        rx.el.div(
            rx.el.input(
                type="checkbox",
                on_change=lambda checked: WizardState.update_form_field(
                    "allow_waitlist", checked
                ),
                default_checked=WizardState.form_data.get("allow_waitlist", True).to(
                    bool
                ),
                class_name="h-4 w-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500",
            ),
            rx.el.label(
                "Yes, allow people to join a waitlist if full",
                class_name="ml-2 text-sm text-gray-300",
            ),
            class_name="flex items-center",
        ),
        class_name="flex flex-col",
    )


def create_activity_step_5() -> rx.Component:
    return rx.el.div(
        rx.el.label("Visibility", class_name="text-sm font-medium text-gray-300 mb-4"),
        rx.el.div(
            rx.foreach(
                ["public", "friends", "circles", "invite_only"],
                lambda option: rx.el.button(
                    option.replace("_", " ").title(),
                    on_click=lambda: WizardState.update_form_field(
                        "visibility_scope", option
                    ),
                    class_name=rx.cond(
                        WizardState.form_data.get("visibility_scope") == option,
                        "p-3 bg-teal-500 text-white rounded-lg font-semibold w-full capitalize",
                        "p-3 bg-gray-700 text-gray-300 rounded-lg w-full hover:bg-gray-600 capitalize",
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
            rx.image(
                src=rx.cond(
                    WizardState.form_data.get("banner_url"),
                    rx.get_upload_url(
                        WizardState.form_data.get("banner_url").to_string()
                    ),
                    "/placeholder.svg",
                ),
                class_name="w-full h-40 object-cover rounded-lg mb-4",
            ),
            rx.el.p(
                "Title: ",
                WizardState.form_data.get("title", ""),
                class_name="text-white",
            ),
            rx.el.p(
                "Activity: ",
                WizardState.form_data.get("activity_type_id", "")
                .to_string()
                .capitalize(),
                class_name="text-gray-400",
            ),
            rx.el.p(
                f"When: {WizardState.form_data.get('date', '')} at {WizardState.form_data.get('start_time', '')}",
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
                WizardState.form_data.get("visibility_scope", "")
                .to_string()
                .capitalize(),
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


def create_event_step_1() -> rx.Component:
    return rx.el.div(
        rx.el.label("Title", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.input(
            on_change=lambda value: WizardState.update_form_field("title", value),
            default_value=WizardState.form_data.get("title", ""),
            placeholder="e.g., Startup Summit 2024",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        rx.el.label("Description", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.textarea(
            on_change=lambda value: WizardState.update_form_field("description", value),
            default_value=WizardState.form_data.get("description", "").to_string(),
            placeholder="Details about your event...",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white h-24 mb-4",
        ),
        rx.el.label(
            "Poster Image", class_name="text-sm font-medium text-gray-300 mb-2"
        ),
        _upload_component("event_poster_upload", WizardState.handle_poster_upload),
        class_name="flex flex-col",
    )


def create_event_step_2() -> rx.Component:
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
        rx.el.label("Venue Name", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.input(
            on_change=lambda value: WizardState.update_form_field("venue_name", value),
            default_value=WizardState.form_data.get("venue_name", ""),
            placeholder="e.g., Expo Center Lahore",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        rx.el.label("City", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.input(
            on_change=lambda value: WizardState.update_form_field("city", value),
            default_value=WizardState.form_data.get("city", ""),
            placeholder="e.g., Lahore",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white",
        ),
        class_name="flex flex-col",
    )


def create_event_step_3() -> rx.Component:
    return rx.el.div(
        rx.el.label("Capacity", class_name="text-sm font-medium text-gray-300 mb-2"),
        rx.el.input(
            type="number",
            on_change=lambda value: WizardState.update_form_field("capacity", value),
            default_value=WizardState.form_data.get("capacity", "").to_string(),
            placeholder="e.g., 500",
            class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
        ),
        class_name="flex flex-col",
    )


def create_event_step_4() -> rx.Component:
    return rx.el.div(
        rx.el.label("Visibility", class_name="text-sm font-medium text-gray-300 mb-4"),
        rx.el.div(
            rx.foreach(
                ["public", "friends", "circles", "invite_only"],
                lambda option: rx.el.button(
                    option.replace("_", " ").title(),
                    on_click=lambda: WizardState.update_form_field(
                        "visibility_scope", option
                    ),
                    class_name=rx.cond(
                        WizardState.form_data.get("visibility_scope") == option,
                        "p-3 bg-teal-500 text-white rounded-lg font-semibold w-full capitalize",
                        "p-3 bg-gray-700 text-gray-300 rounded-lg w-full hover:bg-gray-600 capitalize",
                    ),
                ),
            ),
            class_name="grid grid-cols-2 gap-2",
        ),
        class_name="flex flex-col",
    )


def create_event_step_5() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Is this a ticketed event?",
            class_name="text-sm font-medium text-gray-300 mb-2",
        ),
        rx.el.div(
            rx.el.input(
                type="checkbox",
                on_change=lambda checked: WizardState.update_form_field(
                    "ticketed", checked
                ),
                default_checked=WizardState.form_data.get("ticketed", False).to(bool),
                class_name="h-4 w-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500",
            ),
            rx.el.label(
                "Yes, this event requires tickets",
                class_name="ml-2 text-sm text-gray-300",
            ),
            class_name="flex items-center mb-4",
        ),
        rx.cond(
            WizardState.form_data.get("ticketed").to(bool),
            rx.el.div(
                rx.el.label(
                    "Price (PKR)", class_name="text-sm font-medium text-gray-300 mb-2"
                ),
                rx.el.input(
                    type="number",
                    on_change=lambda value: WizardState.update_form_field(
                        "price_pkr", value
                    ),
                    default_value=WizardState.form_data.get(
                        "price_pkr", ""
                    ).to_string(),
                    placeholder="e.g., 2500",
                    class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white mb-4",
                ),
                rx.el.label(
                    "Ticket Quantity",
                    class_name="text-sm font-medium text-gray-300 mb-2",
                ),
                rx.el.input(
                    type="number",
                    on_change=lambda value: WizardState.update_form_field(
                        "ticket_qty", value
                    ),
                    default_value=WizardState.form_data.get(
                        "ticket_qty", ""
                    ).to_string(),
                    placeholder="e.g., 100",
                    class_name="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg text-white",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "This will be a free event.",
                    class_name="text-sm text-gray-400 p-3 bg-gray-800 rounded-lg border border-gray-700",
                )
            ),
        ),
        class_name="flex flex-col",
    )


def create_event_step_6() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Preview", class_name="text-lg font-bold text-white mb-4"),
        rx.el.div(
            rx.image(
                src=rx.cond(
                    WizardState.form_data.get("poster_url"),
                    rx.get_upload_url(
                        WizardState.form_data.get("poster_url").to_string()
                    ),
                    "/placeholder.svg",
                ),
                class_name="w-full h-64 object-cover rounded-lg mb-4",
            ),
            rx.el.p(
                "Title: ",
                WizardState.form_data.get("title", ""),
                class_name="text-white",
            ),
            rx.el.p(
                f"When: {WizardState.form_data.get('date', '')} at {WizardState.form_data.get('start_time', '')}",
                class_name="text-gray-400",
            ),
            rx.el.p(
                f"Venue: {WizardState.form_data.get('venue_name', '')}, {WizardState.form_data.get('city', '')}",
                class_name="text-gray-400",
            ),
            rx.el.p(
                "Capacity: ",
                WizardState.form_data.get("capacity", ""),
                class_name="text-gray-400",
            ),
            rx.el.p(
                "Visibility: ",
                WizardState.form_data.get("visibility_scope", "")
                .to_string()
                .capitalize(),
                class_name="text-gray-400",
            ),
            rx.cond(
                WizardState.form_data.get("ticketed").to(bool),
                rx.el.p(
                    f"Tickets: {WizardState.form_data.get('ticket_qty', '')} at PKR {WizardState.form_data.get('price_pkr', '')}",
                    class_name="text-gray-400",
                ),
                rx.el.p("Free Event", class_name="text-gray-400"),
            ),
            class_name="space-y-2 p-4 bg-gray-800 rounded-lg",
        ),
        class_name="flex flex-col",
    )


def create_event_wizard_content() -> rx.Component:
    return rx.el.div(
        wizard_progress_indicator(),
        rx.el.div(
            rx.match(
                WizardState.current_step,
                (0, create_event_step_1()),
                (1, create_event_step_2()),
                (2, create_event_step_3()),
                (3, create_event_step_4()),
                (4, create_event_step_5()),
                (5, create_event_step_6()),
                rx.el.p("Invalid step"),
            ),
            class_name="p-4",
        ),
        class_name="flex-grow overflow-y-auto",
    )


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
                is_loading=WizardState.is_publishing,
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