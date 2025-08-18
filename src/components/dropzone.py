from dash import html, dcc


def dropzone(id=None, accept="*", multiple=False, className="", children=None, **kwargs):
    """
    ShadCN UI-inspired dropzone component for file uploads

    Args:
        id: Upload component ID for callbacks
        accept: File types to accept (e.g., 'video/*', 'image/*', '.pdf')
        multiple: Boolean for multiple file selection
        className: Additional CSS classes
        children: Custom children content for the dropzone
        **kwargs: Additional props for dcc.Upload
    """

    default_style = {
        'width': '100%',
        'height': '300px',
        'lineHeight': '300px',
        'borderWidth': '2px',
        'borderStyle': 'dashed',
        'borderRadius': '8px',
        'borderColor': '#d1d5db',
        'textAlign': 'center',
        'backgroundColor': '#fafafa',
        'cursor': 'pointer',
        'transition': 'all 0.2s ease-in-out'
    }

    # Merge with any custom styles
    style = {**default_style, **kwargs.pop('style', {})}

    # Use custom children if provided, otherwise use default
    if children is None:
        children = html.Div([
            html.I(className="fas fa-cloud-upload-alt text-4xl text-gray-400 mb-4"),
            html.H3("Drag and drop a file here",
                    className="text-lg font-medium text-gray-700 mb-2"),
            html.P("or click to browse",
                   className="text-sm text-gray-500 mb-2"),
            html.P("Supports various file formats",
                   className="text-xs text-gray-400")
        ], className="flex flex-col items-center justify-center h-full")

    return dcc.Upload(
        id=id,
        children=children,
        style=style,
        multiple=multiple,
        accept=accept,
        className=className,
        **kwargs
    )


def video_dropzone(id=None, className="", **kwargs):
    """
    Specialized dropzone for video files

    Args:
        id: Upload component ID for callbacks
        className: Additional CSS classes
        **kwargs: Additional props for dropzone
    """

    # Override the children for video-specific messaging
    children = html.Div([
        html.I(className="fas fa-video text-4xl text-gray-400 mb-4"),
        html.H3("Drag and drop a video file here",
                className="text-lg font-medium text-gray-700 mb-2"),
        html.P("or click to browse",
               className="text-sm text-gray-500 mb-2"),
        html.P("Supports MP4, AVI, MOV files",
               className="text-xs text-gray-400")
    ], className="flex flex-col items-center justify-center h-full")

    return dropzone(
        id=id,
        accept='video/*',
        multiple=False,
        className=className,
        children=children,
        **kwargs
    )


def image_dropzone(id=None, className="", **kwargs):
    """
    Specialized dropzone for image files

    Args:
        id: Upload component ID for callbacks
        className: Additional CSS classes
        **kwargs: Additional props for dropzone
    """

    # Override the children for image-specific messaging
    children = html.Div([
        html.I(className="fas fa-image text-4xl text-gray-400 mb-4"),
        html.H3("Drag and drop an image file here",
                className="text-lg font-medium text-gray-700 mb-2"),
        html.P("or click to browse",
               className="text-sm text-gray-500 mb-2"),
        html.P("Supports JPG, PNG, GIF files",
               className="text-xs text-gray-400")
    ], className="flex flex-col items-center justify-center h-full")

    return dropzone(
        id=id,
        accept='image/*',
        multiple=False,
        className=className,
        children=children,
        **kwargs
    )
