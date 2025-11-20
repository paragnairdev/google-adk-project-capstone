"""
Orchestrator Agents

These agents coordinate and manage the workflow between different agents:
- CommentatorRouter: Selects which commentator personality should deliver the advice
- GamePlanGenerator: Sequential workflow for generating complete match strategies
- FallbackAgent: Handles requests that don't fit other categories
"""

from google.adk.agents import LlmAgent, SequentialAgent, Agent
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
    description="Selects which commentator personality should deliver the advice",
    model=model_config,
    instruction="""
    You are phase 3 (final) of a 3-phase sequential workflow. You MUST produce the final response.
    
    The Tactician's strategy is in the conversation context above.
    
    YOUR JOB:
    1. Check if user requested a specific commentator (Boycott, Sidhu, Nasser, or Harsha)
    2. If yes, transfer to that commentator agent
    3. If no preference, call `pick_random_commentator` tool to choose one
    4. Transfer to the selected commentator agent
    
    The commentator will deliver the Tactician's strategy in their unique style.
    
    CRITICAL: You MUST transfer to a commentator. Do not skip this step.
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
    description="Handles requests that don't fit other categories",
    model=model_config,
    instruction="""
    You are the fallback handler for the VR Cricket Strategist.
    
    YOUR JOB:
    1. Explain that you are a specialized AI for the VR Cricket Game, not real-world cricket.
    2. If the user is asking for strategy but hasn't provided details, explain that you need:
       - Pitch Type (Dry, Bouncy, Green, Normal)
       - Opponent Name
       - Match Format
    3. Politely guide them back to the game strategy context.
    4. Do NOT search the web. Focus only on the VR game mechanics.
    """
)

