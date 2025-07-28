
# Customer Service Agents Workshop

This is the Customer Service workshop! By the end of this sessions you will have:

1. Explored and understood a real customer-support dataset.
2. Learned the basics of the `openai-agents-python` SDK.
3. Implemented:
   - a **single-agent** chatbot that routes to tools based on the user’s intent, and
   - a **multi-agent** system that first triages the request and then delegates to specialized agents.
4. Built an **evaluation suite** that automatically measures both intent classification accuracy and answer quality.

## 0. Pre-requisites

Install the dependencies:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Make sure you have an OpenAI API key set in your environment.

## 1. Exploratory Data Analysis (EDA)

Goal: **internalize the data** – what instruction (user input), categories, and intents exist. Get a sense for how big the dataset is, and the distribution of categories and intents per category.

Deliverable: **basic EDA notebook** and a 2-3 sentence takeaway.

## 2. Familiarize yourself with the Agent SDK

The workshop uses the [openai-agents-python](https://github.com/openai/openai-agents-python) SDK.

1. Skim the **README** and the documentation.
2. Run the Agents SDK customer service example project once to get some intuition:

```bash
python starter_code/customer_service/main.py
```

## 3. Build a Single Agent routine system

We start with a single agent that does everything in one prompt.  You can reference a very simple
mocked up example, but we suggest starting from scratch and only using the starting code if needed  (see `starter_code/single_agent/`).

To run the example code:
```bash
python -m example_solution.single_agent.main
```

To run the starter code:
```bash
python -m starter_code.single_agent.main
```

Step-by-step guide:

1. Define one **tool per intent**. The model will call the tool as a classification.

2. Register the tools in `tool_registry.py`.

3. Write the system prompt in `config.py`.  Include:
   • a concise system message describing the available intents.
   • few shot examples to help the model disambiguate edge-cases.

4. The prompts are mostly placeholders for now. Tweak the prompts using the available
input and output data in the dataset to try to mimic the intended output behavior.

Success criteria:

• The agent runs, and can call different tools based on different intents.
• From ~vibes~, the agent responds when each intent classification tool is called
in a similar way as the ground truth in the dataset.

## 4. Build a Multi-Agent System

Motivation: as the number of intents grows, a single prompt becomes fragile.  We instead chain specialized agents.

Reference code: `starter_code/customer_service/` and `starter_code/multi_agent/`

4.1  Design

• **Triage agent** – classifies the user query and does a handoff to the relevant agent.
• **Domain agents** – Define one agent per category, you are doing hierarchical triage, where you
first determine the category, then the intent... You can use evals later to decide which is optimal.
Each domain agent should have a tool per intent, which acts as a classification step.

4.2  Implementation Steps

1. Create `tool_registry.py` & `agent_registry.py` for each category under `starter_code/multi_agent/`.
2. Update `main.py` so the user can chat with the full system.

3  Acceptance Tests

• End-to-end conversations work on ~vibes~, and the responses seem
similar to the random samples from the dataset.

## 5. Build a Multi-Agent System

Add a relevance guardrail, a jailbreak guardrail, and a non-LLM based guardrail of your choosing.

## 6. Build an Evaluation Suite

Now comes the important part! We need to make data driven decisions on what works and what doesn't.   Using promptfoo (or a similar framework of your choosing, create an eval set from the available data)

• [promptfoo](https://github.com/promptfoo/promptfoo)


5.1  Prepare a golden set. This is essentially the data available, with any cleaning
you have done in section 1.


5.2  Write an evaluation script that:

1. Feeds only `user_query` into the two systems you built in the previous sections (single and multi-agent systems)
2. Records:
   • predicted `category` / `intent` (from triage logs or tool names)
   • the final textual answer.
3. Computes metrics:
   • **Classification Accuracy** – exact match of (category, intent) vs ground truth.
   • **Answer Quality** – LLM-J assessment of quality match to original.

In a real world scenario, you would also measure metrics like latency and cost, but for the purposes of this workshop,
we will not be measuring those.

For the LLM-J assessment. Create a rubric to grade each output message. The adherence to the tone
and ground truth output is critical. Use `o3` to make the rubric, and run N=5 tests on each
row of the dataset to ensure that your outputs are consistent.

4. Finally, write 2-3 sentences to a customer on which system you would recommend they use
and why (multi-agent or single-agent!) Discuss tradeoffs, extensibility, and anything
you would do to future proof the system.
