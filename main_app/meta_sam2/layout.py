import dash_core_components as dcc
import dash_html_components as html
from main_app.dash_shared import shared_dash_nav_links

layout = html.Div([
    shared_dash_nav_links(),
    html.H1("Semantic Segmentation by Meta SAM2"),
    
    html.Div([
        # container for the image upload, display, and segmented results
        html.Div([
            #Left side for uploading and displaying the uploaded image
            html.Div([
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
                html.Div(id='output-image-upload', style={'marginTop': '20px'})
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            #Center button for performing segmentation
            html.Div([
                html.Button('Perform Semantic Segmentation', id='segmentation-btn', n_clicks=0),
            ], style={'width': '40%', 'display': 'inline-block', 'textAlign': 'center', 'verticalAlign': 'top'}),
            
            #Right side for displaying the segmented image
            html.Div([
                html.Div(id='segmented-image-display', style={'marginTop': '20px'})
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'space-between', 'marginTop': '20px'}),
    ])
])