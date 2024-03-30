import torch
from transformers import AutoModelForCausalLM

def check_gpu():
    """
    Check if a CUDA-capable GPU is available and return its name and memory information.

    This function uses PyTorch's CUDA API to check if a GPU is available for use.
    If a GPU is available, the function retrieves the name of the GPU (as provided by CUDA)
    and its total memory in gigabytes (GB). If no GPU is available, the function returns
    False, with the GPU name and memory set to None.

    Returns:
    - tuple: A tuple containing three elements:
        - A boolean value indicating whether a CUDA-capable GPU is available (True) or not (False).
        - The name of the GPU as a string, or None if no GPU is available.
        - The total memory of the GPU in gigabytes (GB) as a float, or None if no GPU is available.
    """
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9  # Convert bytes to gigabytes
        return True, gpu_name, gpu_memory
    else:
        return False, None, None
    
def print_memory_footprint(model: AutoModelForCausalLM):
    """
    Print the memory footprint of the given model in gigabytes (GB).

    This function retrieves the memory footprint of the model using its
    `get_memory_footprint` method, converts it to megabytes, and prints it in
    a human-readable format.

    Parameters:
    - model: An object that represents a machine learning model. This object
             must have a method `get_memory_footprint()` which returns the
             memory footprint in bytes.

    Returns:
    string. This function return the memory footprint in gigabytes (GB).
    """
    memory_footprint_bytes = model.get_memory_footprint()
    memory_footprint_mb = memory_footprint_bytes / 1e9
    return memory_footprint_mb