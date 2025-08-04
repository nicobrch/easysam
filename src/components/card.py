from dash import html


def card(children=None, className="", **kwargs):
    """
    Base card component with ShadCN UI styling
    """
    base_classes = "bg-white border border-gray-200 rounded-lg shadow-sm"
    combined_classes = f"{base_classes} {className}".strip()

    return html.Div(
        children=children,
        className=combined_classes,
        **kwargs
    )


def card_header(children=None, className="", **kwargs):
    """Card header component"""
    base_classes = "px-4 py-3 border-b border-gray-200"
    combined_classes = f"{base_classes} {className}".strip()

    return html.Div(
        children=children,
        className=combined_classes,
        **kwargs
    )


def card_content(children=None, className="", **kwargs):
    """Card content component"""
    base_classes = "px-4 py-3"
    combined_classes = f"{base_classes} {className}".strip()

    return html.Div(
        children=children,
        className=combined_classes,
        **kwargs
    )


def card_footer(children=None, className="", **kwargs):
    """Card footer component"""
    base_classes = "px-4 py-3 border-t border-gray-200 bg-gray-50/50"
    combined_classes = f"{base_classes} {className}".strip()

    return html.Div(
        children=children,
        className=combined_classes,
        **kwargs
    )


def card_title(text, className="", **kwargs):
    """Card title component"""
    base_classes = "text-base font-semibold text-gray-900"
    combined_classes = f"{base_classes} {className}".strip()

    return html.H3(
        text,
        className=combined_classes,
        **kwargs
    )


def card_description(text, className="", **kwargs):
    """Card description component"""
    base_classes = "text-xs text-gray-600 mt-1"
    combined_classes = f"{base_classes} {className}".strip()

    return html.P(
        text,
        className=combined_classes,
        **kwargs
    )


def text_card(title, description=None, content=None, footer=None, className="", **kwargs):
    """
    Simple text-only card
    """
    children = []

    # Header with title and description
    if title or description:
        header_content = []
        if title:
            header_content.append(card_title(title))
        if description:
            header_content.append(card_description(description))
        children.append(card_header(header_content))

    # Content
    if content:
        children.append(card_content(content))

    # Footer
    if footer:
        children.append(card_footer(footer))

    return card(children, className, **kwargs)


def image_card(image_src, image_alt="", title=None, description=None, content=None,
               footer=None, className="", **kwargs):
    """
    Card with image and optional text content
    """
    children = []

    # Image
    children.append(
        html.Div([
            html.Img(
                src=image_src,
                alt=image_alt,
                className="w-full h-48 object-cover rounded-t-lg"
            )
        ])
    )

    # Header with title and description
    if title or description:
        header_content = []
        if title:
            header_content.append(card_title(title))
        if description:
            header_content.append(card_description(description))
        children.append(card_header(header_content, className="border-t-0"))

    # Content
    if content:
        children.append(card_content(content))

    # Footer
    if footer:
        children.append(card_footer(footer))

    return card(children, className, **kwargs)


def action_card(title, description=None, content=None, actions=None,
                image_src=None, image_alt="", className="", **kwargs):
    """
    Card with actions/buttons
    """
    children = []

    # Image (optional)
    if image_src:
        children.append(
            html.Div([
                html.Img(
                    src=image_src,
                    alt=image_alt,
                    className="w-full h-48 object-cover rounded-t-lg"
                )
            ])
        )

    # Header with title and description
    if title or description:
        header_content = []
        if title:
            header_content.append(card_title(title))
        if description:
            header_content.append(card_description(description))
        children.append(card_header(
            header_content, className="border-t-0" if image_src else ""))

    # Content
    if content:
        children.append(card_content(content))

    # Footer with actions
    if actions:
        footer_content = html.Div(
            actions,
            className="flex gap-2 justify-end"
        )
        children.append(card_footer(footer_content))

    return card(children, className, **kwargs)
