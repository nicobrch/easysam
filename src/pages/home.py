import dash
from dash import html

dash.register_page(__name__, path='/', name='Home')

layout = html.Div([
    html.Div([
        html.H1('Welcome to EasySAM',
                className="text-4xl font-bold text-gray-900 mb-4"),
        html.P('This is your home page with a beautiful navigation bar.',
               className="text-xl text-gray-600 mb-8"),
        html.Div([
            html.H2(
                'Features', className="text-2xl font-semibold text-gray-800 mb-4"),
            html.Ul([
                html.Li('🎨 Beautiful TailwindCSS styling',
                        className="text-gray-700 mb-2"),
                html.Li('📱 Responsive mobile navigation',
                        className="text-gray-700 mb-2"),
                html.Li('🚀 Fast and modern interface',
                        className="text-gray-700 mb-2"),
            ], className="space-y-2")
        ], className="bg-white p-6 rounded-lg shadow-md")
    ], className="max-w-4xl mx-auto px-4 py-12")
], className="min-h-screen bg-gray-50", style={"fontFamily": "Inter, sans-serif"})
