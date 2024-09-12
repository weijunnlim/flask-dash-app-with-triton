import torch
from sam2.build_sam import build_sam2
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator
import numpy as np
from PIL import Image
import base64
import io
import dash_html_components as html
import matplotlib.pyplot as plt
import cv2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = '/home/dxd_wj/model_serving/flask-dash-app/main_app/meta_sam2/checkpoints/sam2_hiera_large.pt'
model_cfg = 'sam2_hiera_l.yaml'
sam2 = build_sam2(model_cfg, model_path, device=device)
mask_generator = SAM2AutomaticMaskGenerator(sam2)

np.random.seed(3)

def show_anns(anns, borders=True):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:, :, 3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.5]])
        img[m] = color_mask 
        if borders:
            import cv2
            contours, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
            contours = [cv2.approxPolyDP(contour, epsilon=0.01, closed=True) for contour in contours]
            cv2.drawContours(img, contours, -1, (0, 0, 1, 0.4), thickness=1) 

    ax.imshow(img)
def perform_segmentation(uploaded_image):
    # Decode the image
    content_type, content_string = uploaded_image.split(',')
    decoded_image = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded_image))
    image_np = np.array(image.convert("RGB"))
    
    masks = mask_generator.generate(image_np)
    
    #Plot the image and overlay the masks
    plt.figure(figsize=(20, 20))
    plt.imshow(image)
    show_anns(masks)
    plt.axis('off')
    
    #Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    #Convert plot image to base64
    img_base64 = base64.b64encode(buf.getvalue()).decode('ascii')
    buf.close()

    return html.Img(src=f"data:image/png;base64,{img_base64}", style={'width': '100%'})

