"""
Strategy Agent

The Tactician analyzes data and formulates strategic recommendations.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from ..config import retry_config

# Common Model Config
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)


tactician = LlmAgent(
    name="Tactician",
    model=model_config,
    instruction="""
    You are a senior cricket analyst.
    Review the data provided by the FactFinder in the context.
    
    DECISION LOGIC:
    - If user loses chasing > 60% of the time -> Recommend Batting First.
    - If pitch is 'Green' or 'Overcast' -> Recommend Bowling First (unless weak at chasing).
    - If opponent is 'Wizheart' (strong player) -> Recommend conservative target setting.
    
    Output a structured strategic plan. Be logical and cold.
    """
)

