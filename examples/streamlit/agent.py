"""Agent for the Streamlit demo."""

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.types import Checkpointer
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def create_agent(
    session: ClientSession,
    model: str = "openai:gpt-4o-mini",
    checkpointer: Checkpointer | None = None,
):
    """Create an agent with MCP tools."""
    tools = await load_mcp_tools(session)
    prompt_msg = await session.get_prompt("ui_component_prompt")
    prompt = prompt_msg.messages[-1].content.text
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
        server_params = StdioServerParameters(
            command="uvx",
            args=["ui-mcp-server@latest"],
        )
        # TODO: find a more elegant way to maintain the session
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                agent = await create_agent(session, checkpointer=checkpointer)
                config = {"configurable": {"thread_id": "1"}}

                result = await get_agent_response(
                    "Generate a number input between 0 and 100",
                    agent,
                    config,
                )
                print(result)

    asyncio.run(main())
