from dash.dependencies import Input, Output, State
from .inference import run_inference
from dash import html
import numpy as np

def register_callbacks(dash_app):
    @dash_app.callback(
        Output('prediction-output', 'children'),
        Input('submit-button', 'n_clicks'),
        State('gender-dropdown', 'value'),
        State('age-input', 'value'),
        State('hypertension-dropdown', 'value'),
        State('heart-disease-dropdown', 'value'),
        State('ever-married-dropdown', 'value'),
        State('work-type-dropdown', 'value'),
        State('residence-type-dropdown', 'value'),
        State('avg-glucose-input', 'value'),
        State('bmi-input', 'value'),
        State('smoking-status-dropdown', 'value')
    )
    def update_prediction(n_clicks, gender, age, hypertension, heart_disease, ever_married, work_type, residence_type, avg_glucose, bmi, smoking_status):
        if n_clicks > 0:  # Ensure it only runs after the button is clicked
            inputs = {
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'avg_glucose_level': avg_glucose,
            'bmi': bmi,
            'gender_Male': gender == 'Male',
            'gender_Other': gender == 'Other',
            'ever_married_Yes': ever_married == 'Yes',
            'work_type_Never_worked': work_type == 'Never_worked',
            'work_type_Private': work_type == 'Private',
            'work_type_Self-employed': work_type == 'Self-employed',
            'work_type_children': work_type == 'Children',
            'Residence_type_Urban': residence_type == 'Urban',
            'smoking_status_never smoked': smoking_status == 'never smoked',
            'smoking_status_smokes': smoking_status == 'smokes'
        }
            result = run_inference(inputs) #call inference function
            if result == 1:
                risk_status = "at risk"
            else:
                risk_status = "not at risk"
            
            return html.Div([
                html.H5("Predicted Outcome:"),
                html.P(f"Based on the input values, the model predicts: {risk_status}")
            ])
        return ""