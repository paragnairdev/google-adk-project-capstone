"""
Orchestrator Agents

These agents coordinate and manage the workflow between different agents:
- CommentatorRouter: Selects which commentator personality should deliver the advice
- GamePlanGenerator: Sequential workflow for generating complete match strategies
- FallbackAgent: Handles requests that don't fit other categories
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini

from ..tools import pick_random_commentator
from ..config import retry_config
from .data_collectors import fact_finder
from .strategy import tactician
from .commentators import boycott_writer, sidhu_writer, nasser_writer, harsha_writer

# Common Model Config
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)


commentator_router = LlmAgent(
    name="CommentatorSelector",
    model=model_config,
    instruction="""
    You are the Producer of the cricket show.
    1. You have a strategy from the 'Tactician' in your context.
    2. Call `pick_random_commentator` to decide who should speak.
    3. Delegate the task to that specific agent (e.g., if tool returns 'Sidhu', call SidhuWriter).
    4. Do NOT write the strategy yourself. Let the sub-agent do it.
    """,
    tools=[pick_random_commentator],
    sub_agents=[boycott_writer, sidhu_writer, nasser_writer, harsha_writer]
)


game_plan_generator = SequentialAgent(
    name="GamePlanGenerator",
    description="Generates a detailed match strategy using data analysis.",
    sub_agents=[fact_finder, tactician, commentator_router]
)


fallback_agent = LlmAgent(
    name="GenericResponder",
    model=model_config,
    instruction="""
    You are the fallback handler. 
    If the user's request does not fit Strategy or Stats, or if other agents failed:
    1. Tell the user you can only help with Cricket Strategy and Match Statistics.
    2. Ask them to rephrase.
    """
)

