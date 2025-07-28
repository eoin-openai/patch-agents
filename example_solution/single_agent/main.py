import asyncio

from agents import Runner, trace
from example_solution.single_agent.agent_registry import agent
from example_solution.single_agent.constants import AGENT_COLOR, USER_COLOR


async def main():
    print(
        f"{AGENT_COLOR}Bootcamp Support Agent is running. Type a message or 'exit' to quit."
    )
    while True:
        user_input = input(f"{USER_COLOR}User: ")
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print(f"{AGENT_COLOR}Exiting.")
            break
        # Trace the agent run for visibility
        with trace("bootcamp_support_agent"):
            result = await Runner.run(agent, user_input)
        print(f"{AGENT_COLOR}Agent: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
