from dash import html


def button(children, variant="primary", size="default", disabled=False,
           className="", id=None, n_clicks=0, **kwargs):
    """
    ShadCN UI-inspired button component

    Args:
        children: Button content (text, icons, etc.)
        variant: "primary", "secondary", "destructive", "outline", "ghost", "link"
        size: "default", "sm", "lg", "icon"
        disabled: Boolean to disable the button
        className: Additional CSS classes
        id: Button ID for callbacks
        n_clicks: For Dash callbacks
    """

    # Base button classes
    base_classes = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"

    # Variant classes
    variant_classes = {
        "primary": "bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800",
        "secondary": "bg-gray-100 text-gray-900 hover:bg-gray-200 active:bg-gray-300",
        "destructive": "bg-red-600 text-white hover:bg-red-700 active:bg-red-800",
        "outline": "border border-gray-300 bg-transparent text-gray-700 hover:bg-gray-50 active:bg-gray-100",
        "ghost": "text-gray-700 hover:bg-gray-100 active:bg-gray-200",
        "link": "text-blue-600 underline-offset-4 hover:underline active:no-underline"
    }

    # Size classes
    size_classes = {
        "default": "h-10 px-4 py-2",
        "sm": "h-9 rounded-md px-3 text-xs",
        "lg": "h-11 rounded-md px-8",
        "icon": "h-10 w-10"
    }

    # Disabled classes
    disabled_classes = "opacity-50 cursor-not-allowed" if disabled else ""

    # Combine all classes
    combined_classes = f"{base_classes} {variant_classes.get(variant, variant_classes['primary'])} {size_classes.get(size, size_classes['default'])} {disabled_classes} {className}".strip()

    # Prepare props, only include id if it's provided
    button_props = {
        'className': combined_classes,
        'disabled': disabled,
        'n_clicks': n_clicks,
        **kwargs
    }
    
    if id is not None:
        button_props['id'] = id

    return html.Button(
        children,
        **button_props
    )


def primary_button(children, **kwargs):
    """Primary button shorthand"""
    return button(children, variant="primary", **kwargs)


def secondary_button(children, **kwargs):
    """Secondary button shorthand"""
    return button(children, variant="secondary", **kwargs)


def destructive_button(children, **kwargs):
    """Destructive button shorthand"""
    return button(children, variant="destructive", **kwargs)


def outline_button(children, **kwargs):
    """Outline button shorthand"""
    return button(children, variant="outline", **kwargs)


def ghost_button(children, **kwargs):
    """Ghost button shorthand"""
    return button(children, variant="ghost", **kwargs)


def link_button(children, **kwargs):
    """Link button shorthand"""
    return button(children, variant="link", **kwargs)


def icon_button(children, variant="primary", **kwargs):
    """Icon button shorthand"""
    return button(children, variant=variant, size="icon", **kwargs)
