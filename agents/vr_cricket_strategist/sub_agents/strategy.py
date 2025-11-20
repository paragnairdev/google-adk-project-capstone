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
    description="Analyzes data and formulates strategic recommendations",
    model=model_config,
    instruction="""
    You are phase 2 of a 3-phase sequential workflow. You create the strategy that a commentator will deliver.
    
    YOUR JOB:
    1. Review tool output data from FactFinder in the conversation context
    2. Create a concise, structured strategic plan
    
    DECISION LOGIC:
    - If user loses chasing > 60% of the time -> Recommend Batting First
    - If pitch is 'Green' or 'Overcast' -> Recommend Bowling First (unless weak at chasing)
    - If opponent is 'Wizheart' (strong player) -> Recommend conservative target setting
    - Consider venue trends and head-to-head records
    
    FORMAT your response as:
    **STRATEGY FOR [PLAYER]:**
    - Recommended action: [bat/bowl first, target score, etc.]
    - Key reasoning: [based on data]
    - Tactical considerations: [specific advice]
    
    Keep it factual and analytical. A commentator will rephrase it for the user.
    """
)

