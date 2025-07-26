"""Streamlit demo main module."""

import asyncio
import json
from typing import Any
import streamlit as st
from agent import create_agent, get_agent_response
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Load environment variables
load_dotenv()


def render_ui_component(component_data: dict[str, Any]) -> None:  # noqa: C901 PLR0912 PLR0915
    """Render a UI component based on the provided dictionary data."""
    try:
        component_type = component_data.get("type", "").lower()
        label = component_data.get("label", "Component")
        key = component_data.get("key", f"component_{hash(str(component_data))}")

        if component_type == "number_input":
            min_value = component_data.get("min_value", 0)
            max_value = component_data.get("max_value", 100)
            value = component_data.get("value", min_value)
            step = component_data.get("step", 1)
            st.number_input(
                label,
                min_value=min_value,
                max_value=max_value,
                value=value,
                step=step,
                key=key,
            )

        elif component_type == "slider":
            min_value = component_data.get("min_value", 0)
            max_value = component_data.get("max_value", 100)
            value = component_data.get("value", min_value)
            step = component_data.get("step", 1)
            st.slider(
                label,
                min_value=min_value,
                max_value=max_value,
                value=value,
                step=step,
                key=key,
            )

        elif component_type == "selectbox":
            options = component_data.get("options", [])
            index = component_data.get("index", 0)
            st.selectbox(label, options, index=index, key=key)

        elif component_type == "multiselect":
            options = component_data.get("options", [])
            default = component_data.get("default", [])
            st.multiselect(label, options, default=default, key=key)

        elif component_type == "radio":
            options = component_data.get("options", [])
            index = component_data.get("index", 0)
            st.radio(label, options, index=index, key=key)

        elif component_type == "checkbox":
            value = component_data.get("value", False)
            st.checkbox(label, value=value, key=key)

        elif component_type == "text_input":
            value = component_data.get("value", "")
            placeholder = component_data.get("placeholder", "")
            st.text_input(label, value=value, placeholder=placeholder, key=key)

        elif component_type == "text_area":
            value = component_data.get("value", "")
            height = component_data.get("height", None)
            st.text_area(label, value=value, height=height, key=key)

        elif component_type == "button":
            button_type = component_data.get("button_type", "secondary")
            if st.button(label, type=button_type, key=key):
                st.success(f"Button '{label}' clicked!")

        elif component_type in ("dataframe", "table"):
            data = component_data.get("data", [])
            if data:
                st.dataframe(data, key=key)
            else:
                st.write("No data provided for table")

        elif component_type == "form":
            form_fields = component_data.get("fields", [])
            with st.form(key=key):
                for field in form_fields:
                    render_ui_component(field)
                if st.form_submit_button("Submit"):
                    st.success("Form submitted!")

        elif component_type == "columns":
            columns_data = component_data.get("columns", [])
            if columns_data:
                cols = st.columns(len(columns_data))
                for i, col_data in enumerate(columns_data):
                    with cols[i]:
                        if isinstance(col_data, dict):
                            render_ui_component(col_data)
                        else:
                            st.write(col_data)

        elif component_type == "metric":
            value = component_data.get("value", "")
            delta = component_data.get("delta", None)
            st.metric(label, value, delta=delta)

        elif component_type == "progress":
            value = component_data.get("value", 0)
            st.progress(value)

        elif component_type == "json":
            data = component_data.get("data", component_data)
            st.json(data)

        else:
            # Fallback: display as JSON for unknown component types
            st.json(component_data)

    except Exception as e:
        st.error(f"Error rendering component: {str(e)}")
        st.json(component_data)  # Show raw data as fallback


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "checkpointer" not in st.session_state:
        st.session_state.checkpointer = InMemorySaver()
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = "streamlit-chat"


async def get_mcp_response(user_input: str):
    """Get response from MCP agent."""
    server_params = StdioServerParameters(
        command="uvx",
        args=["ui-mcp-server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Create agent for this request
            agent = await create_agent(
                session, checkpointer=st.session_state.checkpointer
            )

            # Get agent response
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            return await get_agent_response(user_input, agent, config)


def debug_response_structure(response):
    """Debug and log response structure."""
    st.write(f"Response type: {type(response)}")
    st.write(f"Response has messages attr: {hasattr(response, 'messages')}")
    st.write(f"Response is dict: {isinstance(response, dict)}")
    if hasattr(response, "messages") or (
        isinstance(response, dict) and "messages" in response
    ):
        messages = (
            response.messages if hasattr(response, "messages") else response["messages"]
        )
        st.write(f"Number of messages: {len(messages)}")
        for i, msg in enumerate(messages):
            st.write(f"Message {i}: {type(msg).__name__}")


def process_response_messages(response):
    """Process and add response messages to session state."""
    messages = None
    if hasattr(response, "messages"):
        messages = response.messages
    elif isinstance(response, dict) and "messages" in response:
        messages = response["messages"]

    if messages:
        # Skip the first message if it's the user's input (HumanMessage)
        start_idx = (
            1 if messages and str(type(messages[0]).__name__) == "HumanMessage" else 0
        )

        for message in messages[start_idx:]:
            message_type = str(type(message).__name__)

            # Handle AIMessages with content (skip empty AI messages)
            if message_type == "AIMessage":
                content = getattr(message, "content", "")
                if content and content.strip():
                    st.session_state.messages.append(
                        {"role": "assistant", "content": content}
                    )

            # Handle ToolMessages
            elif message_type == "ToolMessage":
                st.session_state.messages.append(
                    {"role": "assistant", "content": json.loads(message.content)}
                )
    else:
        # Fallback for unexpected response format
        st.session_state.messages.append(
            {"role": "assistant", "content": str(response)}
        )


async def handle_user_input(user_input: str):
    """Handle user input and get agent response."""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner("Thinking..."):
            response = await get_mcp_response(user_input)

        # Debug response structure
        debug_response_structure(response)

        # Process the response messages
        process_response_messages(response)

    except Exception as e:
        st.error(f"Error getting response: {str(e)}")


def display_chat_history():
    """Display the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], str):
                st.write(message["content"])
            else:  # dict
                render_ui_component(message["content"])


async def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="UI MCP Server Chat Demo", page_icon="🤖", layout="wide"
    )

    st.title("🤖 UI MCP Server Chat Demo")
    st.caption("Chat with an AI agent that can generate interactive UI components!")

    # Initialize session state
    initialize_session_state()

    # Test MCP server availability
    if "mcp_available" not in st.session_state:
        with st.spinner("Checking MCP server availability..."):
            try:
                server_params = StdioServerParameters(
                    command="uvx",
                    args=["ui-mcp-server"],
                )
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        st.session_state.mcp_available = True
                        st.success("✅ MCP server is available!")
            except Exception as e:
                st.error(f"❌ MCP server not available: {str(e)}")
                st.error(
                    "Make sure you have installed ui-mcp-server: "
                    "`pip install ui-mcp-server`"
                )
                st.stop()

    # Create two columns: chat and sidebar with examples
    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader("💡 Try these examples:")
        example_prompts = [
            "Create a number input for age between 0 and 120",
            "Generate a slider for temperature from -10 to 50",
            "Make a radio button for choosing colors: red, blue, green",
            "Create a multiselect for programming languages: Python, "
            "JavaScript, Go, Rust",
            "Show a table with sample user data",
            "Generate a form with name input and country selection",
        ]

        for prompt in example_prompts:
            if st.button(
                prompt,
                key=f"example_{hash(prompt)}",
                use_container_width=True,
            ):
                await handle_user_input(prompt)
                st.rerun()

    with col1:
        # Display chat history
        st.subheader("💬 Chat")
        display_chat_history()

        # Chat input
        if user_input := st.chat_input("Ask me to generate UI components..."):
            await handle_user_input(user_input)
            st.rerun()

        # Clear chat button
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    asyncio.run(main())
