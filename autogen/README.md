# Autogen

To run the model and test the notebooks, follow these steps:

1. Install and start Docker

2. Build and run the container  
In the terminal, run:

```bash
docker build -t model-service .
docker run -p 8000:8000 model-service
```
[Optional] Install Python requirements
If you plan to run the notebook locally, make sure to install the required dependencies:

```bash
pip install -r requirements.txt
```
Once that’s done, you’re all set to run the notebook.

## Switching Models
To use a different model, modify the `generate_text()` function in `model.py` as needed—just make sure to preserve the return format for compatibility.

