from script.sys_tools import check_gpu, print_memory_footprint
from script.LLM_fun import initialize_model, generate_text
import streamlit as st


def create_instruction_section(cfg_app):
    """
    Creates a section in the Streamlit UI to display instructional content.

    Parameters:
    - cfg_app (dict): Configuration settings loaded from a file, containing keys for 'Section_Instruction' which
                      include 'header', 'description', and 'licence_protection'.
    """
    with st.container():
        st.header(cfg_app["Section_Instruction"]["header"])
        st.write(cfg_app["Section_Instruction"]["description"])
        st.write(cfg_app["Section_Instruction"]["licence_protection"])


def check_gpu_section():
    """
    Checks and displays the GPU status in the Streamlit UI.

    This function checks if a GPU is available and displays its status, name, and memory. If a GPU is not found,
    it displays an error message and stops the application from proceeding further.

    Returns:
    - gpu_status (bool): Whether the GPU is available or not.
    - gpu_name (str): The name of the GPU, if available.
    - gpu_memory (float): The memory of the GPU in GB, if available.
    """
    with st.container():
        st.header("Check GPU Status")
        gpu_status, gpu_name, gpu_memory = check_gpu()
        if gpu_status:
            st.success(f"✔️ GPU Connected: {gpu_name}, Memory: {gpu_memory:.2f} GB")
        else:
            st.error(
                "You need to correctly install the drivers for your graphics card in order to use the application."
            )
            st.stop()
    return gpu_status, gpu_name, gpu_memory


def initialization_model_section(gpu_memory, cfg_app):
    """
    Initializes the LLM and displays the status in the Streamlit UI.

    Allows the user to input a model checkpoint and initializes the model with the specified device. It checks if
    the GPU has sufficient memory to load the model. If the model is successfully initialized, it updates the session
    state to indicate the model is ready for text generation.

    Parameters:
    - gpu_memory (float): The available GPU memory in GB.
    - cfg_app (dict): Configuration settings loaded from a file, containing keys for model checkpoint and device.
    """
    with st.container():
        st.header("Initialize Model")
        checkpoint = st.text_input(
            "Model Checkpoint", value=cfg_app["Model"]["checkpoint"]
        )
        device = cfg_app["Model"]["device"]
        if "model_initialized" not in st.session_state:
            st.session_state["model_initialized"] = False

        if st.button("Initialize"):
            if not st.session_state["model_initialized"]:
                try:
                    tokenizer, model = initialize_model(
                        checkpoint=checkpoint, device=device
                    )
                    st.session_state["model"] = model
                    st.session_state["tokenizer"] = tokenizer
                    st.session_state["model_initialized"] = True
                    memory_footprint = print_memory_footprint(model)
                    if gpu_memory >= memory_footprint:
                        st.success(
                            f"Model initialized successfully! Memory used by the model: {memory_footprint:.2f} GB"
                        )
                    else:
                        st.error(
                            f"Insufficient GPU memory: {gpu_memory:.2f} GB available, but {memory_footprint:.2f} GB is required."
                        )
                        st.stop()
                except Exception as e:
                    st.error(f"Failed to initialize the model: {e}")
            else:
                st.success("Model already initialized. Ready to generate text!")


def generate_code_section(cfg_app):
    """
    Generates code based on the user's input using a pre-initialized model.

    This function creates a UI section where the user can input text and specify the number of new tokens to generate.
    Upon clicking the "Generate" button, it uses the pre-initialized model to generate code based on the user's input.
    The generated code is then displayed in the UI.

    Parameters:
    - cfg_app (dict): Configuration settings loaded from a file, specifically for the text generation section,
                      including default values and UI element sizes.
    """
    with st.container():
        st.header("Generate Code")
        input_text = st.text_area(
            "Input Text",
            value=st.session_state.get(
                "generated_text", cfg_app["Generation"]["default_code"]
            ),
            height=int(cfg_app["Generation"]["height_text_area_input"]),
        )
        max_new_tokens = st.slider(
            "Number of New Tokens",
            min_value=1,
            max_value=128,
            value=int(cfg_app["Generation"]["default_new_tokens"]),
        )
        if st.button("Generate"):
            if "model" in st.session_state and "tokenizer" in st.session_state:
                generated_text = generate_text(
                    st.session_state["tokenizer"],
                    st.session_state["model"],
                    input_text,
                    max_new_tokens=max_new_tokens,
                )
                st.session_state["generated_text"] = generated_text
                st.text_area(
                    "Generated Code",
                    value=generated_text,
                    height=int(cfg_app["Generation"]["height_text_area_output"]),
                    disabled=True,
                )
            else:
                st.warning("Please initialize the model first.")


def create_code_move_button():
    """
    Creates a button in the Streamlit UI to move the generated code to the input area.
    """
    if st.button("↻ Move"):
        if "generated_text" in st.session_state:
            st.session_state["input_text"] = st.session_state["generated_text"]
        else:
            st.warning("Please generate some code first.")
