import dash_core_components as dcc
import dash_html_components as html
from main_app.dash_shared import shared_dash_nav_links

layout = html.Div([
    shared_dash_nav_links(),
    html.H1("Text Detection and Recognition by Nvidia"),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-image-upload', style={'textAlign': 'center', 'marginTop': '20px'}),
])