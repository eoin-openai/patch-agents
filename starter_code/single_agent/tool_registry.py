import csv
from pathlib import Path

from agents import function_tool

# Load intents and categories from the Bitext sample CSV
CSV_PATH = Path(__file__).parent.parent / "data/Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv"

_intent_categories = {}
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        intent = row.get("intent")
        category = row.get("category")
        if intent and category and intent not in _intent_categories:
            _intent_categories[intent] = category

# Dynamically create a tool function for each intent
TOOLS = []

def _make_tool(intent, category):
    @function_tool(name_override=intent, description_override=f"Category: {category}")
    def tool(query: str) -> str:
        # Dummy implementation: echo the intent and query
        return f"Tool '{intent}' called with query: {query}"
    tool.__name__ = intent
    return tool

for intent in sorted(_intent_categories):
    category = _intent_categories[intent]
    t = _make_tool(intent, category)
    globals()[intent] = t
    TOOLS.append(t)
