# CodeWritingAssistantLLM
The CodeWritingAssistantLLM app is an innovative programming assistant designed to support developers in creating code quickly and efficiently using advanced natural language models (LLM). 

The application was created for training purposes and will not be used for commercial purposes.

## Features
### GPU compatibility check
Make sure your system has a CUDA-enabled GPU to take advantage of accelerated model inference. The application automatically checks GPU availability and provides feedback. For the current implementation, having CUDA is mandatory.

### Model Initialization

This section of the application is dedicated to preparing the machine learning components necessary for generating code based on user input. It involves two key steps:

- **Model Checkpoint**: The user specifies the identifier of a pre-trained model hosted on Hugging Face's model hub. This identifier points to a specific model that has been trained on vast amounts of code and is capable of understanding and generating code snippets. The model checkpoint acts as a reference to load the exact model configuration and weights.

- **Initialize**: Upon providing the model checkpoint, the application proceeds to load both the model and its associated tokenizer into memory. The tokenizer is responsible for converting user input text into a format that the model can understand (tokenization) and converting the model's output tokens back into human-readable text. Loading the model involves initializing it with the pre-trained weights specified by the checkpoint and preparing it for inference on the specified computing device (e.g., a CUDA-enabled GPU for accelerated performance).

### Generating code

Here's where the magic happens: users enter their code they'd like to expand, adjust the length of the output code with the slider, and click "Generate" to generate a new code snippet. It involves five key steps:

- **Input text**: Users write their code for which they would like to receive a further section. This can be anything from simple functions to more complex logic.
- **Output Length Adjustment**: A slider allows users to control the length of the generated code. The higher the number of generated tokens we set, the more our assistant will prompt more from itself. If we want the assistant not to suggest too much to us, set a small number of generated tokens;
- **Code Generation**: After clicking the "Generate" button, the application processes the input, using a pre-trained LLM to predict what code snippets will best fit the given input.
- **Display Results**: Automatically generated code is displayed, ready for review, customization or integration into a project.
- **Looping**:  If we would like to continue generating new code to what has already been generated then we can press the 'Move' button, which will automatically move our generated output to the input cell. This can help us speed up our code work.


## Installation

To get started with My Code Generation App, follow these installation steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Krukrukk/CodeWritingAssistantLLM.git
   cd my-code-generation-app
   ```

2. **Set Up a Python Virtual Environment** (Optional but recommended):
    ```bash
    python -m venv llm_venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage
   To launch the application, run:
    ```bash
    streamlit run app.py 
    ```
Navigate to the displayed URL in your web browser to interact with the app.

## License

My Code Generation App is released under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.

## Reference
- **Hugging Face** 
    - https://huggingface.co/blog/starcoder
    - https://huggingface.co/blog/starcoder2
    - https://huggingface.co/bigcode/starcoder2-3b
    - https://huggingface.co/docs/transformers/main/model_doc/starcoder2
    - https://huggingface.co/spaces/bigcode/bigcode-model-license-agreement
- **StreamLit** 
    - https://streamlit.io
- **Pytorch**
    - https://pytorch.org
