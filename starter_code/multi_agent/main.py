"""
Interactive runner for the multi-agent Bootcamp Support demo.

This closely mirrors the `examples/customer_service` demo: we keep
track of which agent is currently handling the conversation and show
hand-offs, tool calls, and messages as they occur.
"""

from __future__ import annotations

import asyncio
import uuid

from agents import (
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    trace,
)

from .agent_registry import triage_agent


async def main() -> None:
    print("Bootcamp Support (multi-agent) is running. Type 'exit' to quit.\n")

    current_agent = triage_agent
    input_items: list = []  # Runner expects a list of TResponseInputItem

    # Use a random UUID as a conversation ID so that a single run
    # appears together in traces (if you are using the agents tracing UI).
    conversation_id = uuid.uuid4().hex[:16]

    while True:
        user = input("User: ")
        if user.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        with trace("bootcamp_support_multi_agent", group_id=conversation_id):
            input_items.append({"content": user, "role": "user"})

            result = await Runner.run(current_agent, input_items)

            # Display everything the agent(s) produced during this turn.
            for new_item in result.new_items:
                agent_name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(f"{agent_name}: {ItemHelpers.text_message_output(new_item)}")
                elif isinstance(new_item, HandoffOutputItem):
                    print(
                        f"[Handoff] Conversation transferred from "
                        f"{new_item.source_agent.name} → {new_item.target_agent.name}"
                    )
                elif isinstance(new_item, ToolCallItem):
                    tool_name = getattr(getattr(new_item, "raw_item", None), "name", "<unknown>")
                    print(f"{agent_name}: Calling tool '{tool_name}' …")
                elif isinstance(new_item, ToolCallOutputItem):
                    print(f"{agent_name}: Tool output → {new_item.output}")
                else:
                    # Unknown/unsupported item type – just skip it.
                    pass

            # Prepare for the next turn.
            input_items = result.to_input_list()
            current_agent = result.last_agent


if __name__ == "__main__":
    asyncio.run(main())
