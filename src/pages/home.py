import dash
from dash import html
from components import page_layout, section

dash.register_page(__name__, path='/', name='Home')

layout = page_layout([
    html.P('This is your home page with a beautiful navigation bar.',
           className="text-xl text-gray-600 mb-8"),

    section([
        html.Div([
            html.Ul([
                html.Li('🎨 Beautiful TailwindCSS styling',
                        className="text-gray-700 mb-2"),
                html.Li('📱 Responsive mobile navigation',
                        className="text-gray-700 mb-2"),
                html.Li('🚀 Fast and modern interface',
                        className="text-gray-700 mb-2"),
            ], className="space-y-2")
        ], className="bg-white p-6 rounded-lg shadow-md")
    ], title="Features")
], title="Welcome to EasySAM")
