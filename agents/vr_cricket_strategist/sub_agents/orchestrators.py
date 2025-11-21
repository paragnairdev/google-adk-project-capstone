"""
Orchestrator Agents

These agents coordinate and manage the workflow between different agents:
- CommentatorRouter: Selects which commentator personality should deliver the advice
- GamePlanGenerator: Sequential workflow for generating complete match strategies
- FallbackAgent: Handles requests that don't fit other categories

Design Pattern: Hierarchical Orchestration
- Top level: CricketCoachOrchestrator (in agent.py) routes by intent
- Mid level: GamePlanGenerator orchestrates strategy workflow
- Low level: CommentatorRouter selects personality for delivery

This layered approach provides:
1. Clear separation of concerns (routing vs. workflow vs. presentation)
2. Independent testability of each orchestration layer
3. Flexibility to modify workflows without affecting routing logic
"""

from google.adk.agents import LlmAgent, SequentialAgent, Agent
from google.adk.models.google_llm import Gemini

from ..tools import pick_random_commentator
from ..config import retry_config
from .data_collectors import fact_finder
from .strategy import tactician
from .commentators import boycott_writer, sidhu_writer, nasser_writer, harsha_writer

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)


# ============================================================================
# COMMENTATOR ROUTER (Phase 3 of Strategy Workflow)
# ============================================================================
# Purpose: Select personality for strategy delivery
#
# Behavior:
# 1. Check if user requested specific commentator
# 2. If not, randomly select one using pick_random_commentator tool
# 3. Transfer to selected commentator agent
#
# Design Decision: Separate routing from delivery to:
# - Enable user preference ("I want Boycott's opinion")
# - Maintain variety (random selection keeps it fresh)
# - Isolate personality logic (commentator agents focus on style)
#
# Why Use a Tool for Random Selection?
# Alternative: Pure Python random.choice()
# Chosen approach: Tool-based selection
# Reason: Maintains consistency with ADK patterns and enables:
# - Observability (tool calls are logged)
# - Testing (can mock tool to test specific commentators)
# - Future enhancement (ML-based personality matching)
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


# ============================================================================
# GAME PLAN GENERATOR (3-Phase Sequential Workflow)
# ============================================================================
# Purpose: End-to-end strategy generation pipeline
#
# Workflow:
# Phase 1: FactFinder → Collect data (silent)
# Phase 2: Tactician → Formulate strategy
# Phase 3: CommentatorRouter → Select personality → Deliver with flair
#
# Design Decision: Sequential Agent Pattern
# Why not Parallel? Data collection must complete before analysis
# Why not Single Agent? Separation enables:
# - Testing each phase independently
# - Parallel development of phases by different team members
# - Reusability (FactFinder could be used by other workflows)
# - Clear failure points (know which phase failed)
#
# Sequential guarantees: Each phase completes before next begins
# This ensures: No strategy without data, no delivery without strategy
game_plan_generator = SequentialAgent(
    name="GamePlanGenerator",
    description="Generates a detailed match strategy using data analysis.",
    sub_agents=[fact_finder, tactician, commentator_router]
)

# ============================================================================
# FALLBACK AGENT
# ============================================================================
# Purpose: Handle queries that don't fit strategy or statistics
#
# Routed by: CricketCoachOrchestrator when intent is unclear
#
# Use Cases:
# - Incomplete queries ("Should I bat first?" without format/opponent)
# - Out-of-scope questions ("Tell me about IPL 2024")
# - Clarification requests after failed routing
#
# Design Decision: Graceful Degradation
# Rather than error messages, this agent:
# 1. Acknowledges the limitation
# 2. Explains what's needed for a proper answer
# 3. Guides user back to valid query types
#
# Behavior: Educational and Redirective (not dismissive)
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

