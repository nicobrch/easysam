import dash
from dash import html, dcc
from layout import playground_layout, main_content_section, sidebar_section
from components import button, input_field

# Register the page with a variable path template to capture image_id
dash.register_page(__name__, path_template="/image-label/<image_id>")


def layout(image_id=None, **kwargs):
    """
    Image labeling page layout

    Args:
        image_id: The image ID captured from the URL path
        **kwargs: Additional keyword arguments
    """

    # Left column content (main content)
    left_content = main_content_section([
        # Image display with rounded corners
        html.Div([
            html.Img(
                src="https://picsum.photos/1280/720?random=1",
                className="w-full h-auto rounded-lg shadow-md hover:cursor-crosshair",
                style={"maxHeight": "720px", "objectFit": "contain"}
            )
        ], className="mt-4")
    ], title=f"Image {image_id or 'Not Found'}")

    # Right column content (sidebar with options)
    right_content = html.Div([
        sidebar_section([
            html.P("Labeling Tools", className="text-sm text-gray-600 mb-3"),
            html.Div([
                button("Add Label", size="sm", className="mb-2 w-full"),
                button("Delete Label", variant="outline",
                       size="sm", className="mb-2 w-full"),
                button("Clear All", variant="destructive",
                       size="sm", className="w-full")
            ])
        ], title="Actions"),

        sidebar_section([
            html.Div([
                html.Label(
                    "Label Name:", className="block text-sm font-medium text-gray-700 mb-1"),
                input_field(
                    id="label-name-input",
                    placeholder="Enter label name...",
                    className="mb-3"
                )
            ])
        ], title="Label Properties"),

        sidebar_section([
            html.Div([
                html.P("Current Labels:",
                       className="text-sm font-medium text-gray-700 mb-2"),
                html.Div([
                    html.Div([
                        html.Span("Object 1", className="text-sm"),
                        html.Button(
                            "×", className="ml-2 text-red-500 hover:text-red-700")
                    ], className="flex justify-between items-center p-2 bg-gray-50 rounded mb-1"),
                    html.Div([
                        html.Span("Object 2", className="text-sm"),
                        html.Button(
                            "×", className="ml-2 text-red-500 hover:text-red-700")
                    ], className="flex justify-between items-center p-2 bg-gray-50 rounded mb-1")
                ], className="max-h-40 overflow-y-auto")
            ])
        ], title="Labels")
    ], className="h-full")

    return playground_layout(
        left_content=left_content,
        right_content=right_content
    )
