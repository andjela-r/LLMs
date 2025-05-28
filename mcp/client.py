import gradio as gr
import os

from mcp.client.stdio import StdioServerParameters
from smolagents import InferenceClientModel, CodeAgent, ToolCollection
from smolagents.mcp_client import MCPClient


try:
    mcp_client = MCPClient(
        {"url": "http://localhost:7860/gradio_api/mcp/sse"}
    )
    tools = mcp_client.get_tools()

    hf_key = os.environ.get("HF_API_KEY")
    model = InferenceClientModel(api_key=hf_key)
    agent = CodeAgent(tools=[*tools], model=model)

    demo = gr.ChatInterface(
        fn=lambda message, history: str(agent.run(message)),
        type="messages",
        examples=[
            "Prime factorization of 68", 
            "How do I make scrambled eggs?", 
            "Convert 28 degrees Celsius to Fahrenheit"
            "What's the sentiment of this text?\n 'I am so angry, that movie made me upset.'"
        ],
        title="Agent with MCP Tools",
        description="This is a simple agent that uses MCP tools to answer questions.",
    )

    demo.launch()
finally:
    mcp_client.disconnect()