from pathlib import Path

import pandas as pd
from example_solution.single_agent.constants import NUM_EXAMPLES, RANDOM_STATE

CSV_PATH = (
    Path(__file__).parent.parent.parent
    / "data/Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"
)

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_data() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH)


DF = load_data()


def load_markdown_prompt(file_name: str, **substitutions) -> str:
    """
    Loads a markdown prompt and injects any substitutions.
    """
    file_content = (PROMPTS_DIR / file_name).read_text()

    if substitutions:
        file_content = file_content.format(**substitutions)

    return file_content


def get_example_queries(intent: str | None = None) -> str:
    """
    Returns a formatted string of example queries and their expected responses and intents.
    """
    if intent:
        example_queries = DF[DF["intent"] == intent][
            ["instruction", "response", "intent"]
        ].sample(NUM_EXAMPLES, random_state=RANDOM_STATE)
    else:
        example_queries = DF[["instruction", "response", "intent"]].sample(
            NUM_EXAMPLES, random_state=RANDOM_STATE
        )

    example_queries = [
        f"""
        Question: {row["instruction"]}
        Answer: {row["response"]}
        Intent: {row["intent"]}
        """
        for _, row in example_queries.iterrows()
    ]
    return "\n## Example: \n".join(example_queries)
