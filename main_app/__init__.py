from flask import Flask, request, url_for
from flask.helpers import get_root_path
from dash import Dash
from os import getpid
from dash_bootstrap_components.themes import BOOTSTRAP
#import dash_auth
from flask_login import LoginManager, current_user
from main_app.routes import server_bp
from main_app.classes.student import Student
import flask
from main_app.extensions import db
import numpy as np
#from dash import html

import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from explainerdashboard.custom import *
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

# VALID_USERNAME_PASSWORD_PAIRS = {
#     'hello': 'world'
# }

def load_html_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def create_app(dash_debug, dash_auto_reload):
    server = Flask(__name__, static_folder='static')

    # configure flask app/server here
    server.config.from_object('config.Config')

    #Set up Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(server)
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Student.query.get(user_id)
    
    server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(server)


    ###START CODE###

    import xgboost as xgb
    import shap
    model = xgb.XGBClassifier()
    model.load_model('main_app/stroke_predictor/stroke_model.json')
    explainer_v2 = shap.TreeExplainer(model)
    #X is taking the whole dataset, when plotting then input in user's values
    import pandas as pd
    dataset_clean_median = pd.read_csv('main_app/dataset_clean_median.csv')
    X = dataset_clean_median.drop(['stroke', 'id'], axis=1) #all features

    # shap.force_plot(explainer.expected_value, shap_values[0, :], X.iloc[0, :])
    # shap.save_html('force_plot.html', shap.force_plot(explainer.expected_value, shap_values[0, :], X.iloc[0, :]))

    class CustomDashPage(ExplainerComponent): #probably can wrap in any other component written in their documentation
        def __init__(self, explainer, title="Custom Dashboard", name="None"):
            super().__init__(explainer, title, name=name)
            #can choose whatever component u want   
            self.shap_dependence = ShapDependenceComponent(explainer, name=self.name+"dep",
                                hide_title=True, hide_cats=True, hide_highlight=True,
                                cats=True)
            self.contrib = ShapContributionsGraphComponent(explainer, name=self.name+"contrib",
                            hide_selector=True, hide_cats=True, 
                            hide_depth=True, hide_sort=True,)
    
        def layout(self):
            return html.Div([
                self.shap_dependence.layout(),
                self.contrib.layout(),
                html.Div(id='output-div', children="Enter input data:"),

                html.Div([
                    dbc.Label("Gender:", className="form-label"),
                    dcc.Dropdown(
                        id='gender',
                        options=[
                            {'label': 'Male', 'value': 'Male'},
                            {'label': 'Female', 'value': 'Female'},
                            {'label': 'Other', 'value': 'Other'}
                        ],
                        placeholder='Select Gender'
                    )
                ]),
                
        
                html.Div([
                    dbc.Label("Age:", className="form-label"),
                    dcc.Input(
                        id='age', type='number', placeholder='Enter Age'
                    )
                ]),

                html.Div([
                    dbc.Label("Hypertension:", className="form-label"),
                    dcc.Dropdown(
                        id='hypertension',
                        options=[
                            {'label': 'No', 'value': 0},
                            {'label': 'Yes', 'value': 1}
                        ],
                        placeholder='Select Hypertension (0/1)'
                    )
                ]),

 
                html.Div([
                    dbc.Label("Heart Disease:", className="form-label"),
                    dcc.Dropdown(
                        id='heart_disease',
                        options=[
                            {'label': 'No', 'value': 0},
                            {'label': 'Yes', 'value': 1}
                        ],
                        placeholder='Select Heart Disease (0/1)'
                    )
                ]),

                html.Div([
                    dbc.Label("Ever Married:", className="form-label"),
                    dcc.Dropdown(
                        id='ever_married',
                        options=[
                            {'label': 'Yes', 'value': 'Yes'},
                            {'label': 'No', 'value': 'No'}
                        ],
                        placeholder='Select Ever Married (Yes/No)'
                    )
                ]),

                html.Div([
                    dbc.Label("Work Type:", className="form-label"),
                    dcc.Dropdown(
                        id='work_type',
                        options=[
                            {'label': 'Self-employed', 'value': 'Self-employed'},
                            {'label': 'Private', 'value': 'Private'},
                            {'label': 'Govt_job', 'value': 'Govt_job'},
                            {'label': 'Never_worked', 'value': 'Never_worked'},
                            {'label': 'Children', 'value': 'Children'}
                        ],
                        placeholder='Select Work Type'
                    )
                ]),

                html.Div([
                    dbc.Label("Residence Type:", className="form-label"),
                    dcc.Dropdown(
                        id='Residence_type',
                        options=[
                            {'label': 'Urban', 'value': 'Urban'},
                            {'label': 'Rural', 'value': 'Rural'}
                        ],
                        placeholder='Select Residence Type'
                    )
                ]),

                html.Div([
                    dbc.Label("Avg Glucose lvl:", className="form-label"),
                    dcc.Input(
                        id='avg_glucose_level', type='number', placeholder='Enter Avg Glucose Level'
                    )
                ]),

                html.Div([
                    dbc.Label("BMI:", className="form-label"),
                    dcc.Input(
                        id='bmi', type='number', placeholder='Enter BMI'
                    )
                ]),

                html.Div([
                    dbc.Label("Smoking status:", className="form-label"),
                    dcc.Dropdown(
                        id='smoking_status',
                        options=[
                            {'label': 'Formerly Smoked', 'value': 'formerly smoked'},
                            {'label': 'Smokes', 'value': 'smokes'},
                            {'label': 'Never Smoked', 'value': 'never smoked'}
                        ],
                        placeholder='Select Smoking Status'
                    )
                ]),
                
                html.Div([
                    html.Button(id='input-button', children="Generate Force Plot"),
                    html.Iframe(id='shap-force-plot', style={"width": "100%", "height": "600px"})
                ])
            ])
        
        def component_callbacks(self, app):
            @app.callback(
                Output('shap-force-plot', 'srcDoc'), #need to return as srcDoc
                Input('input-button', 'n_clicks'),
                [Input('gender', 'value'),
                Input('age', 'value'),
                Input('hypertension', 'value'),
                Input('heart_disease', 'value'),
                Input('ever_married', 'value'),
                Input('work_type', 'value'),
                Input('Residence_type', 'value'),
                Input('avg_glucose_level', 'value'),
                Input('bmi', 'value'),
                Input('smoking_status', 'value')]
            )
            
            def update_force_plot(n_clicks, gender, age, hypertension, heart_disease,
                                  ever_married, work_type, Residence_type, avg_glucose_level, bmi, smoking_status):
                if n_clicks is None:
                    return '' 
                
                input_data = {
                    'gender': gender,
                    'age': age,
                    'hypertension': hypertension,
                    'heart_disease': heart_disease,
                    'ever_married': ever_married,
                    'work_type': work_type,
                    'Residence_type': Residence_type,
                    'avg_glucose_level': avg_glucose_level,
                    'bmi': bmi,
                    'smoking_status': smoking_status
                }
                def encode_categorical(input_data):
                    encoded_data = {}
                    
                    encoded_data['gender_Male'] = 1 if input_data['gender'] == 'Male' else 0
                    encoded_data['gender_Female'] = 1 if input_data['gender'] == 'Female' else 0
                    encoded_data['gender_Other'] = 1 if input_data['gender'] == 'Other' else 0

                    encoded_data['ever_married_Yes'] = 1 if input_data['ever_married'] == 'Yes' else 0
                    encoded_data['ever_married_No'] = 1 if input_data['ever_married'] == 'No' else 0

                    work_types = ['Self-employed', 'Private', 'Govt_job', 'Never_worked', 'Children']
                    for work in work_types:
                        encoded_data[f'work_type_{work}'] = 1 if input_data['work_type'] == work else 0

                    encoded_data['Residence_type_Urban'] = 1 if input_data['Residence_type'] == 'Urban' else 0
                    encoded_data['Residence_type_Rural'] = 1 if input_data['Residence_type'] == 'Rural' else 0


                    smoking_statuses = ['formerly smoked', 'smokes', 'never smoked']
                    for status in smoking_statuses:
                        encoded_data[f'smoking_status_{status}'] = 1 if input_data['smoking_status'] == status else 0

                    encoded_data['age'] = input_data['age']
                    encoded_data['hypertension'] = input_data['hypertension']
                    encoded_data['heart_disease'] = input_data['heart_disease']
                    encoded_data['avg_glucose_level'] = input_data['avg_glucose_level']
                    encoded_data['bmi'] = input_data['bmi']

                    return encoded_data
                
                encoded_input_data = encode_categorical(input_data)

            
                input_df = pd.DataFrame([encoded_input_data])

                input_df_encoded = pd.get_dummies(input_df, drop_first=True)

                input_df_aligned = input_df_encoded.reindex(columns=X.columns, fill_value=0) 

                shap_values_input = explainer_v2.shap_values(input_df_aligned)

                force_plot = shap.force_plot(explainer_v2.expected_value, shap_values_input[0], input_df_aligned.iloc[0, :])
                
                shap_html = f"<html><head>{shap.getjs()}</head><body>{force_plot.html()}</body></html>"

                return shap_html
            

            

    import pickle   
    from explainerdashboard import ExplainerDashboard
    #change the routing to as required
    with open('main_app/stroke_predictor/classifier_explainer.pkl', 'rb') as f: 
        explainer = pickle.load(f)
    #can set shap_interaction = False because shap interaction values take very long to calculate   
    dashboard = ExplainerDashboard(explainer, 
                                   #basically add whatever tabs u want
                                   [ImportancesComposite, ClassifierModelStatsComposite, 
                                    IndividualPredictionsComposite, WhatIfComposite, 
                                    ShapDependenceComposite, DecisionTreesComposite,
                                    ShapInteractionsComposite, CustomDashPage],
                                   server=server, url_base_pathname="/stroke_predictor/dashboard/",
                                   title = 'Stroke Model Explainer',
                                   shap_interaction=True)
    
    #html_content = load_html_file('main_app/stroke_predictor/force_plot.html') #to change  

    from main_app.dash_shared import shared_dash_nav_links
    #import dash_bootstrap_components as dbc
    #layout
    dashboard.app.layout = dbc.Container([
        shared_dash_nav_links(),
        dbc.Container([
            dashboard.app.layout,
        #     html.Iframe(
        #         srcDoc =html_content,
        #         style={"width": "100%", "height": "600px", "border": "none"}
        # )
        ]),
    ], fluid = True)

    @server.route('/stroke_predictor/dashboard')
    def return_dashboard():
        return dashboard.app.index()
    

    #need to create a dash component to field this dashboard 


    ###END CODE###
    
    
    register_dash_apps(server, dash_debug, dash_auto_reload)

    register_blueprints(server)

    # if running on gunicorn with multiple workers this message should print once for each worker if preload_app is set to False
    print(f'Flask With Dash Apps Built Successfully with PID {str(getpid())}.')
    return server

def register_dash_apps(flask_server, dash_debug, dash_auto_reload):
    #register all dash apps
    from main_app.home.layout import layout as home_layout
    from main_app.home.callbacks import register_callbacks as home_callbacks
    register_dash_app(
        flask_server=flask_server,
        title='Home Page',
        base_pathname='home',
        layout=home_layout,
        register_callbacks_funcs=[home_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.cat_dog.layout import layout as cat_dog_layout
    from main_app.cat_dog.callbacks import register_callbacks as cat_dog_callbacks
    register_dash_app(
        flask_server=flask_server,
        title='Cat Dog Prediction',
        base_pathname='cat_dog',
        layout=cat_dog_layout,
        register_callbacks_funcs=[cat_dog_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.text_converter.layout import layout as text_converter_layout
    from main_app.text_converter.callbacks import register_callbacks as text_converter_callbacks
    register_dash_app(
        flask_server=flask_server,
        title='Text Converter',
        base_pathname='text_converter',
        layout=text_converter_layout,
        register_callbacks_funcs=[text_converter_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.stroke_predictor.layout import layout as stroke_predictor_layout
    from main_app.stroke_predictor.callbacks import register_callbacks as stroke_predictor_callbacks
    register_dash_app(
        flask_server=flask_server,
        title='Stroke Predictor',
        base_pathname='stroke_predictor',
        layout=stroke_predictor_layout,
        register_callbacks_funcs=[stroke_predictor_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.table.layout import layout as table_layout
    from main_app.table.callbacks import register_callbacks as table_callbacks
    register_dash_app(
        flask_server=flask_server,
        title='Table',
        base_pathname='table',
        layout=table_layout,
        register_callbacks_funcs=[table_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.meta_sam2.layout import layout as meta_sam2_layout
    from main_app.meta_sam2.callbacks1 import register_image_upload_callback as meta_sam2_callbacks1
    from main_app.meta_sam2.callbacks2 import segmented_image_callback as meta_sam2_callbacks2
    register_dash_app(
        flask_server=flask_server,
        title='Meta SAM2',
        base_pathname='meta_sam2',
        layout=meta_sam2_layout,
        register_callbacks_funcs=[meta_sam2_callbacks1, meta_sam2_callbacks2],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )


    from main_app.login.layout import layout as login_layout
    from main_app.login.callbacks import register_callbacks as login_callbacks
    from main_app.login.callbacks2 import register_callbacks2 as login_callbacks2
    register_dash_app(
        flask_server=flask_server,
        title='Login',
        base_pathname='login',
        layout=login_layout,
        register_callbacks_funcs=[login_callbacks, login_callbacks2],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )

    from main_app.signup.layout import layout as signup_layout
    from main_app.signup.callbacks import register_callbacks as signup_callbacks
    register_dash_app(
        flask_server=flask_server,
        title='Signup',
        base_pathname='signup',
        layout=signup_layout,
        register_callbacks_funcs=[signup_callbacks],
        dash_debug=dash_debug,
        dash_auto_reload=dash_auto_reload,
        external_stylesheets=[BOOTSTRAP]
    )


def register_dash_app(flask_server, title, base_pathname, layout, register_callbacks_funcs, dash_debug, dash_auto_reload, external_stylesheets= None):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dash_app = Dash(
        __name__,
        server=flask_server,
        url_base_pathname=f'/{base_pathname}/',
        assets_folder=get_root_path(__name__) + '/static/',
        meta_tags=[meta_viewport],
        external_stylesheets=external_stylesheets,
        # external_scripts=[]
    )

    # auth = dash_auth.BasicAuth(
    #     my_dash_app,
    #     VALID_USERNAME_PASSWORD_PAIRS
    # )


    with flask_server.app_context():
        my_dash_app.title = title
        my_dash_app.layout = layout
        my_dash_app.css.config.serve_locally = True
        my_dash_app.enable_dev_tools(debug=dash_debug, dev_tools_hot_reload=dash_auto_reload)
        if register_callbacks_funcs:
            for call_back_func in register_callbacks_funcs:
                call_back_func(my_dash_app)

        @my_dash_app.server.before_request
        def restrict_access():
            public_routes = ['/meta_sam2/', '/table/', '/login/', '/signup/', '/database'] #never put '/' as it will allow all routes
            current_path = request.path

            #only public routes can access without logging in
            if any(current_path.startswith(route) for route in public_routes):
                return  

            #if login successful
            if current_user.is_authenticated:
                return
    
            return flask.redirect(url_for('main.login'))


            
def register_blueprints(server):
    from main_app.routes import server_bp
    server.register_blueprint(server_bp)
