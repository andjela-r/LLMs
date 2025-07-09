# ACP (Agent Communication Protocol)

## Setup
1. Create `.env` with the following content:
    ```
    HF_TOKEN=your_huggingface_token
    GEMINI_API=your_gemini_api_key
    ```
2. Install dependencies with `uv add`:
    - acp-sdk
    - autogen-agentchat
    - autogen-ext[openai]
    - colorama
    - python-dotenv
    - smolagents[toolkit]
    
## Running with `uv`
1. Run `uv run coder.py`
2. In another terminal, run `uv run explainer.py`
3. In another terminal, run `uv run main.py`

