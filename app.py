import streamlit as st
from script.LLM_fun import initialize_model, generate_text  
import torch

# Function to check GPU availability and details
def check_gpu():
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9  
        return True, gpu_name, gpu_memory
    else:
        return False, None, None

# Title and Logo
st.title("My Code Generation App")
st.image("logo.png", width=100)  # Adjust path and size as needed
st.write("This application will assist you in writing code using LLM StarCoder2 ^1")

# Check GPU Status
gpu_status, gpu_name, gpu_memory = check_gpu()
if gpu_status:
    st.success(f"✔️ GPU Connected: {gpu_name}, Memory: {gpu_memory:.2f} GB")
else:
    st.error("You need to correctly install the drivers for your graphics card in order to use the application.")
    st.stop()
    
with st.container():
    st.header("Initialize Model")
    checkpoint = st.text_input("Model Checkpoint", value="bigcode/starcoder2-3b")

    # Initialize a session state variable for model initialization status if it does not already exist
    if 'model_initialized' not in st.session_state:
        st.session_state['model_initialized'] = False

    # The button is disabled if the model is already initialized, based on the session state variable
    if not st.session_state['model_initialized']:
        if st.button("Initialize"):
            try:
                tokenizer, model = initialize_model(checkpoint)
                st.session_state['model'] = model
                st.session_state['tokenizer'] = tokenizer
                st.session_state['model_initialized'] = True 
                st.success("Model initialized successfully!")
            except Exception as e:
                st.error(f"Failed to initialize the model: {e}")
    else:
        st.success("Model already initialized. Ready to generate text!") 

# Section for Text Generation Input
with st.container():
    st.header("Generate Code")
    input_text = st.text_area("Input Text", value="def tell_me_truth(text):", height=150)
    if st.button("Generate"):
        if 'model' in st.session_state and 'tokenizer' in st.session_state:
            generated_text = generate_text(st.session_state['tokenizer'], st.session_state['model'], input_text)
            st.text_area("Generated Code", value=generated_text, height=250, disabled=True)
        else:
            st.warning("Please initialize the model first.")
