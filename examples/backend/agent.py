"""Backend Agent."""

import os
from typing import Annotated, Literal
from langchain_core.runnables import RunnableConfig
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field


class Configuration(BaseModel):
    """Configuration for the agent."""

    system_prompt: str = Field(
        default=(
            """You are an intelligent assistant that can operate the file 
system and generate UI components.

## How to react to user requests
- When the user asks for available files, you should first retrieve 
the files, and display them in a single choice component.
- When the user asks for displaying a media file, you should first 
retrieve the full path of the file and then display the file in the 
UI.
- When generating components, your next message should be simply referring to 
the component by saying "Please check the output above." Do not repeat the 
content of the component.
- When the user has selected a file, you should display the file in the UI."""
        ),
        description="The system prompt for the agent.",
    )
    model: Annotated[
        Literal["openai:gpt-4o", "openai:gpt-4o-mini"],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai:gpt-4o-mini",
        description="The model to use for the agent.",
    )


async def agent(config: RunnableConfig):
    """Create a backend agent."""
    configurable = config.get("configurable", {})

    model = configurable.get("model", "openai:gpt-4o-mini")
    prompt = configurable.get("system_prompt", "You are a helpful assistant.")

    client = MultiServerMCPClient(
        {
            "ui-mcp-server": {
                "command": "uvx",
                "args": ["ui-mcp-server"],
                "transport": "stdio",
            },
            "file-system": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    os.environ.get("FILE_SYSTEM_PATH", "/home/"),
                ],
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()

    return create_react_agent(
        model,
        tools,
        prompt=prompt,
        context_schema=Configuration,
    )
