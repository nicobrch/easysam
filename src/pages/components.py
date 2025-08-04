import dash
from dash import html, callback, Input, Output, State
from components import (
    text_card, image_card, action_card,
    primary_button, secondary_button, destructive_button, outline_button,
    text_input, number_input, email_input, password_input, textarea,
    dropdown, select, multi_select, create_options
)

dash.register_page(__name__, path='/components', name='Components')

# Sample data for dropdowns
fruit_options = create_options(
    ["Apple", "Banana", "Cherry", "Date", "Elderberry"])
color_options = create_options({
    "red": "Red",
    "blue": "Blue",
    "green": "Green",
    "yellow": "Yellow"
})

layout = html.Div([
    html.Div([
        html.H1('Component Showcase',
                className="text-4xl font-bold text-gray-900 mb-8"),

        # Buttons Section
        html.Section([
            html.H2('Buttons', className="text-2xl font-semibold text-gray-800 mb-4"),
            html.Div([
                text_card(
                    title="Button Variants",
                    content=html.Div([
                        html.Div([
                            primary_button("Primary", id="btn-primary"),
                            secondary_button("Secondary", id="btn-secondary"),
                            destructive_button(
                                "Destructive", id="btn-destructive"),
                            outline_button("Outline", id="btn-outline"),
                        ], className="flex gap-2 mb-4"),
                        html.Div([
                            primary_button("Disabled", disabled=True),
                            secondary_button("Small", size="sm"),
                            destructive_button("Large", size="lg"),
                        ], className="flex gap-2"),
                        html.Div(id="button-output",
                                 className="mt-4 p-2 bg-gray-100 rounded")
                    ])
                )
            ], className="mb-8")
        ]),

        # Cards Section
        html.Section([
            html.H2('Cards', className="text-2xl font-semibold text-gray-800 mb-4"),
            html.Div([
                # Text Card
                html.Div([
                    text_card(
                        title="Simple Text Card",
                        description="This is a basic card with just text content",
                        content=html.P(
                            "This card demonstrates the text-only variant with a title, description, and content area."),
                        footer=html.Span(
                            "Card footer", className="text-sm text-gray-500")
                    )
                ], className="w-full md:w-1/3"),

                # Image Card
                html.Div([
                    image_card(
                        image_src="https://picsum.photos/300/200?random=1",
                        image_alt="Sample image",
                        title="Image Card",
                        description="Card with image and text",
                        content=html.P(
                            "This card includes an image at the top with text content below.")
                    )
                ], className="w-full md:w-1/3"),

                # Action Card
                html.Div([
                    action_card(
                        title="Action Card",
                        description="Card with action buttons",
                        content=html.P(
                            "This card includes action buttons in the footer."),
                        actions=[
                            outline_button("Cancel"),
                            primary_button("Save")
                        ]
                    )
                ], className="w-full md:w-1/3")
            ], className="flex flex-col md:flex-row gap-4 mb-8")
        ]),

        # Inputs Section
        html.Section([
            html.H2('Input Fields',
                    className="text-2xl font-semibold text-gray-800 mb-4"),
            html.Div([
                text_card(
                    title="Form Inputs",
                    content=html.Div([
                        html.Div([
                            text_input(
                                id="text-input",
                                label="Full Name",
                                placeholder="Enter your full name",
                                helper_text="This will be displayed on your profile",
                                required=True
                            ),
                            email_input(
                                id="email-input",
                                label="Email Address",
                                placeholder="Enter your email",
                                required=True
                            )
                        ], className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"),

                        html.Div([
                            password_input(
                                id="password-input",
                                label="Password",
                                placeholder="Enter password",
                                required=True
                            ),
                            number_input(
                                id="number-input",
                                label="Age",
                                placeholder="Enter your age",
                                min=1,
                                max=120
                            )
                        ], className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"),

                        textarea(
                            id="textarea-input",
                            label="Bio",
                            placeholder="Tell us about yourself...",
                            rows=4,
                            helper_text="Maximum 500 characters"
                        )
                    ])
                )
            ], className="mb-8")
        ]),

        # Dropdowns Section
        html.Section([
            html.H2('Dropdowns',
                    className="text-2xl font-semibent text-gray-800 mb-4"),
            html.Div([
                text_card(
                    title="Dropdown Components",
                    content=html.Div([
                        html.Div([
                            select(
                                id="simple-select",
                                label="Favorite Fruit",
                                options=fruit_options,
                                placeholder="Choose a fruit...",
                                required=True
                            ),
                            dropdown(
                                id="searchable-dropdown",
                                label="Preferred Color",
                                options=color_options,
                                placeholder="Search colors...",
                                searchable=True,
                                clearable=True
                            )
                        ], className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"),

                        multi_select(
                            id="multi-select",
                            label="Skills",
                            options=create_options(
                                ["Python", "JavaScript", "React", "Dash", "Machine Learning", "Data Science"]),
                            placeholder="Select multiple skills...",
                            helper_text="Select all that apply"
                        ),

                        html.Div(id="dropdown-output",
                                 className="mt-4 p-2 bg-gray-100 rounded")
                    ])
                )
            ], className="mb-8")
        ])

    ], className="max-w-6xl mx-auto px-4 py-8")
], className="min-h-screen bg-gray-50", style={"fontFamily": "Inter, sans-serif"})


# Callbacks for interactivity
@callback(
    Output('button-output', 'children'),
    [Input('btn-primary', 'n_clicks'),
     Input('btn-secondary', 'n_clicks'),
     Input('btn-destructive', 'n_clicks'),
     Input('btn-outline', 'n_clicks')],
    prevent_initial_call=True
)
def handle_button_clicks(primary, secondary, destructive, outline):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "No button clicked yet"

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_names = {
        'btn-primary': 'Primary',
        'btn-secondary': 'Secondary',
        'btn-destructive': 'Destructive',
        'btn-outline': 'Outline'
    }

    return f"Last clicked: {button_names.get(button_id, 'Unknown')} button"


@callback(
    Output('dropdown-output', 'children'),
    [Input('simple-select', 'value'),
     Input('searchable-dropdown', 'value'),
     Input('multi-select', 'value')],
    prevent_initial_call=True
)
def handle_dropdown_changes(fruit, color, skills):
    output = []

    if fruit:
        output.append(html.P(f"Selected fruit: {fruit}"))
    if color:
        output.append(html.P(f"Selected color: {color}"))
    if skills:
        output.append(html.P(f"Selected skills: {', '.join(skills)}"))

    return output if output else "Make some selections to see output"
