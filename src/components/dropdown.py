from dash import html, dcc


def dropdown(id=None, options=None, value=None, placeholder="Select an option...",
             multi=False, searchable=True, clearable=True, disabled=False,
             label=None, helper_text=None, error_message=None, required=False,
             className="", **kwargs):
    """
    ShadCN UI-inspired dropdown component

    Args:
        id: Dropdown ID for callbacks
        options: List of options [{"label": "Label", "value": "value"}, ...]
        value: Current selected value(s)
        placeholder: Placeholder text
        multi: Boolean for multi-select
        searchable: Boolean for search functionality
        clearable: Boolean for clear button
        disabled: Boolean to disable dropdown
        label: Label text
        helper_text: Helper text below dropdown
        error_message: Error message (shows red styling)
        required: Boolean for required field
        className: Additional CSS classes
    """

    if options is None:
        options = []

    # Custom styling for the dropdown
    dropdown_style = {
        'control': {
            'border': '1px solid #d1d5db' if not error_message else '1px solid #ef4444',
            'borderRadius': '6px',
            'minHeight': '40px',
            'boxShadow': 'none',
            '&:hover': {
                'border': '1px solid #9ca3af' if not error_message else '1px solid #ef4444'
            },
            '&:focus-within': {
                'border': '2px solid #3b82f6' if not error_message else '2px solid #ef4444',
                'boxShadow': '0 0 0 2px rgba(59, 130, 246, 0.1)' if not error_message else '0 0 0 2px rgba(239, 68, 68, 0.1)'
            }
        },
        'placeholder': {
            'color': '#6b7280',
            'fontSize': '14px'
        },
        'singleValue': {
            'color': '#111827',
            'fontSize': '14px'
        },
        'multiValue': {
            'backgroundColor': '#f3f4f6',
            'borderRadius': '4px'
        },
        'multiValueLabel': {
            'color': '#374151',
            'fontSize': '14px'
        },
        'option': {
            'fontSize': '14px',
            'padding': '8px 12px',
            '&:hover': {
                'backgroundColor': '#f3f4f6'
            }
        },
        'menu': {
            'borderRadius': '6px',
            'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            'border': '1px solid #e5e7eb'
        }
    }

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
                className=label_classes
            )
        )

    # Dropdown
    dropdown_component = dcc.Dropdown(
        id=id,
        options=options,
        value=value,
        placeholder=placeholder,
        multi=multi,
        searchable=searchable,
        clearable=clearable,
        disabled=disabled,
        style=dropdown_style,
        className=className,
        **kwargs
    )

    components.append(dropdown_component)

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


def select(id=None, options=None, value=None, placeholder="Select...", **kwargs):
    """Simple select dropdown shorthand"""
    return dropdown(
        id=id,
        options=options,
        value=value,
        placeholder=placeholder,
        multi=False,
        searchable=False,
        clearable=False,
        **kwargs
    )


def multi_select(id=None, options=None, value=None, placeholder="Select multiple...", **kwargs):
    """Multi-select dropdown shorthand"""
    return dropdown(
        id=id,
        options=options,
        value=value,
        placeholder=placeholder,
        multi=True,
        searchable=True,
        clearable=True,
        **kwargs
    )


def searchable_dropdown(id=None, options=None, value=None, placeholder="Search and select...", **kwargs):
    """Searchable dropdown shorthand"""
    return dropdown(
        id=id,
        options=options,
        value=value,
        placeholder=placeholder,
        multi=False,
        searchable=True,
        clearable=True,
        **kwargs
    )


# Helper function to create options easily
def create_options(items):
    """
    Create options from various input formats

    Args:
        items: Can be:
            - List of strings: ["Option 1", "Option 2"]
            - List of dicts: [{"label": "Option 1", "value": "opt1"}, ...]
            - Dict: {"opt1": "Option 1", "opt2": "Option 2"}
    """
    if isinstance(items, list):
        if all(isinstance(item, str) for item in items):
            # List of strings
            return [{"label": item, "value": item} for item in items]
        elif all(isinstance(item, dict) for item in items):
            # List of dicts (already in correct format)
            return items
    elif isinstance(items, dict):
        # Dict format
        return [{"label": label, "value": value} for value, label in items.items()]

    return []
