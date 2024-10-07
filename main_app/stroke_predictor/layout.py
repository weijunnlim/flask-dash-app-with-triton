import dash_bootstrap_components as dbc
import dash_html_components as html
from main_app.dash_shared import shared_dash_nav_links
import dash_core_components as dcc

layout = dbc.Container([
    shared_dash_nav_links(),
    dbc.Row(
        dbc.Col(
            html.H1("Patient Health Data", className="text-center mb-4"),
            width=12  
        )
    ),
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Gender:", className="form-label"),
                            dbc.Select(
                                id='gender-dropdown',
                                options=[
                                    {'label': 'Male', 'value': 'Male'},
                                    {'label': 'Female', 'value': 'Female'},
                                    {'label': 'Other', 'value': 'Other'}
                                ],
                                value='Male',
                                className="form-select"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("Age:", className="form-label"),
                            dbc.Input(
                                id='age-input',
                                type='number',
                                value=0,
                                min=0,
                                step=1,
                                className="form-control"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("Hypertension:", className="form-label"),
                            dbc.Select(
                                id='hypertension-dropdown',
                                options=[
                                    {'label': 'No', 'value': 0},
                                    {'label': 'Yes', 'value': 1}
                                ],
                                value=0,
                                className="form-select"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("Heart Disease:", className="form-label"),
                            dbc.Select(
                                id='heart-disease-dropdown',
                                options=[
                                    {'label': 'No', 'value': 0},
                                    {'label': 'Yes', 'value': 1}
                                ],
                                value=0,
                                className="form-select"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("Ever Married:", className="form-label"),
                            dbc.Select(
                                id='ever-married-dropdown',
                                options=[
                                    {'label': 'Yes', 'value': 'Yes'},
                                    {'label': 'No', 'value': 'No'}
                                ],
                                value='Yes',
                                className="form-select"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("Work Type:", className="form-label"),
                            dbc.Select(
                                id='work-type-dropdown',
                                options=[
                                    {'label': 'Private', 'value': 'Private'},
                                    {'label': 'Self-employed', 'value': 'Self-employed'},
                                    {'label': 'Govt_job', 'value': 'Govt_job'},
                                    {'label': 'Children', 'value': 'Children'},
                                    {'label': 'Never_worked', 'value': 'Never_worked'}
                                ],
                                value='Private',
                                className="form-select"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("Residence Type:", className="form-label"),
                            dbc.Select(
                                id='residence-type-dropdown',
                                options=[
                                    {'label': 'Urban', 'value': 'Urban'},
                                    {'label': 'Rural', 'value': 'Rural'}
                                ],
                                value='Urban',
                                className="form-select"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("Average Glucose Level:", className="form-label"),
                            dbc.Input(
                                id='avg-glucose-input',
                                type='number',
                                value=0.0,
                                min=0,
                                step=0.01,
                                className="form-control"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("BMI:", className="form-label"),
                            dbc.Input(
                                id='bmi-input',
                                type='number',
                                value=0.0,
                                min=0,
                                step=0.1,
                                className="form-control"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col([
                            dbc.Label("Smoking Status:", className="form-label"),
                            dbc.Select(
                                id='smoking-status-dropdown',
                                options=[
                                    {'label': 'formerly smoked', 'value': 'formerly smoked'},
                                    {'label': 'never smoked', 'value': 'never smoked'},
                                    {'label': 'smokes', 'value': 'smokes'}
                                ],
                                value='never smoked',
                                className="form-select"
                            )
                        ], width=12, className="mb-3"),

                        dbc.Col(
                            html.A("About Model", href="/stroke_predictor/dashboard", className="btn btn-primary w-100 mt-3"),
                            width=12, className="text-end"
                        ),

                        dbc.Col([
                            dbc.Button('Submit Prediction', id='submit-button', n_clicks=0, className="btn btn-primary w-100 mt-3"),
                        ], width=12),

                        dbc.Col([
                            html.Div(id='prediction-output', className="mt-3")
                        ], width=12),
                    ], className="gx-4") 
                ]),
                className="shadow-sm"
            ),
            width=6  
        ),
        className="d-flex justify-content-center" 
    )
], fluid=True)
