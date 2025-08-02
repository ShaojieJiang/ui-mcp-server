"""Chat with the agent."""

import asyncio
import base64
import json
import uuid
from typing import Any
import streamlit as st
from agent import Agent
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from streamlit.elements.widgets.chat import ChatInputValue
from streamlit.runtime.uploaded_file_manager import UploadedFile


load_dotenv()


class ChatPage:
    """Chat page."""

    def __init__(self) -> None:
        """Initialize the chat page."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
        self.messages: list[dict] = st.session_state.messages
        self.agent = Agent(thread_id=st.session_state.session_id)

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

    async def display_ui_component(self, message: dict) -> None:
        """Display the UI component."""
        data = json.loads(message["content"])
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
                with st.form(key=message["tool_call_id"]):
                    user_input = self.display_input_form(data)
                    submit_button = st.form_submit_button("Submit")
                    if submit_button:
                        await self.update_ui_input(message, user_input)
                        await self.get_agent_response(
                            f"My input to {data['label']} is {user_input}"
                        )
            case "line" | "bar" | "scatter" | "image" | "audio" | "video":
                self.display_output_component(data)
            case _:
                st.write("Unable to display the UI component.")
                st.write(data)

    async def update_ui_input(self, message: dict, user_input: Any) -> None:
        """Update the user input."""
        data = json.loads(message["content"])
        data["value"] = user_input
        message["content"] = json.dumps(data)
        await self.agent.update_message(message)

    async def display_messages(self) -> None:
        """Display the messages."""
        for message in self.messages:
            message_type = (
                message["type"] if message["type"] != "tool" else "assistant"
            )  # display tool messages as assistant messages
            if not message["content"]:
                continue
            with st.chat_message(message_type):
                if message["type"] == "tool":
                    await self.display_ui_component(message)
                else:
                    msg_content = message["content"]
                    if isinstance(msg_content, str):
                        st.write(msg_content)
                    else:
                        for content in msg_content:
                            content_type = content["type"]
                            if content_type == "text":
                                st.write(content["text"])
                            elif content_type == "image_url":
                                st.image(content["image_url"]["url"])

    def image_to_base64(self, image: UploadedFile) -> str:
        """Convert the image to base64."""
        return base64.b64encode(image.read()).decode("utf-8")

    async def get_agent_response(self, user_input: ChatInputValue) -> None:
        """Get the agent response."""
        user_message = HumanMessage(
            content=[{"type": "text", "text": user_input.text}]
            + [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{file.type};base64,{self.image_to_base64(file)}"
                    },
                }
                for file in user_input.files
            ]
        )
        self.messages.extend(await self.agent.get_response(user_message))
        st.rerun()

    async def main(self) -> None:
        """Entry point."""
        st.title("Chat with `ui-mcp-server`")
        await self.display_messages()

        if user_input := st.chat_input(
            "Input your message...",
            accept_file="multiple",
            file_type=["jpg", "jpeg", "png"],
        ):
            if isinstance(user_input, ChatInputValue):
                with st.chat_message("user"):
                    st.write(user_input.text)
                    for file in user_input.files:
                        st.image(file)
                await self.get_agent_response(user_input)
            else:
                st.write(f"Unknown user input type: {type(user_input)}")
                st.chat_message("user").write(user_input)


if "page" not in st.session_state:
    st.session_state.page = ChatPage()
asyncio.run(st.session_state.page.main())
