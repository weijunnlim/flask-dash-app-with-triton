import xgboost as xgb
import pandas as pd
import numpy as np


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