"""
Interactive runner for the Bootcamp Support Agent.
"""

from agents import Runner, trace
from .agent_registry import agent
import asyncio

async def main():
    print("Bootcamp Support Agent is running. Type a message or 'exit' to quit.")
    while True:
        user_input = input("User: ")
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Exiting.")
            break
        # Trace the agent run for visibility
        with trace("bootcamp_support_agent"):
            result = await Runner.run(agent, user_input)
        print(f"Agent: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
