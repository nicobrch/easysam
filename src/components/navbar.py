import dash
from dash import html, dcc, Input, Output, callback


def create_navbar():
    """Create and return the navbar component"""
    return html.Div([
        # Navigation Bar
        html.Nav([
            html.Div([
                # Logo/Brand
                html.Div([
                    html.H1("EasySAM", className="text-2xl font-bold text-white")
                ], className="flex items-center"),

                # Navigation Links
                html.Div([
                    html.Div([
                        dcc.Link(
                            page['name'],
                            href=page["relative_path"],
                            className="text-white hover:text-blue-200 transition-colors duration-200 px-3 py-2 rounded-md text-sm font-medium"
                        ) for page in dash.page_registry.values()
                    ], className="flex space-x-4")
                ], className="hidden md:block"),

                # Mobile menu button
                html.Button([
                    html.Span("☰", className="text-xl")
                ], className="md:hidden text-white hover:text-blue-200 focus:outline-none p-2", id="mobile-menu-button")
            ], className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16")
        ], className="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg"),

        # Mobile Navigation Menu (hidden by default)
        html.Div([
            html.Div([
                dcc.Link(
                    page['name'],
                    href=page["relative_path"],
                    className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium"
                ) for page in dash.page_registry.values()
            ], className="px-2 pt-2 pb-3 space-y-1")
        ], className="md:hidden bg-blue-700", id="mobile-menu", style={"display": "none"})
    ], style={"fontFamily": "Inter, sans-serif"})


# Callback for mobile menu toggle
@callback(
    Output('mobile-menu', 'style'),
    Input('mobile-menu-button', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_mobile_menu(n_clicks):
    """Toggle the mobile menu visibility"""
    if n_clicks and n_clicks % 2 == 1:
        return {"display": "block"}
    return {"display": "none"}
