import asyncio
import os
from enum import Enum

import pandas as pd
from agents import Agent, Runner
from example_solution.multi_agent.agent_registry import triage_agent as multi_agent
from example_solution.multi_agent.tool_registry import TOOL_EVENTS
from example_solution.single_agent.agent_registry import agent as single_agent
from example_solution.single_agent.constants import RANDOM_STATE
from example_solution.single_agent.utils import DF
from openai import OpenAI


class AgentType(str, Enum):
    SINGLE = "single"
    MULTI = "multi"


async def run_query(agent: Agent, row: pd.Series) -> dict:
    """
    Runs a single query through the agent and returns a dictionary of results.
    """
    instruction = row["instruction"]
    messages = [{"role": "user", "content": instruction}]

    try:
        response = await Runner.run(agent, messages)
        predicted_answer = response.final_output
        predicted_intent = TOOL_EVENTS[-1]["intent"] if TOOL_EVENTS else None
        predicted_category = TOOL_EVENTS[-1]["category"] if TOOL_EVENTS else None
    except Exception:
        predicted_answer = None
        predicted_intent = None
        predicted_category = None

    return {
        "instruction": instruction,
        "expected_intent": row["intent"],
        "expected_category": row["category"],
        "expected_answer": row["response"],
        "predicted_answer": predicted_answer,
        "predicted_intent": predicted_intent,
        "predicted_category": predicted_category,
    }


async def run_agent_on_instructions(
    agent_type: AgentType, df_rows: pd.DataFrame
) -> pd.DataFrame:
    """
    Runs the agent on a set of instructions and returns a DataFrame of results.
    """
    agent = single_agent if agent_type == AgentType.SINGLE else multi_agent

    results = []
    for _, row in df_rows.iterrows():
        result = await run_query(agent, row)
        results.append(result)

    return pd.DataFrame(results)


async def grade_response(
    openai_client: OpenAI, instruction: str, predicted_answer: str, expected_answer: str
) -> int:
    """
    Grades a single response from the agent on a scale of 0 to 10.
    """
    prompt = f"""
    You are grading a response from an agent on a scale of 0 to 10, comparing against a gold
    standard. Given the user query, the agent's response, and the gold standard, grade the
    agent's response, taking into account the following criteria:

    1. Relevance: How well does the response address the user's query?
    2. Accuracy: How accurate is the response to the gold standard?
    3. Clarity: How clear is the response?
    4. Tone: How appropriate is the tone of the response?

    User Query: {instruction}
    Agent Response: {predicted_answer}
    Gold Standard: {expected_answer}

    Return only a single number between 0 and 10.
    """
    response = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return int(response.choices[0].message.content)


async def grade_results(
    openai_client: OpenAI, results_df: pd.DataFrame, agent_type: AgentType
) -> dict:
    """
    Grades the results of the agent on a scale of 0 to 10.
    """
    results_df["intent_correct"] = (
        results_df["predicted_intent"] == results_df["expected_intent"]
    )
    results_df["category_correct"] = (
        results_df["predicted_category"].str.lower()
        == results_df["expected_category"].str.lower()
    )
    intent_accuracy = results_df["intent_correct"].mean()
    category_accuracy = results_df["category_correct"].mean()

    grade_tasks = [
        grade_response(
            openai_client,
            row["instruction"],
            row["predicted_answer"],
            row["expected_answer"],
        )
        for _, row in results_df.iterrows()
    ]
    grades = await asyncio.gather(*grade_tasks)
    mean_grade = sum(grades) / len(grades)

    return {
        "agent_type": agent_type,
        "intent_accuracy": intent_accuracy,
        "category_accuracy": category_accuracy,
        "mean_response_grade": mean_grade,
    }


async def main():
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    num_examples_to_eval = 25
    df_rows = DF.sample(n=num_examples_to_eval, random_state=RANDOM_STATE)
    single_results = await run_agent_on_instructions(AgentType.SINGLE, df_rows)
    multi_results = await run_agent_on_instructions(AgentType.MULTI, df_rows)
    single_grade = await grade_results(openai_client, single_results, AgentType.SINGLE)
    multi_grade = await grade_results(openai_client, multi_results, AgentType.MULTI)

    result_df = pd.DataFrame([single_grade, multi_grade])
    print(result_df)


if __name__ == "__main__":
    asyncio.run(main())
