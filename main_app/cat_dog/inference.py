import torch
from torchvision import transforms
from PIL import Image

def process_image(image_path):
    # Check if a GPU is available and use it if it is, otherwise fall back to CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Define the path to your model
    model_path = '/home/dxd_wj/model_serving/flask-dash-app/main_app/cat_dog/model.pth'

    # Load the model and move it to the appropriate device
    model = torch.load(model_path, map_location=device)
    model.to(device)
    model.eval()  # Set the model to evaluation mode

    # Define image transformations
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Load and transform the image
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension

    # Move the input image to the same device as the model
    image = image.to(device)

    # Perform inference
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1) #to determine which class has higher score
        prediction = predicted.item() # 0 or 1

    class_labels = ['Cat', 'Dog']
    return class_labels[prediction]