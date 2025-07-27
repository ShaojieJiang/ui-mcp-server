"""Chat with the agent."""

import asyncio
import json
import uuid
from typing import Any
import streamlit as st
from agent import Agent
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage


load_dotenv()


class ChatPage:
    """Chat page."""

    def __init__(self) -> None:
        """Initialize the chat page."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
        self.messages: list[BaseMessage] = st.session_state.messages
        self.agent = Agent(
            config={"configurable": {"thread_id": st.session_state.session_id}}
        )

    def display_input_form(self, data: dict[str, Any]) -> None:
        """Display the input form."""
        match data["type"]:
            case "number_input":
                user_input = st.number_input(
                    label=data["label"],
                    min_value=data["min_value"],
                    max_value=data["max_value"],
                    value=data["value"],
                    step=data["step"],
                    key=data["key"],
                    help=data.get("help"),
                )
            case "slider":
                user_input = st.slider(
                    label=data["label"],
                    min_value=data["min_value"],
                    max_value=data["max_value"],
                    value=data["value"],
                    step=data["step"],
                    key=data["key"],
                    help=data.get("help"),
                )
            case "radio":
                user_input = st.radio(
                    label=data["label"],
                    options=data["options"],
                    index=None,
                    key=data["key"],
                    help=data.get("help"),
                )
            case "multiselect":
                user_input = st.multiselect(
                    label=data["label"],
                    options=data["options"],
                    default=data["value"],
                    key=data["key"],
                    help=data.get("help"),
                )
            case "color_picker":
                user_input = st.color_picker(
                    label=data["label"],
                    value=data["value"],
                    key=data["key"],
                    help=data.get("help"),
                )
            case "date_input":
                user_input = st.date_input(
                    label=data["label"],
                    value=data["value"],
                    min_value=data["min_value"],
                    max_value=data["max_value"],
                    format=data["format"],
                    key=data["key"],
                    help=data.get("help"),
                )
            case "time_input":
                user_input = st.time_input(
                    label=data["label"],
                    value=data["value"],
                    key=data["key"],
                    help=data.get("help"),
                    step=data["step"],
                )
            case "audio_input":
                user_input = st.audio_input(
                    label=data["label"],
                    key=data["key"],
                    help=data.get("help"),
                )
            case "camera_input":
                user_input = st.camera_input(
                    label=data["label"],
                    key=data["key"],
                    help=data.get("help"),
                )
            case _:
                st.write("Unable to display the UI component.")
                st.write(data)
                user_input = None
        return user_input

    def display_output_component(self, data: dict[str, Any]) -> None:
        """Display the output component."""
        match data["type"]:
            case "line":
                st.line_chart(
                    data["data"],
                    x_label=data["x_label"],
                    y_label=data["y_label"],
                )
            case "bar":
                st.bar_chart(
                    data["data"],
                    x_label=data["x_label"],
                    y_label=data["y_label"],
                )
            case "scatter":
                st.scatter_chart(
                    data["data"],
                    x_label=data["x_label"],
                    y_label=data["y_label"],
                )
            case "image":
                st.image(
                    data["url"],
                    caption=data["caption"],
                    width=data["width"],
                    clamp=data["clamp"],
                    channels=data["channels"],
                    output_format=data["output_format"],
                )
            case "audio":
                st.audio(
                    data["url"],
                    format=data["format"],
                    sample_rate=data["sample_rate"],
                    loop=data["loop"],
                    autoplay=data["autoplay"],
                )
            case "video":
                st.video(
                    data["url"],
                    format=data["format"],
                    subtitles=data["subtitles"],
                    muted=data["muted"],
                    loop=data["loop"],
                    autoplay=data["autoplay"],
                )
            case _:
                st.write("Unable to display the UI component.")
                st.write(data)

    def display_ui_component(self, message: ToolMessage) -> None:
        """Display the UI component."""
        data = json.loads(message.content)
        match data["type"]:
            case (
                "number_input"
                | "slider"
                | "radio"
                | "multiselect"
                | "color_picker"
                | "date_input"
                | "time_input"
                | "audio_input"
                | "camera_input"
            ):
                with st.form(key=message.tool_call_id):
                    user_input = self.display_input_form(data)
                    submit_button = st.form_submit_button("Submit")
                    if submit_button:
                        self.update_ui_input(message, user_input)
                        self.get_agent_response(
                            f"My input to {data['label']} is {user_input}"
                        )
            case "line" | "bar" | "scatter" | "image" | "audio" | "video":
                self.display_output_component(data)
            case _:
                st.write("Unable to display the UI component.")
                st.write(data)

    def update_ui_input(self, message: ToolMessage, user_input: Any) -> None:
        """Update the user input."""
        data = json.loads(message.content)
        data["value"] = user_input
        message.content = json.dumps(data)
        self.agent.update_message(message)

    def display_messages(self) -> None:
        """Display the messages."""
        for message in self.messages:
            message_type = (
                message.type if message.type != "tool" else "assistant"
            )  # display tool messages as assistant messages
            if not message.content:
                continue
            with st.chat_message(message_type):
                if message.type == "tool":
                    self.display_ui_component(message)
                else:
                    st.write(message.content)

    def get_agent_response(self, user_text: str) -> None:
        """Get the agent response."""
        self.messages.extend(asyncio.run(self.agent.get_response(user_text)))
        st.rerun()

    def main(self) -> None:
        """Main function."""
        st.title("Chat with `ui-mcp-server`")
        self.display_messages()

        if user_text := st.chat_input("Input your message..."):
            st.chat_message("user").write(user_text)
            self.get_agent_response(user_text)


if "page" not in st.session_state:
    st.session_state.page = ChatPage()
st.session_state.page.main()
