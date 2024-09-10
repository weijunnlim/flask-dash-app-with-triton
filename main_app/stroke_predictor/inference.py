import xgboost as xgb
import pandas as pd
import numpy as np
import tritonclient.http as httpclient


def run_inference(inputs):
    client = httpclient.InferenceServerClient(url="localhost:8000")
    # Load the XGBoost model from the JSON file
    #model = xgb.Booster()
    #model.load_model('/home/dxd_wj/model_serving/flask-dash-app/main_app/stroke_predictor/stroke_model.json')

    #Preprocess the input data
    input_data = preprocess_inputs(inputs)

    #Convert the input data to a DMatrix
    #dmatrix = xgb.DMatrix(input_data)
    input_array = input_data.to_numpy(dtype=np.float32)

    #create input
    data_input = httpclient.InferInput(
        "input__0", input_array.shape, datatype="FP32"
    )

    data_input.set_data_from_numpy(input_array)

    #Query the server
    prediction_output = client.infer(
        model_name="stroke_predictor", inputs=[data_input]
    )
    #process output from  model
    predicted_output = prediction_output.as_numpy("output__0")
    #predictions = model.predict(dmatrix)
    #optimal_threshold = 0.035420958
    predicted_class = predicted_output
    predicted_class = (predicted_class).astype(int)
    
    
    return predicted_class[0][0] #output is 2d, one hot encoding [[1,0]] for at risk, [[0,1]] for not at risk

def preprocess_inputs(inputs):
    # Convert the inputs dictionary to a DataFrame
    df = pd.DataFrame([inputs])
    df['hypertension'] = df['hypertension'].astype('bool')
    df['heart_disease'] = df['heart_disease'].astype('bool')
    return df