import dash
from dash import Dash, html, dcc
from components.navbar import create_navbar

app = Dash(__name__,
           use_pages=True,
           title="EasySam",
           external_scripts=["https://unpkg.com/@tailwindcss/browser@4"],
           external_stylesheets=[
               "https://fonts.googleapis.com/css2?family=Inter&display=swap",
               "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
           ])

app.layout = html.Div([
    create_navbar(),

    # Main Content Container
    html.Div([
        dash.page_container
    ], className="min-h-screen bg-gray-50")
])

if __name__ == '__main__':
    app.run(debug=True)
