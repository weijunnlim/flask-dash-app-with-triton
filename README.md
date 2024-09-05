# Model Deployment and Flask-Dash App Setup

## Installation Instructions

1. **Install ONNX Models:**
   - For text detection and text recognition models, follow NVIDIA's guide: [NVIDIA Triton Inference Server Tutorial](https://github.com/triton-inference-server/tutorials/blob/main/Conceptual_Guide/Part_1-model_deployment/README.md).

2. **Install Dependencies:**
   - Activate your virtual environment if needed.
   - Install required packages:

     ```bash
     pip install -r requirements.txt
     ```

3. **Run NVIDIA Triton Inference Server:**
   - Open a new terminal and navigate to the directory where your model repository is located.
   - Run the Triton Inference Server using Docker:

     ```bash
     docker run --gpus=all -it --shm-size=256m --rm \
       -p8000:8000 -p8001:8001 -p8002:8002 \
       -v $(pwd)/model_repository:/models \
       nvcr.io/nvidia/tritonserver:24.07-py3 \
       tritonserver --model-repository=/models
     ```

4. **Run the Flask-Dash Application:**
   - Execute the Flask-Dash app:

     ```bash
     python app.py
     ```

## Template Notes

- **Application Entry Point:** `app.py`
- **Layouts:** The app uses native Dash layouts. It does not utilize Jinja iFrames, but both methods are demonstrated.
- **Additional Configurations:** Assign additional configurations to the Dash apps in the `register_dash_app` function.

## Helpful Tutorials & Repositories

- [How to Embed a Dash App into an Existing Flask App](https://medium.com/@olegkomarov_77860/how-to-embed-a-dash-app-into-an-existing-flask-app-ea05d7a2210b)
- [Plotly Dash with Flask](https://hackersandslackers.com/plotly-dash-with-flask/)
- [Flask Blueprints](https://hackersandslackers.com/flask-blueprints/)
- [Flask Template Auth with Dash](https://github.com/jimmybow/Flask_template_auth_with_Dash)
