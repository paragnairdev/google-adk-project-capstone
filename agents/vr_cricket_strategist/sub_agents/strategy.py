"""
Strategy Agent

The Tactician analyzes data and formulates strategic recommendations.

Design Pattern: Middle agent in 3-phase sequential workflow
- Phase 1: FactFinder collects data
- Phase 2: Tactician (this agent) analyzes and strategizes
- Phase 3: CommentatorRouter delivers with personality

Separation of Concerns:
By isolating strategy formulation from data collection and delivery,
we achieve:
1. Testability: Can test strategy logic independently
2. Consistency: Same strategy logic regardless of commentator
3. Maintainability: Update decision logic without touching other phases
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from ..config import retry_config
from ..constants import TACTICIAN_AGENT, FACT_FINDER_OUTPUT

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)


# ============================================================================
# TACTICIAN AGENT
# ============================================================================
# Purpose: Convert raw data into actionable strategic recommendations
#
# Input: Tool output from FactFinder (venue trends, head-to-head stats)
# Output: Structured strategy document (factual, no personality)
# 
# Decision Algorithm:
# The agent uses heuristics based on cricket strategy principles:
# - Green pitches favor bowling first (movement for pace bowlers)
# - Strong chasing record → recommend bowling first
# - Weak opponent → aggressive targets
# - Strong opponent (e.g., Joe) → conservative approach
#
# Design Decision: Instructions encode domain knowledge rather than
# using ML models. For a prototype, this provides:
# 1. Transparency: Strategy logic is auditable
# 2. Predictability: Same inputs → same outputs
# 3. Debuggability: Easy to understand why a recommendation was made
#
# Future Enhancement: Could integrate ML models for win probability
tactician_agent = LlmAgent(
    name=TACTICIAN_AGENT,
    description="Analyzes data and formulates strategic recommendations",
    model=model_config,
    instruction=f"""
    You are phase 2 of a 3-phase sequential workflow. You create the strategy that a commentator will deliver.
    
    YOUR JOB:
    1. Review the {{fact_finder_output}} from the conversation context
    2. Create a concise, structured strategic plan
    
    DECISION LOGIC:
    - If user loses chasing > 60% of the time -> Recommend Batting First
    - If pitch is 'Green' or 'Overcast' -> Recommend Bowling First (unless weak at chasing)
    - If opponent is 'Joe' (strong player) -> Recommend conservative target setting
    - Consider venue trends and head-to-head records
    
    FORMAT your response as:
    **STRATEGY FOR [PLAYER]:**
    - Recommended action: [bat/bowl first, target score, etc.]
    - Key reasoning: [based on data]
    - Tactical considerations: [specific advice]
    
    Keep it factual and analytical. A commentator will rephrase it for the user.
    """
)

