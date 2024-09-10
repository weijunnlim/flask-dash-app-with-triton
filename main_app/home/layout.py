import dash_core_components as dcc
import dash_html_components as html
from main_app.dash_shared import shared_dash_nav_links

layout = html.Div([
    shared_dash_nav_links(),
    html.Div([
        html.H1('Welcome to the Home Page'),
        html.P('This is the home page of your application. Add any static or dynamic content here.'),
    ], id='page-content')
])