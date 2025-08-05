import dash
from dash import html, dcc, Input, Output, callback


def navbar(brand_name="EasySAM", brand_href="/", className="", **kwargs):
    """
    ShadCN UI-inspired navbar component

    Args:
        brand_name: Brand/logo text
        brand_href: Brand link URL
        className: Additional CSS classes
    """
    return html.Div([
        # Navigation Bar
        html.Nav([
            html.Div([
                # Logo/Brand
                html.Div([
                    dcc.Link(
                        brand_name,
                        href=brand_href,
                        className="text-lg font-bold text-white hover:text-blue-100 transition-colors duration-200"
                    )
                ], className="flex items-center"),

                # Navigation Links (centered)
                html.Div([
                    html.Div([
                        dcc.Link(
                            page['name'],
                            href=page["relative_path"],
                            className="text-white/90 hover:text-white transition-colors duration-200 px-2 py-1 rounded text-xs font-medium hover:bg-white/10"
                        ) for page in dash.page_registry.values()
                    ], className="flex space-x-1")
                ], className="hidden md:flex flex-1 justify-center"),

                # Mobile menu button (right side)
                html.Div([
                    html.Button([
                        html.Span("☰", className="text-base")
                    ], className="md:hidden text-white hover:text-blue-100 focus:outline-none focus:ring-1 focus:ring-white/20 p-1 rounded transition-colors", id="mobile-menu-button")
                ], className="flex items-center")
            ], className="max-w-full mx-auto px-3 sm:px-4 lg:px-6 flex items-center h-12")
        ], className=f"fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg border-b border-blue-500/20 {className}".strip()),

        # Mobile Navigation Menu (hidden by default)
        html.Div([
            html.Div([
                dcc.Link(
                    page['name'],
                    href=page["relative_path"],
                    className="text-white/90 hover:text-white hover:bg-white/10 block px-2 py-1 rounded text-xs font-medium transition-colors duration-200"
                ) for page in dash.page_registry.values()
            ], className="px-2 pt-1 pb-2 space-y-0.5")
        ], className="fixed top-12 left-0 right-0 z-40 md:hidden bg-blue-700/95 backdrop-blur-sm border-b border-blue-500/20", id="mobile-menu", style={"display": "none"})
    ], **kwargs)


def create_navbar():
    """Legacy function for backward compatibility"""
    return navbar()


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
