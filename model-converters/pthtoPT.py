import torch
import torchvision.models as models

# Load your existing model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load('model.pth')
model.to(device)

# Ensure the model is in evaluation mode
model.eval()

# Example input tensor
example_input = torch.randn(1, 3, 224, 224)  # Adjust dimensions if needed
example_input = example_input.to(device)

# Trace the model
traced_model = torch.jit.trace(model, example_input)

# Save the traced model
traced_model.save('model.pt')
