from dash import html, dcc


def input_field(id=None, type="text", placeholder="", value="", disabled=False,
                label=None, helper_text=None, error_message=None, required=False,
                className="", **kwargs):
    """
    ShadCN UI-inspired input component

    Args:
        id: Input ID for callbacks
        type: Input type ("text", "email", "password", "number", etc.)
        placeholder: Placeholder text
        value: Current value
        disabled: Boolean to disable input
        label: Label text
        helper_text: Helper text below input
        error_message: Error message (shows red styling)
        required: Boolean for required field
        className: Additional CSS classes
    """

    # Base input classes
    base_classes = "flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"

    # Error state classes
    if error_message:
        error_classes = "border-red-500 focus-visible:ring-red-500"
        base_classes = base_classes.replace("border-gray-300", "border-red-500").replace(
            "focus-visible:ring-blue-500", "focus-visible:ring-red-500")

    combined_classes = f"{base_classes} {className}".strip()

    # Create input element
    if type == "number":
        input_element = dcc.Input(
            id=id,
            type="number",
            placeholder=placeholder,
            value=value,
            disabled=disabled,
            required=required,
            className=combined_classes,
            **kwargs
        )
    else:
        input_element = dcc.Input(
            id=id,
            type=type,
            placeholder=placeholder,
            value=value,
            disabled=disabled,
            required=required,
            className=combined_classes,
            **kwargs
        )

    # Build the complete component
    components = []

    # Label
    if label:
        label_classes = "text-sm font-medium text-gray-700 mb-2 block"
        if required:
            label_content = [label, html.Span(" *", className="text-red-500")]
        else:
            label_content = label

        components.append(
            html.Label(
                label_content,
                htmlFor=id,
                className=label_classes
            )
        )

    # Input
    components.append(input_element)

    # Helper text or error message
    if helper_text and not error_message:
        components.append(
            html.P(
                helper_text,
                className="text-xs text-gray-600 mt-1"
            )
        )

    if error_message:
        components.append(
            html.P(
                error_message,
                className="text-xs text-red-600 mt-1"
            )
        )

    return html.Div(components, className="space-y-1")


def text_input(id=None, placeholder="Enter text...", **kwargs):
    """Text input shorthand"""
    return input_field(id=id, type="text", placeholder=placeholder, **kwargs)


def email_input(id=None, placeholder="Enter email...", **kwargs):
    """Email input shorthand"""
    return input_field(id=id, type="email", placeholder=placeholder, **kwargs)


def password_input(id=None, placeholder="Enter password...", **kwargs):
    """Password input shorthand"""
    return input_field(id=id, type="password", placeholder=placeholder, **kwargs)


def number_input(id=None, placeholder="Enter number...", **kwargs):
    """Number input shorthand"""
    return input_field(id=id, type="number", placeholder=placeholder, **kwargs)


def search_input(id=None, placeholder="Search...", **kwargs):
    """Search input shorthand"""
    return input_field(id=id, type="search", placeholder=placeholder, **kwargs)


def textarea(id=None, placeholder="Enter text...", value="", rows=3, disabled=False,
             label=None, helper_text=None, error_message=None, required=False,
             className="", **kwargs):
    """
    Textarea component
    """
    base_classes = "flex min-h-[80px] w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none"

    if error_message:
        base_classes = base_classes.replace("border-gray-300", "border-red-500").replace(
            "focus-visible:ring-blue-500", "focus-visible:ring-red-500")

    combined_classes = f"{base_classes} {className}".strip()

    # Build the complete component
    components = []

    # Label
    if label:
        label_classes = "text-sm font-medium text-gray-700 mb-2 block"
        if required:
            label_content = [label, html.Span(" *", className="text-red-500")]
        else:
            label_content = label

        components.append(
            html.Label(
                label_content,
                htmlFor=id,
                className=label_classes
            )
        )

    # Textarea
    components.append(
        dcc.Textarea(
            id=id,
            placeholder=placeholder,
            value=value,
            disabled=disabled,
            rows=rows,
            className=combined_classes,
            **kwargs
        )
    )

    # Helper text or error message
    if helper_text and not error_message:
        components.append(
            html.P(
                helper_text,
                className="text-xs text-gray-600 mt-1"
            )
        )

    if error_message:
        components.append(
            html.P(
                error_message,
                className="text-xs text-red-600 mt-1"
            )
        )

    return html.Div(components, className="space-y-1")
