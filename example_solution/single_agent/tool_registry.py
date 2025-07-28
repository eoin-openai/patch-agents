import threading
from collections import defaultdict
from typing import Callable

from agents import function_tool
from example_solution.single_agent.constants import TOOL_CALL_COLOR
from example_solution.single_agent.utils import DF

_intent_categories = defaultdict(str)
for intent, category in DF[["intent", "category"]].drop_duplicates().values:
    _intent_categories[intent] = category


# Lists of events for each tool call for use in synchronous evaluation.
# Note that this global tracking is not recommended for real use cases, and
# is only used here for simplicity in running the evaluations.
TOOL_EVENTS: list[dict[str, str]] = []
_append_lock = threading.Lock()


def thread_safe_append(event: dict[str, str]) -> None:
    with _append_lock:
        TOOL_EVENTS.append(event)


def _make_tool(intent: str, category: str) -> Callable[[str], None]:
    """
    Creates a tool function for the given intent and category.
    """

    @function_tool(name_override=intent, description_override=category)
    def tool(query: str) -> None:
        print(f"{TOOL_CALL_COLOR}Tool '{intent}' called with query: {query}\033[0m")
        thread_safe_append({"intent": intent, "category": category, "query": query})
        return

    tool.__name__ = intent
    return tool


TOOLS: list[Callable[[str], None]] = [
    _make_tool(intent, category) for intent, category in _intent_categories.items()
]


__all__ = ["TOOLS", "TOOL_EVENTS", "thread_safe_append"]
