import numpy as np
from torchvision import transforms
from PIL import Image
import tritonclient.http as httpclient

def process_image(image_path):
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    client = httpclient.InferenceServerClient(url="localhost:8000")

    transform = transforms.Compose([
        transforms.Resize((224, 224)), #my model is resnet model so it was trained on 224 x 224 images
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]), #pytorch way of normalising images
    ])

    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  #adding batch dimension into shape (1, 3, 224 , 224) 3 rgb channels 
    #so that can process multiple images even though this case is only 1

    #create input
    image_input = httpclient.InferInput(
        "input.1", image.shape, datatype="FP32"
    )

    image_input.set_data_from_numpy(image.numpy())

    #Query the server
    prediction_output = client.infer(
        model_name="cat_dog", inputs=[image_input]
    )
    #process output from model
    predicted_output = prediction_output.as_numpy("536")

    # Perform inference
    # with torch.no_grad():
    #     output = model(image)
    predicted = np.argmax(predicted_output, 1) #to determine which class has higher score
    prediction = predicted[0]

    class_labels = ['Cat', 'Dog']
    return class_labels[prediction]