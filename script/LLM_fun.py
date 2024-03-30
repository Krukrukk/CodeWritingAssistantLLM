from typing import Tuple
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def initialize_model(checkpoint: str, 
                     device: str = "cuda") -> Tuple[AutoTokenizer, AutoModelForCausalLM]:
    """
    Initialize and return a tokenizer and model loaded from a specified Hugging Face checkpoint.

    This function loads a tokenizer and a causal language model compatible with the given checkpoint.
    The model is configured for use with a specified computing device (e.g., CPU or CUDA for GPU).
    It ensures that the model utilizes half-precision floating-point format (bfloat16) for enhanced performance
    on compatible hardware.

    Parameters:
    - checkpoint (str): The name of the pre-trained model checkpoint from Hugging Face's model hub.
    - device (str): The device to use for the model. Defaults to "cuda" for GPU acceleration.

    Returns:
    - tuple(AutoTokenizer, AutoModelForCausalLM): A tuple containing the initialized tokenizer and model.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(checkpoint, padding_side='left')
        model = AutoModelForCausalLM.from_pretrained(checkpoint, device_map="auto", torch_dtype=torch.bfloat16)
        model.to(device)
        return tokenizer, model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize model and tokenizer from checkpoint '{checkpoint}': {e}")
    
def generate_text(tokenizer: AutoTokenizer, 
                  model: AutoModelForCausalLM, 
                  text: str, 
                  device: str="cuda", 
                  max_length_input: int=500, 
                  max_new_tokens: int=50) -> str:
    """
    Generate text based on the provided input text using a pre-initialized tokenizer and model.

    Parameters:
    - tokenizer (AutoTokenizer): The tokenizer for encoding the input text and decoding the output tokens.
    - model (AutoModelForCausalLM): The pre-initialized model used for generating the text.
    - text (str): The input text to base the generation on.
    - device (str): The device the model operates on. Defaults to "cuda" for GPU acceleration.
    - max_length_input (int): The maximum length of the input text to be encoded (in tokens). Defaults to 500.
    - max_new_tokens (int): The maximum number of new tokens to be generated. Defaults to 50.

    Returns:
    - str: The text generated by the model based on the input text.
    """
    try:
        # Ensure the tokenizer's pad token is set to the EOS token if it's not already set
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # Encode the input text, ensuring not to exceed max_length_input
        inputs = tokenizer.encode_plus(text, return_tensors="pt", max_length=max_length_input, truncation=True, padding='max_length')
        
        # Move the tensor to the appropriate device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate a sequence of tokens with max_new_tokens controlling the output length
        output_tokens = model.generate(**inputs, max_length=max_length_input + max_new_tokens)[0]
        
        # Decode the tokens to a string, skipping special tokens
        generated_text = tokenizer.decode(output_tokens, skip_special_tokens=True)
        return generated_text
    except Exception as e:
        raise RuntimeError(f"Failed to generate text: {e}")