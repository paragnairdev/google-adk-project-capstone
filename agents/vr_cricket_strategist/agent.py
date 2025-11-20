"""
VR Cricket Strategist - Root Agent

This module contains the main root agent that orchestrates all sub-agents
to provide cricket strategy and analysis.
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini

# Import tools, sub-agents, and callbacks
from .tools import get_current_identity
from .config import retry_config
from .callbacks import circuit_breaker
from .sub_agents import (
    # Orchestrators
    game_plan_generator,
    fallback_agent,
    commentator_router,
    # Data collectors
    fact_finder,
    stat_analyst,
    # Strategy
    tactician,
    # Commentators
    boycott_writer,
    sidhu_writer,
    nasser_writer,
    harsha_writer,
)

# Model configuration
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)

# Re-export for backward compatibility with tests
__all__ = [
    'root_agent',
    'model_config',
    'LlmAgent',
    'SequentialAgent',
    'Gemini',
    'game_plan_generator',
    'stat_analyst',
    'fallback_agent',
    'fact_finder',
    'tactician',
    'boycott_writer',
    'sidhu_writer',
    'nasser_writer',
    'harsha_writer',
    'commentator_router',
    'identity_agent',
    'orchestrator_agent',
]

identity_agent = LlmAgent(
    name="IdentityAgent",
    model=model_config,
    instruction="Call the `get_current_identity` tool immediately and output the result.",
    tools=[get_current_identity]
)

orchestrator_agent = LlmAgent(
    name="CricketCoachOrchestrator",
    model=model_config,
    instruction="""
    You are the VR Cricket Coach/Strategist Interface.
    
    The user's identity has already been established in the conversation history.
    
    ### ROUTING INSTRUCTIONS
    Classify the user's intent and route to the correct specialist:

    **FOR STRATEGY REQUESTS ("What should I do?", "Help me improve", "Give me advice"):**
    
    BEFORE transferring to `GamePlanGenerator`, check if you have ALL required information:
    - Match format (T20, ODI, or Test)
    - Opponent name
    - Pitch type (Dry, Bouncy, Green, or Normal)
    
    IF MISSING ANY INFO:
    - Ask the user for the missing information clearly
    - List ALL missing items in one message
    - WAIT for their response (do NOT transfer to GamePlanGenerator yet)

    IF USER RESPONDS WITH THE MISSING INFORMATION:
    - Transfer to `GenericResponder` to handle the request.
    - Look for responses like "no pitch type", "no opponent"
    
    IF YOU HAVE ALL INFO:
    - Transfer to `GamePlanGenerator` (which will gather data, create strategy, and deliver via commentator)
    
    **FOR STATS REQUESTS ("Show me data", "Stadium info", "Head to head"):**
    - Transfer to `StatAnalyst`
    
    **FOR CHIT-CHAT:**
    - Handle greetings and casual conversation yourself
    
    **LOOP PREVENTION:**
    - If an agent transfers back without an answer, apologize and say "I don't have that information"
    """,
    tools=[get_current_identity],
    sub_agents=[game_plan_generator, stat_analyst, fallback_agent] 
)

# ============================================================================
# ROOT AGENT - Main Orchestrator
# ============================================================================

root_agent = SequentialAgent(
    name="RootAgent",
    sub_agents=[identity_agent, orchestrator_agent]
)

# Attach circuit breaker callbacks to prevent infinite loops
root_agent.before_agent_callback = circuit_breaker
identity_agent.before_agent_callback = circuit_breaker
orchestrator_agent.before_agent_callback = circuit_breaker
stat_analyst.before_agent_callback = circuit_breaker
game_plan_generator.before_agent_callback = circuit_breaker