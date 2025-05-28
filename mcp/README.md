# 🛠️🤖 MCP (Model Context Protocol) Demo

This project is based on the [🤗 Hugging Face MCP Course 🤗](https://huggingface.co/learn/mcp-course/unit0/introduction), using Gradio for both the MCP server and MCP-powered agent client.

It demonstrates how to:  
- Register tools via an MCP-compatible Gradio server.  
- Build an agent that dynamically retrieves and uses those tools.  

## 🚀 What’s This Project?

This is a simple chat agent powered by MCP tools and a Hugging Face-hosted language model.
It uses:
- An MCP server that exposes a tool (sentiment analysis with TextBlob).
- An MCP client agent that can retrieve and invoke this tool using smolagents.


## 🛠 Setup

### Install Dependencies (in a virtual environment is recommended)
```python
pip install -r requirements.txt
```

### Set Your Hugging Face API Key
You’ll need this to run the agent with a model from Hugging Face Hub.

1. Replace in `mcp.json`
2. Create `.env` and add the same key with the same name as in `mcp.json`

### Start the MCP server with: 

```python
python server.py
```

- Hosts a sentiment analysis tool using Gradio.
- Accessible at: [http://localhost:7860](http://localhost:7860)

### Start the MCP client with:  

```python
python client.py
```

- Opens a Gradio chat interface.
- Accessible at: [http://localhost:7861](http://localhost:7861)
- The agent can now answer questions using the tools registered on the MCP server.
