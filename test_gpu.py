import torch

# Check if CUDA (GPU support) is available
if torch.cuda.is_available():
    # Print the current GPU ID and its specifications
    print(f"CUDA is available! Running on GPU: {torch.cuda.get_device_name(torch.cuda.current_device())}")
    
    # Create a tensor and move it to GPU
    tensor = torch.randn(3, 3).to('cuda')
    
    # Perform a simple operation on the GPU
    result = tensor * tensor
    print("Operation on GPU successful. Result:")
    print(result)
else:
    print("CUDA is not available. Please check your PyTorch installation and GPU drivers.")