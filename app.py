"""
Title: CodeWritingAssistantLLM App
Author: Maciej Małecki
Last_update: 2024-03-30
"""
import streamlit as st
from script.sys_tools import check_gpu, print_memory_footprint
from script.LLM_fun import initialize_model, generate_text  

# Title and Logo
st.title("CodeWritingAssistantLLM App")
# st.image("logo.png", width=100)  # Adjust path and size as needed
st.write("This application will assist you in writing code using LLM.")

with st.container():
    st.header("Instructions")
    st.write("""The main task of the assistant is to suggest the dower 
             part of the code you have written. In order to be able to do this, 
             you first need to load/download the appropriate model, and then enter 
             your code that you want to improve. After pressing button 'Generate', you will be 
             offered to develop your code. If you think you want to continue generating, 
             click 'Move' to move all the generated text to the input compartment. Have fun!""")
    st.write("The application was created for training purposes and will not be used for commercial purposes.")
with st.container():
    st.header("Check GPU Status")
    gpu_status, gpu_name, gpu_memory = check_gpu()
    if gpu_status:
        st.success(f"✔️ GPU Connected: {gpu_name}, Memory: {gpu_memory:.2f} GB")
    else:
        st.error("You need to correctly install the drivers for your graphics card in order to use the application.")
        st.stop()

# Model Initialization Section
with st.container():
    st.header("Initialize Model")
    checkpoint = st.text_input("Model Checkpoint", value="bigcode/starcoder2-3b")
    if 'model_initialized' not in st.session_state:
        st.session_state['model_initialized'] = False

    if not st.session_state['model_initialized']:
        # After model initialization
        if st.button("Initialize"):
            try:
                tokenizer, model = initialize_model(checkpoint)
                st.session_state['model'] = model
                st.session_state['tokenizer'] = tokenizer
                st.session_state['model_initialized'] = True 
                memory_footprint = print_memory_footprint(model)
                if gpu_memory >= memory_footprint:
                    st.success(f"Model initialized successfully! Memory used by the model: {memory_footprint:.2f} GB")
                else:   
                    st.error(f"Insufficient GPU memory: {gpu_memory:.2f} GB available, but {memory_footprint:.2f} GB is required.")
                    st.stop()
            except Exception as e:
                st.error(f"Failed to initialize the model: {e}")
    else:
        st.success("Model already initialized. Ready to generate text!") 

# Text Generation Input Section
with st.container():
    st.header("Generate Code")
    input_text = st.text_area("Input Text", value=st.session_state.get('generated_text', "def hello_world_in_country(country: str):"), height=300)
    max_new_tokens = st.slider("Number of New Tokens", min_value=1, max_value=128, value=20)
    
    if st.button("Generate"):
        if 'model' in st.session_state and 'tokenizer' in st.session_state:
            generated_text = generate_text(st.session_state['tokenizer'], st.session_state['model'], input_text, max_new_tokens=max_new_tokens)
            st.session_state['generated_text'] = generated_text  # Save generated text to session state
            st.text_area("Generated Code", value=generated_text, height=400, disabled=True)
        else:
            st.warning("Please initialize the model first.")

# Button to Move Generated Code to Input
if st.button("↻ Move"):
    if 'generated_text' in st.session_state:
        # Update the input text area with the generated text
        st.session_state['input_text'] = st.session_state['generated_text']
        # This will automatically update the input text area since its value is tied to 'input_text' session state
    else:
        st.warning("Please generate some code first.")



