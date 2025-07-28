"""
Definition of the Bootcamp Support Agent.
"""
from agents import Agent
from .tool_registry import TOOLS
from .config import MODEL

# Prepare instructions, listing available tools
tool_names = ", ".join([t.__name__ for t in TOOLS])
instructions = f"""
You are a customer support agent. For each user message, identify the intent and call the corresponding tool.
Available tools: {tool_names}.
Always invoke the appropriate tool by name; do not provide answers directly.
"""

# Create the agent with enforced tool use
agent = Agent(
    name="Bootcamp Support Agent",
    instructions=instructions,
    tools=TOOLS,
    model=MODEL,
)
