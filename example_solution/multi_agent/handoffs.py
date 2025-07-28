from typing import Any

from agents.handoffs import RunContextWrapper
from example_solution.multi_agent.tool_registry import thread_safe_append
from pydantic import BaseModel


class HandoffInput(BaseModel):
    query: str
    intent: str
    category: str


async def on_handoff(
    context: RunContextWrapper[Any],
    input: HandoffInput,
) -> None:
    """
    Tracks the handoff event for evaluation of tool calling.
    """
    thread_safe_append(
        {"intent": input.intent, "category": input.category, "query": input.query},
    )
    return None
