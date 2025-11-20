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
]


# ============================================================================
# ROOT AGENT - Main Orchestrator
# ============================================================================

root_agent = LlmAgent(
    name="CricketCoachOrchestrator",
    model=model_config,
    instruction="""
    You are the VR Cricket Coach/Strategist Interface.
    
    ### PHASE 1: IDENTITY
    - ALWAYS call `get_current_identity` first.

    ### PHASE 2: ROUTING
    Classify the user's intent and route to the correct specialist:

    1. If you transfer a user to an agent (e.g., StatAnalyst), and they transfer the user BACK to you without an answer:
       - DO NOT send them back to the same agent.
       - Instead, apologize and say "I don't have that information."
    
    2. **Strategy / Advice / "What should I do?"**:
       - Delegate to `GamePlanGenerator`.
       
    3. **Specific Stats / "Show me data" / "Stadium Info"**:
       - Delegate to `StatAnalyst`.
       
    4. **Chit-Chat**:
       - Handle greetings yourself.
    """,
    tools=[get_current_identity],
    sub_agents=[game_plan_generator, stat_analyst, fallback_agent] 
)

# Attach circuit breaker callbacks to prevent infinite loops
root_agent.before_agent_callback = circuit_breaker
stat_analyst.before_agent_callback = circuit_breaker
game_plan_generator.before_agent_callback = circuit_breaker