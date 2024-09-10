import torch
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
import numpy as np
from PIL import Image
import base64
import io
import dash_core_components as dcc
import dash_html_components as html


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = '/home/dxd_wj/model_serving/flask-dash-app/main_app/meta_sam2/checkpoints/sam2_hiera_large.pt'
model_cfg = 'sam2_hiera_l.yaml'
predictor = SAM2ImagePredictor(build_sam2(model_cfg, model_path, device=device))

def perform_segmentation(uploaded_image):
    #decode the image
    content_type, content_string = uploaded_image.split(',')
    decoded_image = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded_image))
    image_np = np.array(image.convert("RGB"))

    # Perform semantic segmentation
    h, w, _ = image_np.shape
    input_points = np.array([
        [w // 2, h // 2],  # Center point
        [w // 2 + 50, h // 2],  # Point to the right of the center
        [w // 2 - 50, h // 2]   # Point to the left of the center
    ])
    input_labels = np.array([1, 1, 1]) 

    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
        predictor.set_image(image_np)
        masks, scores, logits = predictor.predict(
            point_coords=input_points,
            point_labels=input_labels,
            multimask_output=True,
        )
        
        #sorting between the scores to input best one
        sorted_ind = np.argsort(scores)[::-1]
        masks = masks[sorted_ind]
        scores = scores[sorted_ind]
        logits = logits[sorted_ind]

    #Convert segmented image to base64 string for display
    def image_to_base64(image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
        return f"data:image/png;base64,{img_str}"

    #Convert first mask to PIL Image for display
    segmented_image = Image.fromarray((masks[0] * 255).astype(np.uint8))
    segmented_image_base64 = image_to_base64(segmented_image)

    return html.Img(src=segmented_image_base64, style={'width': '100%'})


