import torch

# Create PyTorch Model Object
# model = STRModel(input_channels=1, output_channels=512, num_classes=37)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model weights from external file
model = torch.load("model.pth")
#state = {key.replace("module.", ""): value for key, value in state.items()}
model.to(device)
model.eval()
#model.load_state_dict(state)

# Create ONNX file by tracing model
trace_input = torch.randn(1, 3, 224, 224)
trace_input = trace_input.to(device)
torch.onnx.export(model, trace_input, "model.onnx", verbose=True)