from __future__ import annotations

import asyncio
import uuid

from agents import (
    HandoffOutputItem,
    InputGuardrailTripwireTriggered,
    ItemHelpers,
    MessageOutputItem,
    OutputGuardrailTripwireTriggered,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    trace,
)
from example_solution.multi_agent.agent_registry import triage_agent
from example_solution.multi_agent.constants import (
    AGENT_COLOR,
    GUARDRAIL_COLOR,
    INFO_COLOR,
    TOOL_CALL_COLOR,
    USER_COLOR,
)


async def main() -> None:
    print(
        f"{INFO_COLOR}Bootcamp Support (multi-agent) is running. Type 'exit' to quit.\n"
    )

    current_agent = triage_agent
    input_items: list = []  # Runner expects a list of TResponseInputItem

    conversation_id = uuid.uuid4().hex[:16]

    while True:
        user = input(f"{USER_COLOR}User: ")
        if user.lower() in {"exit", "quit"}:
            print("Exiting.")
            break

        with trace("bootcamp_support_multi_agent", group_id=conversation_id):
            input_items.append({"content": user, "role": "user"})

            try:
                result = await Runner.run(current_agent, input_items)
            except (
                InputGuardrailTripwireTriggered,
                OutputGuardrailTripwireTriggered,
            ) as e:
                print(f"{GUARDRAIL_COLOR}{e.guardrail_result.output.output_info}")
                break

            # Display everything the agent(s) produced during this turn.
            for new_item in result.new_items:
                agent_name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(
                        f"{AGENT_COLOR}{agent_name}: {ItemHelpers.text_message_output(new_item)}"
                    )
                elif isinstance(new_item, HandoffOutputItem):
                    print(
                        f"{INFO_COLOR}[Handoff] Conversation transferred from "
                        f"{new_item.source_agent.name} → {new_item.target_agent.name}"
                    )
                elif isinstance(new_item, ToolCallItem):
                    tool_name = getattr(
                        getattr(new_item, "raw_item", None), "name", "<unknown>"
                    )
                    print(
                        f"{TOOL_CALL_COLOR}{agent_name}: Calling tool '{tool_name}' …"
                    )
                elif isinstance(new_item, ToolCallOutputItem):
                    print(
                        f"{TOOL_CALL_COLOR}{agent_name}: Tool output → {new_item.output}"
                    )
                else:
                    # Unknown/unsupported item type – just skip it.
                    pass

            # Prepare for the next turn.
            input_items = result.to_input_list()
            current_agent = result.last_agent


if __name__ == "__main__":
    asyncio.run(main())
