import xgboost as xgb
import pandas as pd
import numpy as np


inputs = {
    'age': 82,
    'hypertension': 0,
    'heart_disease': 1,
    'avg_glucose_level': 84.03,
    'bmi': 26.5,
    'gender_Male': False,
    'gender_Other': False,
    'ever_married_Yes': False,
    'work_type_Never_worked': False,
    'work_type_Private': True,
    'work_type_Self-employed': False,
    'work_type_children': False,
    'Residence_type_Urban': False,
    'smoking_status_never smoked': False,
    'smoking_status_smokes': False,
}
def run_inference(inputs):
    # Load the XGBoost model from the JSON file
    model = xgb.Booster()
    model.load_model('/home/dxd_wj/model_serving/flask-dash-app/main_app/stroke_predictor/stroke_model.json')

    # Preprocess the input data
    input_data = preprocess_inputs(inputs)

    # Convert the input data to a DMatrix
    dmatrix = xgb.DMatrix(input_data)

    # Perform inference
    predictions = model.predict(dmatrix)
    
    optimal_threshold = 0.035420958
    predicted_class = (predictions > optimal_threshold).astype(int)
    
    return predicted_class[0]

def preprocess_inputs(inputs):
    # Convert the inputs dictionary to a DataFrame
    df = pd.DataFrame([inputs])
    return df
result = run_inference(inputs)

print(f"Probability of stroke: {result}")