"""
Definition of the triage agent and all per-intent specialist agents.

The triage agent receives the user's message, determines the intent,
and then performs a hand-off to the appropriate intent agent.  Each
specialist agent is equipped with exactly one tool – the function
implementing the business logic for the intent it serves.
"""

from __future__ import annotations

from agents import Agent, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from bootcamp_agents.multi_agent.tool_registry import TOOLS

# ----------------------------------------------------------------------------
# Build one specialist agent for every tool/intent.
# ----------------------------------------------------------------------------

_intent_agents: list[Agent] = []

for _tool in TOOLS:
    _intent_name = _tool.__name__

    _intent_agent = Agent(
        name=f"{_intent_name} Agent",
        handoff_description=(
            f"Responds to customer requests classified with the '{_intent_name}' intent."
        ),
        instructions=(
            f"{RECOMMENDED_PROMPT_PREFIX}\n"
            f"You are the specialist agent for the customer intent '{_intent_name}'.\n"
            "Respond appropriately and completely in a friendly, professional tone.\n"
            "If you receive a message that is not relevant to this intent, transfer the conversation back to the triage agent.\n"
            "Do NOT call any tools."
        ),
        # No tools – this agent only produces a natural language response.
        # The hand-offs list will be completed after the triage agent is created.
    )

    _intent_agents.append(_intent_agent)

# ----------------------------------------------------------------------------
# Create the triage agent that delegates to the specialist agents.
# ----------------------------------------------------------------------------
triage_agent = Agent(
    name="Triage Agent",
    handoff_description="Routes the customer to the correct specialist agent based on intent.",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a triage agent for customer support. "
        "Read the user's latest message, determine its intent, and transfer the "
        "conversation to the specialist agent that best matches that intent. "
        "If you are not confident about the intent, ask clarifying questions instead of transferring."
    ),
    handoffs=[handoff(agent=a) for a in _intent_agents],
)

# ----------------------------------------------------------------------------
# Allow every specialist agent to send the conversation back to triage.
# ----------------------------------------------------------------------------

for _a in _intent_agents:
    _a.handoffs.append(triage_agent)


# What we expose from this module
__all__ = [
    "triage_agent",
]
