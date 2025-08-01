"""Backend Agent."""

import os
from typing import Annotated, Literal
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field


DEFAULT_PROMPT = """You are an intelligent assistant that can operate the file 
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
- When the user has selected a file, you should display the file in the UI.
"""


class Configuration(BaseModel):
    """Configuration for the agent."""

    system_prompt: str = Field(
        default=DEFAULT_PROMPT,
        description="The system prompt for the agent.",
    )
    model: Annotated[
        Literal[
            "openai:gpt-4o",
            "openai:gpt-4o-mini",
            "google:gemini-2.5-flash",
            "google:gemini-2.5-pro",
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="openai:gpt-4o",
        description="The model to use for the agent.",
    )


def get_model(model_name: str) -> str | ChatGoogleGenerativeAI:
    """Get the model."""
    if model_name.startswith("google:"):
        return ChatGoogleGenerativeAI(
            model=model_name.split(":")[1],
        )
    return model_name


async def agent(config: RunnableConfig):
    """Create a backend agent."""
    configurable = config.get("configurable", {})

    model = get_model(configurable.get("model", "google:gemini-2.5-flash"))
    prompt = configurable.get("system_prompt", DEFAULT_PROMPT)

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
            "tavily-search": {
                "url": "https://mcp.tavily.com/mcp/?tavilyApiKey="
                + os.environ.get("TAVILY_API_KEY"),
                "transport": "streamable_http",
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
