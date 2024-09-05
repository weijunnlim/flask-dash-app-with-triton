### pip install -r requirements.txt (activate virtual env first if needed)
### run the nvidia triton inference server on port 8000 in another terminal (at where your model repo is at)
### docker run --gpus=all -it --shm-size=256m --rm -p8000:8000 -p8001:8001 -p8002:8002 -v $(pwd)/model_repository:/models nvcr.io/nvidia/tritonserver:24.07-py3
### tritonserver --model-repository=/models
### run the flask dash app
### python app.py

# Template Notes:
* Application entry point is app.py
* I personally use native dash layouts and do not utilize jinja iFrames but both methods are shown
* Additional configurations can be assigned to the dash apps in the register_dash_app function.
# Helpful Tutorials & Repos
* https://medium.com/@olegkomarov_77860/how-to-embed-a-dash-app-into-an-existing-flask-app-ea05d7a2210b
* https://hackersandslackers.com/plotly-dash-with-flask/
* https://hackersandslackers.com/flask-blueprints/
* https://github.com/jimmybow/Flask_template_auth_with_Dash
------------------------------------------------------------------------------------------------------------------------
