from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import DefaultAzureCredential
import os

from utils.memory_provider import UserMemoryProvider

def initialize_stockz_agent():
    
    credential = DefaultAzureCredential()

    client = FoundryChatClient(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model=os.getenv("DEPLOYMENT_NAME"),
        credential=credential,
    )

    with open("agent-instruction.md", "r", encoding="utf-8") as f:
        agent_instructions = f.read()

    web_search_tool = client.get_web_search_tool(
        user_location={"city": "Mumbai", "region": "India"},
    )
    code_interpreter_tool = client.get_code_interpreter_tool()

    tapetide_mcp = client.get_mcp_tool(
        name="Tapetide MCP",
        url="https://mcp.tapetide.com/mcp",
        headers={"Authorization": f"Bearer {os.getenv("TAPETIDE_API_KEY")}"},
        approval_mode="never_require",
    )

    agent = Agent(
        name="StockzAgent",
        instructions=agent_instructions,
        client=client,
        context_providers=[UserMemoryProvider()],   
        tools=[
            web_search_tool,
            code_interpreter_tool,
            tapetide_mcp
        ]
    )   

    return agent
