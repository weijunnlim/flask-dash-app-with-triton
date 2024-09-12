from locust import HttpUser, between, task, events, TaskSet
import io
from PIL import Image
import numpy as np
from io import BytesIO
import random
import base64

#generate different test images
def create_test_image():
    width, height = 224, 224
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    image = Image.new("RGB", (width, height), color=color)
    byte_arr = BytesIO()
    image.save(byte_arr, format='JPEG')
    
    byte_arr.seek(0)
    return byte_arr


class ImageUploadUser(HttpUser):
    wait_time = between(1, 2)  # Simulate user wait times between requests
    
    @task
    def upload_image(self):
        # Generate test image
        image_data = create_test_image()

        # Define image upload URL in your web app
        files = {'file': ('test_image.jpg', image_data, 'image/jpeg')}

        # headers = {
        #     'Accept':'application/json'
        # }

        #Make POST request to your web app's image upload endpoint
        # response = self.client.get("/cat_dog/_dash-component-suites/dash/dcc/async-upload.js", files=files)

        # encoded_image = base64.b64encode(image_data.getvalue()).decode('utf-8')
        # image_content = f"data:image/jpeg;base64,{encoded_image}"
        
        response = self.client.post(
            "/cat_dog/_dash-update-component",
            files = files
        )
        
        if response.status_code == 200:
            print("Image upload successful")
        else:
            print(f"Failed with status code: {response.status_code}")


# Optional: Event handler to log test completion
@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Test completed")

