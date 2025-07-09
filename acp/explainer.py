from acp_sdk.server import Server, RunYield, RunYieldResume
from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv

load_dotenv

server = Server()

model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash-8b",
    api_key=os.getenv("GEMINI_API"),
)

@server.agent()
async def explainer(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    """This is an Agent that explains code solutions line by line."""
    agent = AssistantAgent(
        name="explainer",
        model_client=model_client,
        system_message="Explain given code line by line and the solution as a whole.",
    )
    prompt = input[0].parts[0].content
    result = await agent.run(task=prompt)

    yield Message(parts=[MessagePart(content=str(result.messages[-1].content))])


if __name__ == "__main__":
    server.run(port=8001)