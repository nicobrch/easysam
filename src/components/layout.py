from dash import html


def page_layout(children, title=None, className="", **kwargs):
    """
    Common page layout component for consistent styling across pages

    Args:
        children: Page content
        title: Optional page title (H1)
        className: Additional CSS classes for the content container
        **kwargs: Additional props for the outer container
    """
    content = []

    # Add title if provided
    if title:
        content.append(
            html.H1(title, className="text-4xl font-bold text-gray-900 mb-8")
        )

    # Add children content
    if isinstance(children, list):
        content.extend(children)
    else:
        content.append(children)

    return html.Div([
        html.Div(
            content,
            className=f"max-w-9/10 mx-auto px-2 py-8 {className}".strip()
        )
    ], className="min-h-screen bg-gray-50 pt-2", style={"fontFamily": "Inter, sans-serif"}, **kwargs)


def section(children, title=None, className="", **kwargs):
    """
    Common section component for organizing page content

    Args:
        children: Section content
        title: Optional section title (H2)
        className: Additional CSS classes
        **kwargs: Additional props
    """
    content = []

    # Add section title if provided
    if title:
        content.append(
            html.H2(title, className="text-2xl font-semibold text-gray-800 mb-4")
        )

    # Add children content
    if isinstance(children, list):
        content.extend(children)
    else:
        content.append(children)

    return html.Section(
        content,
        className=f"mb-8 {className}".strip(),
        **kwargs
    )


def content_grid(children, cols=1, gap="gap-4", className="", **kwargs):
    """
    Common grid layout for content

    Args:
        children: Grid items
        cols: Number of columns (1, 2, 3, 4)
        gap: Gap size class
        className: Additional CSS classes
    """
    col_classes = {
        1: "grid-cols-1",
        2: "grid-cols-1 md:grid-cols-2",
        3: "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
        4: "grid-cols-1 md:grid-cols-2 lg:grid-cols-4"
    }

    grid_classes = f"grid {col_classes.get(cols, 'grid-cols-1')} {gap}"

    return html.Div(
        children,
        className=f"{grid_classes} {className}".strip(),
        **kwargs
    )


def flex_container(children, direction="row", gap="gap-4", justify="justify-start",
                   align="items-start", wrap=True, className="", **kwargs):
    """
    Common flex container for layouts

    Args:
        children: Flex items
        direction: "row" or "col"
        gap: Gap size class
        justify: Justify content class
        align: Align items class
        wrap: Whether to wrap items
        className: Additional CSS classes
    """
    flex_classes = [
        "flex",
        f"flex-{direction}",
        gap,
        justify,
        align
    ]

    if wrap and direction == "row":
        flex_classes.append("flex-wrap")

    return html.Div(
        children,
        className=f"{' '.join(flex_classes)} {className}".strip(),
        **kwargs
    )
