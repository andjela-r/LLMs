from smolagents import CodeAgent, InferenceClientModel
from acp_sdk.server import Server, RunYield, RunYieldResume
from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from huggingface_hub import HfApi
import os

server = Server()

api = HfApi(token=os.getenv("HF_TOKEN"))

@server.agent()
async def coder(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """This is a CodeAgent that solves Leetcode questions and returns the source code of the solutions."""
    agent = CodeAgent(tools=[], model=InferenceClientModel(), add_base_tools=True)

    prompt = input[0].parts[0].content
    response = agent.run(prompt)

    yield Message(parts=[MessagePart(content=str(response))])

if __name__ == "__main__":
    server.run(port=8000)