"""Agent for the Streamlit demo."""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent


async def create_agent(model: str = "openai:gpt-4o-mini") -> CompiledStateGraph:
    """Create an agent with MCP tools."""
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
    checkpointer = InMemorySaver()

    return create_react_agent(
        model,
        tools,
        prompt=prompt,
        checkpointer=checkpointer,
    )


async def get_agent_response(
    user_input: str,
    agent,
    config: dict | None = None,
) -> str:
    """Get response from an existing agent."""
    if config is None:
        config = {}
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
    )
    return response


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()
    checkpointer = InMemorySaver()

    async def main():
        """Run the demo agent."""
        agent = await create_agent()
        config = {"configurable": {"thread_id": "1"}}

        result = await get_agent_response(
            "Generate a number input between 0 and 100",
            agent,
            config,
        )
        print(result)

    asyncio.run(main())
