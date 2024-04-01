"""
Title: CodeWritingAssistantLLM App
Author: Maciej Małecki
Last_update: 2024-03-30
"""

import streamlit as st
from utils.cfg_reader import Configuration
from script.services import *


def main():
    cfg_app = Configuration("config/config_app.cfg")

    st.title(cfg_app["Front"]["title"])
    st.write(cfg_app["Front"]["description"])

    st.write("____")
    create_instruction_section(cfg_app)
    st.write("____")
    _, _, gpu_memory = check_gpu_section()
    st.write("____")
    initialization_model_section(gpu_memory, cfg_app)
    generate_code_section(cfg_app)
    create_code_move_button()


if __name__ == "__main__":
    main()
