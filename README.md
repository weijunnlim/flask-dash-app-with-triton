# Model Deployment and Flask-Dash App Setup

## Installation Instructions

1. **Install Models:**
   - For text detection and text recognition models, follow NVIDIA's guide: [NVIDIA Triton Inference Server Tutorial](https://github.com/triton-inference-server/tutorials/blob/main/Conceptual_Guide/Part_1-model_deployment/README.md).
   - For meta SAM2 models, cd to the checkpoints folder and run the download checkpoints script using

     ```bash
     ./download_ckpts.sh
     ```   

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
5. **(Optional) Prometheus and Grafana Monitoring Setup:**
   - If you'd like to view the server's performance metrics using Prometheus and Grafana, follow the steps below:

   **Prometheus Setup:**
   - Refer to [Triton Inference Server Prometheus Metrics Setup](https://github.com/triton-inference-server/hugectr_backend/blob/main/docs/metrics.md).
   - Once Prometheus is configured, start it by running:

     ```bash
     ./prometheus
     ```

   **Grafana Setup:**
   - Run Grafana using Docker:

     ```bash
     docker run -d -p 3000:3000 grafana/grafana
     ```

   - Grafana will be available at `localhost:3000`.

   - Default user and password would be admin

## Summary
By following the steps above, you will have the Triton Inference Server running to serve your models, along with a Flask-Dash application. Optionally, you can set up Prometheus and Grafana to monitor performance.
