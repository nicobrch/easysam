import dash
from dash import html, dcc, callback, Input, Output, State
from typing import NamedTuple, Optional
from pathlib import Path
import base64
from utils.frames import extract_frames
from utils.paths import get_original_frames_path, UPLOADS_DIR
from components import (
    text_card,
    primary_button, secondary_button,
    text_input, number_input,
    select, create_options,
    video_dropzone
)
from layout import page_layout, section, content_grid, flex_container

dash.register_page(__name__, path='/upload-video', name='Upload Video')


class VideoFormData(NamedTuple):
    """Data structure for video form inputs"""
    video_name: Optional[str]
    resolution: Optional[str]
    frame_step: Optional[int]


def validate_form_data(form_data: VideoFormData) -> tuple[bool, list[str]]:
    """
    Validate form data and return validation status and error messages

    Args:
        form_data: VideoFormData instance with form values

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    # Validate video name
    if not form_data.video_name or not form_data.video_name.strip():
        errors.append("Video name is required")
    elif len(form_data.video_name.strip()) < 3:
        errors.append("Video name must be at least 3 characters")

    # Validate resolution
    if not form_data.resolution:
        errors.append("Video resolution is required")

    # Validate frame step
    if form_data.frame_step is None:
        errors.append("Frame step is required")
    elif form_data.frame_step < 1 or form_data.frame_step > 30:
        errors.append("Frame step must be between 1 and 30")

    return len(errors) == 0, errors


# Video resolution options (16:9 aspect ratio)
resolution_options = create_options({
    "1920x1080": "1920×1080 (Full HD)",
    "1280x720": "1280×720 (HD)",
})

layout = page_layout([
    # Hidden location component for redirects
    dcc.Location(id="page-redirect", refresh=True),
    section([
        html.Div([
            # Upload Zone
            html.Div([
                video_dropzone(id='video-upload')
            ], id="upload-zone", className="mb-6"),

            # Upload Status
            dcc.Loading(
                id="processing-loading",
                type="default",
                children=html.Div(id="upload-status", className="mb-6"),
            ),

            # Form Section (initially hidden)
            html.Div([
                text_card(
                    title="Video Configuration",
                    content=html.Div([
                        # Validation errors display
                        html.Div(id="validation-errors", className="mb-4"),

                        content_grid([
                            text_input(
                                id="video-name-input",
                                label="Video Name",
                                placeholder="Enter a name for your video",
                                helper_text="This will be used to identify your video",
                                required=True
                            ),
                            select(
                                id="resolution-select",
                                label="Video Resolution",
                                options=resolution_options,
                                placeholder="Select resolution...",
                                value="1920x1080",
                                required=True
                            )
                        ], cols=2, className="mb-4"),

                        number_input(
                            id="frame-step-input",
                            label="Frame Step",
                            placeholder="Enter frame step (e.g., 4)",
                            helper_text="Process every Nth frame (higher values = faster processing, lower accuracy)",
                            value=4,
                            min=1,
                            max=30,
                            required=True
                        ),

                        flex_container([
                            secondary_button("Cancel", id="cancel-btn"),
                            primary_button("Process Video",
                                           id="process-btn")
                        ], justify="justify-end", className="mt-6")
                    ])
                )
            ], id="video-form", style={"display": "none"})
        ])
    ], title="Upload Video")
], title="Video Upload")


@callback(
    [Output('upload-status', 'children'),
     Output('video-form', 'style'),
     Output('video-name-input', 'value')],
    [Input('video-upload', 'contents')],
    [State('video-upload', 'filename')]
)
def handle_video_upload(contents, filename):
    if contents is None:
        return "", {"display": "none"}, ""

    # Show upload success message
    status_message = html.Div([
        html.Div([
            html.I(className="fas fa-check-circle text-green-500 text-xl mr-3"),
            html.Div([
                html.H4(f"✓ {filename}",
                        className="text-sm font-medium text-gray-900"),
                html.P("Video uploaded successfully",
                       className="text-xs text-gray-600")
            ])
        ], className="flex items-center")
    ], className="bg-green-50 border border-green-200 rounded-lg p-4")

    # Extract filename without extension for default name
    default_name = filename.rsplit('.', 1)[0] if filename else ""

    return status_message, {"display": "block"}, default_name


@callback(
    [Output('process-btn', 'disabled'),
     Output('validation-errors', 'children')],
    [Input('video-name-input', 'value'),
     Input('resolution-select', 'value'),
     Input('frame-step-input', 'value')],
    prevent_initial_call=False
)
def validate_form_inputs(video_name, resolution, frame_step):
    """Validate form inputs and enable/disable the process button accordingly"""

    # Create form data object
    form_data = VideoFormData(
        video_name=video_name,
        resolution=resolution,
        frame_step=frame_step
    )

    # Validate the form
    is_valid, errors = validate_form_data(form_data)

    # Create error message component if there are errors
    error_component = None
    if errors:
        error_component = html.Div([
            html.Div([
                html.I(
                    className="fas fa-exclamation-triangle text-red-500 text-sm mr-2"),
                html.Span("Please fix the following issues:",
                          className="text-sm font-medium text-red-800")
            ], className="flex items-center mb-2"),
            html.Ul([
                html.Li(error, className="text-sm text-red-700") for error in errors
            ], className="list-disc list-inside space-y-1 ml-6")
        ], className="bg-red-50 border border-red-200 rounded-lg p-3")

    # Button should be disabled if form is invalid
    button_disabled = not is_valid

    return button_disabled, error_component


@callback(
    [Output('upload-zone', 'children'),
     Output('upload-status', 'children', allow_duplicate=True),
     Output('video-form', 'style', allow_duplicate=True),
     Output('process-btn', 'disabled', allow_duplicate=True),
     Output('validation-errors', 'children', allow_duplicate=True),
     Output('video-name-input', 'value', allow_duplicate=True),
     Output('frame-step-input', 'value', allow_duplicate=True),
     Output('resolution-select', 'value', allow_duplicate=True)],
    [Input('cancel-btn', 'n_clicks')],
    prevent_initial_call=True
)
def handle_cancel(n_clicks):
    if n_clicks:
        # Re-mount the dropzone and reset all UI to initial state without touching styles
        return (
            [video_dropzone(id='video-upload')],  # reset upload zone
            "",                                 # clear upload status
            {"display": "none"},               # hide form
            True,                                 # disable process button
            "",                                 # clear validation errors
            "",                                 # clear video name
            4,                                    # reset frame step
            "1920x1080",                        # reset resolution
        )

    return (
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
        dash.no_update,
    )


@callback(
    [
        Output('upload-status', 'children', allow_duplicate=True),
        Output('page-redirect', 'href')
    ],
    [Input('process-btn', 'n_clicks')],
    [State('video-name-input', 'value'),
     State('resolution-select', 'value'),
     State('frame-step-input', 'value'),
     State('video-upload', 'contents'),
     State('video-upload', 'filename')],
    prevent_initial_call=True
)
def handle_process_video(n_clicks, video_name, resolution, frame_step, upload_contents, upload_filename):
    if not n_clicks:
        return dash.no_update, dash.no_update

    # Create and validate form data
    form_data = VideoFormData(
        video_name=video_name,
        resolution=resolution,
        frame_step=frame_step
    )

    is_valid, errors = validate_form_data(form_data)

    if not is_valid:
        # Show validation error if form is somehow invalid
        error_message = html.Div([
            html.Div([
                html.I(
                    className="fas fa-exclamation-triangle text-red-500 text-xl mr-3"),
                html.Div([
                    html.H4("Validation Error",
                            className="text-sm font-medium text-gray-900"),
                    html.P("Please check your input values",
                           className="text-xs text-gray-600")
                ])
            ], className="flex items-center")
        ], className="bg-red-50 border border-red-200 rounded-lg p-4")
        return error_message, dash.no_update

    # Ensure a video is uploaded
    if not upload_contents or not upload_filename:
        error_message = html.Div([
            html.Div([
                html.I(
                    className="fas fa-exclamation-triangle text-red-500 text-xl mr-3"),
                html.Div([
                    html.H4("No video to process",
                            className="text-sm font-medium text-gray-900"),
                    html.P("Please upload a video before processing.",
                           className="text-xs text-gray-600")
                ])
            ], className="flex items-center")
        ], className="bg-red-50 border border-red-200 rounded-lg p-4")
        return error_message, dash.no_update

    # Decode and persist the uploaded video to disk
    try:
        header, b64data = upload_contents.split(',', 1)
        video_bytes = base64.b64decode(b64data)
        ext = Path(upload_filename).suffix or ".mp4"
        video_dir = Path(UPLOADS_DIR) / video_name
        video_dir.mkdir(parents=True, exist_ok=True)
        video_path = video_dir / f"{video_name}{ext}"
        with open(video_path, 'wb') as f:
            f.write(video_bytes)
    except Exception as e:
        error_message = html.Div([
            html.Div([
                html.I(
                    className="fas fa-exclamation-triangle text-red-500 text-xl mr-3"),
                html.Div([
                    html.H4("Failed to save upload",
                            className="text-sm font-medium text-gray-900"),
                    html.P(str(e), className="text-xs text-gray-600")
                ])
            ], className="flex items-center")
        ], className="bg-red-50 border border-red-200 rounded-lg p-4")
        return error_message, dash.no_update

    # Run frame extraction to the original frames path
    try:
        output_dir = get_original_frames_path(video_name)
        extract_frames(video_path=video_path,
                       output_dir=output_dir, frame_step=frame_step)
    except Exception as e:
        error_message = html.Div([
            html.Div([
                html.I(
                    className="fas fa-exclamation-triangle text-red-500 text-xl mr-3"),
                html.Div([
                    html.H4("Frame extraction failed",
                            className="text-sm font-medium text-gray-900"),
                    html.P(str(e), className="text-xs text-gray-600")
                ])
            ], className="flex items-center")
        ], className="bg-red-50 border border-red-200 rounded-lg p-4")
        return error_message, dash.no_update

    # Success: optional message and redirect
    success_message = html.Div([
        html.Div([
            html.I(className="fas fa-check-circle text-green-500 text-xl mr-3"),
            html.Div([
                html.H4("Video processed",
                        className="text-sm font-medium text-gray-900"),
                html.P("Redirecting to home...",
                       className="text-xs text-gray-600")
            ])
        ], className="flex items-center")
    ], className="bg-green-50 border border-green-200 rounded-lg p-4")

    # Redirect to index page
    return success_message, "/"
