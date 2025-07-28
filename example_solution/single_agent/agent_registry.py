from agents import Agent
from example_solution.single_agent.config import (
    AGENT_MODEL,
)
from example_solution.single_agent.tool_registry import TOOLS
from example_solution.single_agent.utils import (
    get_example_queries,
    load_markdown_prompt,
)

agent = Agent(
    name="Bootcamp Support Agent",
    instructions=load_markdown_prompt(
        "single_agent.md",
        available_tools=[t.__name__ for t in TOOLS],
        examples=get_example_queries(),
    ),
    tools=TOOLS,
    model=AGENT_MODEL,
)

__all__ = ["agent"]
