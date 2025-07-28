from example_solution.single_agent.constants import (
    AGENT_COLOR,
    NUM_EXAMPLES,
    RANDOM_STATE,
    SYSTEM_PROMPT_COLOR,
    TOOL_CALL_COLOR,
    USER_COLOR,
)
from example_solution.single_agent.utils import DF

INFO_COLOR = "\033[96m"  # Cyan
GUARDRAIL_COLOR = "\033[91m"  # Red


__all__ = [
    "INFO_COLOR",
    "USER_COLOR",
    "AGENT_COLOR",
    "TOOL_CALL_COLOR",
    "SYSTEM_PROMPT_COLOR",
    "DF",
    "GUARDRAIL_COLOR",
    "NUM_EXAMPLES",
    "RANDOM_STATE",
]
