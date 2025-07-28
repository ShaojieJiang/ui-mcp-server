"""Backend Agent."""

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


async def create_agent(model: str):
    """Create a backend agent."""
    client = MultiServerMCPClient(
        {
            "ui-mcp-server": {
                "command": "uvx",
                "args": ["ui-mcp-server"],
                "transport": "stdio",
            }
        }
    )
    tools = await client.get_tools()
    prompt_msg = await client.get_prompt("ui-mcp-server", "ui_component_prompt")
    prompt = prompt_msg[-1].content

    return create_react_agent(model, tools, prompt=prompt)


agent = asyncio.run(create_agent(model="openai:gpt-4o-mini"))
