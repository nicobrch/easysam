import dash
from dash import html
from layout import page_layout, section

dash.register_page(__name__, path='/', name='Home')

layout = page_layout([
    html.P('This is your home page with a beautiful navigation bar.',
           className="text-sm text-gray-600 mb-4"),

    section([
        html.Div([
            html.Ul([
                html.Li('🎨 Beautiful TailwindCSS styling',
                        className="text-gray-700 mb-1 text-sm"),
                html.Li('📱 Responsive mobile navigation',
                        className="text-gray-700 mb-1 text-sm"),
                html.Li('🚀 Fast and modern interface',
                        className="text-gray-700 mb-1 text-sm"),
            ], className="space-y-1")
        ], className="bg-white p-4 rounded-lg shadow-md")
    ], title="Features")
], title="Welcome to EasySAM")
