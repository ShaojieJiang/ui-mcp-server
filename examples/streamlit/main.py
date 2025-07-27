"""Chat with the agent."""

import asyncio
import uuid
import streamlit as st
from agent import Agent
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage


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

    def display_messages(self) -> None:
        """Display the messages."""
        for message in self.messages:
            with st.chat_message(message.type):
                st.write(message.content)

    def get_agent_response(self, user_input: str) -> None:
        """Get the agent response."""
        self.messages.extend(asyncio.run(self.agent.get_response(user_input)))
        st.rerun()

    def main(self) -> None:
        """Main function."""
        st.title("Chat with UI Agent")
        self.display_messages()

        if user_input := st.chat_input("Input your message..."):
            st.chat_message("user").write(user_input)
            self.get_agent_response(user_input)


if "page" not in st.session_state:
    st.session_state.page = ChatPage()
st.session_state.page.main()
