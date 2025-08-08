import dash
from dash import html, dcc, Input, Output, callback, no_update, clientside_callback
import time
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
        # Image display with rounded corners wrapped in loading component
        html.Div([
            # Image with loading effect
            dcc.Loading([
                html.Img(
                    id="main-image",
                    src=dash.get_asset_url('uhK9rL.jpg'),
                    className="w-full h-auto rounded-lg shadow-md hover:cursor-crosshair",
                    style={"maxHeight": "720px", "objectFit": "contain"}
                )],
                overlay_style={"visibility": "visible", "filter": "blur(2px)"},
                type="cube",
            ),
            # Hidden div to store click data and trigger callback
            html.Div(id="image-click-data", style={"display": "none"}),
            html.Div(id="image-setup-trigger",
                     style={"display": "none"}, children="loaded"),
            # Button to trigger loading
            html.Div([
                button(
                    "Process Image",
                    id="process-image-btn",
                    variant="primary",
                    size="sm",
                    className="mt-3",
                    n_clicks=0
                )
            ], className="flex justify-center")
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


@callback(
    Output("main-image", "src"),
    Input("process-image-btn", "n_clicks"),
)
def process_image(n_clicks):
    if n_clicks and n_clicks > 0:
        time.sleep(2)  # Simulate processing time
        # Return the same image source (in a real app, this would be the processed image)
        return dash.get_asset_url('uhK9rL.jpg')
    return no_update


# Clientside callback to handle image clicks and log coordinates
clientside_callback(
    """
    function(src, trigger) {
        return new Promise((resolve) => {
            const img = document.getElementById('main-image');
            if (!img) {
                resolve('');
                return;
            }
            
            // Function to set up click handler
            const setupClickHandler = () => {
                // Remove existing event listener to avoid duplicates
                if (window.imageClickHandler) {
                    img.removeEventListener('click', window.imageClickHandler);
                }
                
                // Define the click handler
                window.imageClickHandler = function(event) {
                    const rect = img.getBoundingClientRect();
                    const clickX = event.clientX - rect.left;
                    const clickY = event.clientY - rect.top;
                    
                    // Get the actual image dimensions
                    const naturalWidth = img.naturalWidth;
                    const naturalHeight = img.naturalHeight;
                    
                    // Get the displayed image dimensions
                    const displayWidth = img.offsetWidth;
                    const displayHeight = img.offsetHeight;
                    
                    // Calculate the scale factors
                    const scaleX = naturalWidth / displayWidth;
                    const scaleY = naturalHeight / displayHeight;
                    
                    // Calculate relative coordinates (0-1 range)
                    const relativeX = clickX / displayWidth;
                    const relativeY = clickY / displayHeight;
                    
                    // Calculate absolute coordinates in original image resolution
                    const absoluteX = Math.round(clickX * scaleX);
                    const absoluteY = Math.round(clickY * scaleY);
                    
                    // Log to console
                    console.log('Image Click Coordinates:', {
                        'Display Position': { x: Math.round(clickX), y: Math.round(clickY) },
                        'Relative Position (0-1)': { x: parseFloat(relativeX.toFixed(4)), y: parseFloat(relativeY.toFixed(4)) },
                        'Absolute Position': { x: absoluteX, y: absoluteY },
                        'Image Dimensions': { 
                            natural: { width: naturalWidth, height: naturalHeight },
                            display: { width: displayWidth, height: displayHeight }
                        }
                    });
                };
                
                // Add the event listener
                img.addEventListener('click', window.imageClickHandler);
                console.log('Click handler set up for image');
                resolve('click-handler-ready');
            };
            
            // Check if image is already loaded
            if (img.complete && img.naturalHeight !== 0) {
                setupClickHandler();
            } else {
                // Wait for image to load
                img.onload = setupClickHandler;
            }
        });
    }
    """,
    Output("image-click-data", "children"),
    Input("main-image", "src"),
    Input("image-setup-trigger", "children")
)
