from dash import html


def playground_layout(left_content, right_content, className="", **kwargs):
    """
    Playground layout component with two columns - large left and smaller right

    Args:
        left_content: Content for the left (main) column
        right_content: Content for the right (sidebar) column
        className: Additional CSS classes for the outer container
        **kwargs: Additional props for the outer container
    """
    return html.Div([
        html.Div([
            # Left column (main content) - takes 2/3 of the space
            html.Div(
                left_content,
                className="bg-white rounded-lg p-6 shadow-sm lg:col-span-3"
            ),
            # Right column (sidebar) - takes 1/3 of the space
            html.Div(
                right_content,
                className="bg-white rounded-lg p-6 shadow-sm lg:col-span-1 h-full min-h-[600px]"
            )
        ], className="grid grid-cols-1 lg:grid-cols-4 gap-6 max-w-8/10 mx-auto px-3 py-4 min-h-[calc(100vh-2rem)]")
    ], className=f"min-h-screen bg-gray-50 pt-4 {className}".strip(),
        style={"fontFamily": "Inter, sans-serif"}, **kwargs)


def sidebar_section(children, title=None, className="", **kwargs):
    """
    Sidebar section component for organizing sidebar content

    Args:
        children: Section content
        title: Optional section title
        className: Additional CSS classes
        **kwargs: Additional props
    """
    content = []

    # Add section title if provided
    if title:
        content.append(
            html.H3(title, className="text-md font-semibold text-gray-800 mb-3")
        )

    # Add children content
    if isinstance(children, list):
        content.extend(children)
    else:
        content.append(children)

    return html.Div(
        content,
        className=f"mb-4 {className}".strip(),
        **kwargs
    )


def main_content_section(children, title=None, className="", **kwargs):
    """
    Main content section component for the left column

    Args:
        children: Section content
        title: Optional section title
        className: Additional CSS classes
        **kwargs: Additional props
    """
    content = []

    # Add section title if provided
    if title:
        content.append(
            html.H1(title, className="text-3xl font-bold text-gray-900 mb-6")
        )

    # Add children content
    if isinstance(children, list):
        content.extend(children)
    else:
        content.append(children)

    return html.Div(
        content,
        className=f"{className}".strip(),
        **kwargs
    )
