"""
Configuration for the Bootcamp Support Agent.
"""
from agents import ModelSettings

# Model to use for the agent
MODEL = "gpt-4.1"

# Enforce tool use for intent-based routing
MODEL_SETTINGS = ModelSettings()
