"""Agent for the Streamlit demo."""

import json
import uuid
from pprint import pprint
from langchain_core.messages import HumanMessage
from langgraph_sdk import get_client


class Agent:
    """Agent wrapper."""

    def __init__(self, thread_id: str) -> None:
        """Initialize the agent."""
        self.thread_id = thread_id
        self.client = get_client(url="http://localhost:2024")

    async def maybe_create_thread(self) -> None:
        """Create a thread if it doesn't exist."""
        try:
            await self.client.threads.get(self.thread_id)
        except Exception:
            await self.client.threads.create(
                thread_id=self.thread_id, if_exists="do_nothing"
            )

    async def get_past_messages(self) -> list[dict]:
        """Get past messages from an existing agent."""
        await self.maybe_create_thread()
        past_state = await self.client.threads.get_history(self.thread_id)
        if len(past_state) > 0:
            return past_state[0]["values"]["messages"]
        return []

    async def update_message(self, message: dict) -> None:
        """Update a message.

        Old message will be replaced according to the message id.
        If the message id is not found, the message will be appended to the end
        of the messages.

        Args:
            message: The message to update.
        """
        past_messages = await self.get_past_messages()
        await self.client.threads.update_state(
            self.thread_id,
            values={"messages": past_messages + [message]},
        )

    async def get_response(
        self,
        user_input: HumanMessage,
    ) -> list[dict]:
        """Get response from an existing agent and return new messages."""
        past_messages = await self.get_past_messages()
        response = await self.client.runs.wait(
            self.thread_id,
            "ui_agent",  # Name of assistant. Defined in langgraph.json.
            input={
                "messages": [
                    user_input.model_dump(),
                ],
            },
        )
        return response["messages"][len(past_messages) :]


if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()

    def update_tool_data(message: dict) -> dict:
        """Update the tool data."""
        data = json.loads(message["content"])
        data["value"] = 10
        message["content"] = json.dumps(data)
        return message

    async def main():
        """Run the demo agent."""
        agent = Agent(thread_id=str(uuid.uuid4()))

        result = await agent.get_response(
            "Generate a number input between 0 and 100",
        )
        pprint(result)

        updated_tool_message = None
        for msg in result:
            if msg["type"] == "tool":
                updated_tool_message = update_tool_data(msg)
                await agent.update_message(updated_tool_message)

        result = await agent.get_response(
            "What is the value of the number input?",
        )
        pprint(result)

        # result = await agent.get_response(
        #     "What did I just ask?",
        # )
        # pprint(result)

        # result = await agent.get_response(
        #     "What is the value of the number input?",
        # )
        # pprint(result)

    asyncio.run(main())
