import dash_core_components as dcc
import dash_html_components as html
from main_app.dash_shared import shared_dash_nav_links

layout = html.Div([
    shared_dash_nav_links(),
    html.H1("Patient Health Data"),

    html.Div([
        html.Label('Gender:'),
        dcc.Dropdown(
            id='gender-dropdown',
            options=[
                {'label': 'Male', 'value': 'Male'},
                {'label': 'Female', 'value': 'Female'},
                {'label': 'Other', 'value': 'Other'}
            ],
            value='Male'
        )
    ]),
    
    html.Div([
        html.Label('Age:'),
        dcc.Input(
            id='age-input',
            type='number',
            value=0,
            min=0,  
            step=1
        )
    ]),
    
    html.Div([
        html.Label('Hypertension:'),
        dcc.Dropdown(
            id='hypertension-dropdown',
            options=[
                {'label': 'No', 'value': 0},
                {'label': 'Yes', 'value': 1}
            ],
            value=0
        )
    ]),
    
    html.Div([
        html.Label('Heart Disease:'),
        dcc.Dropdown(
            id='heart-disease-dropdown',
            options=[
                {'label': 'No', 'value': 0},
                {'label': 'Yes', 'value': 1}
            ],
            value=0
        )
    ]),
    
    html.Div([
        html.Label('Ever Married:'),
        dcc.Dropdown(
            id='ever-married-dropdown',
            options=[
                {'label': 'Yes', 'value': 'Yes'},
                {'label': 'No', 'value': 'No'}
            ],
            value='Yes'
        )
    ]),
    
    html.Div([
        html.Label('Work Type:'),
        dcc.Dropdown(
            id='work-type-dropdown',
            options=[
                {'label': 'Private', 'value': 'Private'},
                {'label': 'Self-employed', 'value': 'Self-employed'},
                {'label': 'Govt_job', 'value': 'Govt_job'},
                {'label': 'Children', 'value': 'children'},
                {'label': 'Never_worked', 'value': 'Never_worked'}
            ],
            value='Private'
        )
    ]),
    
    html.Div([
        html.Label('Residence Type:'),
        dcc.Dropdown(
            id='residence-type-dropdown',
            options=[
                {'label': 'Urban', 'value': 'Urban'},
                {'label': 'Rural', 'value': 'Rural'}
            ],
            value='Urban'
        )
    ]),
    
    html.Div([
        html.Label('Average Glucose Level:'),
        dcc.Input(
            id='avg-glucose-input',
            type='number',
            value=0.00,
            min=0,  
            step=0.01  
        )
    ]),
    
    html.Div([
        html.Label('BMI:'),
        dcc.Input(
            id='bmi-input',
            type='number',
            value=0.0,
            min=0,
            step=0.1 
        )
    ]),
    
    html.Div([
        html.Label('Smoking Status:'),
        dcc.Dropdown(
            id='smoking-status-dropdown',
            options=[
                {'label': 'formerly smoked', 'value': 'formerly smoked'},
                {'label': 'never smoked', 'value': 'never smoked'},
                {'label': 'smokes', 'value': 'smokes'}
            ],
            value='never smoked'
        )
    ]),

    html.Button('Submit Prediction', id='submit-button', n_clicks=0),

    html.Div(id='prediction-output')
])