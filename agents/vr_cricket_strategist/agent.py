"""
VR Cricket Strategist - Root Agent

This module implements the main orchestration layer for the multi-agent system.

Architecture Overview:
┌────────────────────────────────────────────────────────────────────────┐
│ root_agent (Sequential)                                                │
│  ├─> identity_agent: Loads user session state                          │
│  └─> cricket_coach_orchestrator_agent: Routes to specialized agents    │
│       ├─> game_plan_generator_agent (Sequential)                       │
│       │    ├─> fact_finder_agent: Data collection                      │
│       │    ├─> tactician_agent: Strategy formulation                   │
│       │    └─> commentator_selector_agent: Personality selection       │
│       │         ├─> boycott_writer_agent                               │
│       │         ├─> sidhu_writer_agent                                 │
│       │         ├─> nasser_writer_agent                                │
│       │         └─> harsha_writer_agent                                │
│       ├─> stat_analyst_agent: Direct statistical queries               │
│       └─> generic_responder_agent: Fallback handler                    │
└────────────────────────────────────────────────────────────────────────┘

Design Pattern: Sequential Agent at Root Level
- Ensures identity is ALWAYS loaded before routing
- Prevents routing decisions without user context
- Simplifies error handling (identity failures caught early)

Circuit Breaker Integration:
All agents have circuit_breaker callbacks attached to prevent infinite loops.
See callbacks.py for implementation details.
"""

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini

# Import tools, sub-agents, callbacks, and constants
from .tools import get_current_identity, set_current_identity
from .config import retry_config
from .callbacks import circuit_breaker
from .constants import (
    IDENTITY_AGENT,
    CRICKET_COACH_ORCHESTRATOR_AGENT,
    ROOT_AGENT,
    GAME_PLAN_GENERATOR_AGENT,
    GENERIC_RESPONDER_AGENT,
)
from .sub_agents import (
    # Orchestrators
    game_plan_generator_agent,
    generic_responder_agent,
    commentator_router_agent,
    # Data collectors
    fact_finder_agent,
    stat_analyst_agent,
    # Strategy
    tactician_agent,
    # Commentators
    boycott_writer_agent,
    sidhu_writer_agent,
    nasser_writer_agent,
    harsha_writer_agent,
)

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
# Shared model configuration for all agents
# Uses Gemini 2.5 Flash for balance of speed, quality, and cost
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)

# ============================================================================
# MODULE EXPORTS
# ============================================================================
# Re-export for consistency
__all__ = [
    'root_agent',
    'model_config',
    'LlmAgent',
    'SequentialAgent',
    'Gemini',
    'game_plan_generator_agent',
    'stat_analyst_agent',
    'generic_responder_agent',
    'fact_finder_agent',
    'tactician_agent',
    'boycott_writer_agent',
    'sidhu_writer_agent',
    'nasser_writer_agent',
    'harsha_writer_agent',
    'commentator_router_agent',
    'identity_agent',
    'orchestrator_agent',
]

# ============================================================================
# PHASE 1: IDENTITY AGENT
# ============================================================================
# Purpose: Load user identity from session state before any routing decisions
# 
# Design Decision: Separated identity loading into dedicated agent to:
# 1. Ensure identity is ALWAYS loaded (can't be skipped)
# 2. Make routing logic cleaner (orchestrator assumes identity exists)
# 3. Enable testing with mock identities easily
#
# Behavior: Silent execution - just loads identity and passes to next agent
identity_agent = LlmAgent(
    name=IDENTITY_AGENT,
    model=model_config,
    instruction="""
    You are the Identity Manager. Your goal is to ensure the next agent has the correct user data.
    
    **Logic Flow:**
    1. Analyze the user's latest input.
    2. **CHECK FOR UPDATES:** If the user is explicitly stating their name, correcting you, or introducing themselves (e.g., "I am Ragz", "Call me Steve", "My name isn't Joe"), you MUST call `set_current_identity` with the new player_name. The team and batting_style parameters are optional - only provide them if the user explicitly mentions them.
    3. **DEFAULT:** If the user is NOT changing their identity, call `get_current_identity`.
    
    **Output Requirement:**
    - Regardless of which tool you called, output the final identity JSON object.
    - Do not add conversational filler.
    """,
    tools=[get_current_identity, set_current_identity]
)

# ============================================================================
# PHASE 2: ORCHESTRATOR AGENT
# ============================================================================
# Purpose: Main routing hub that classifies queries and delegates to specialists
#
# Routing Strategy:
# - Strategy Requests → GamePlanGenerator (multi-stage workflow)
# - Statistical Queries → StatAnalyst (direct data access)
# - General/Invalid → generic_responder_agent (fallback)
#
# Design Decision: Use LLM-based routing (not rule-based) to handle:
# 1. Natural language ambiguity ("Should I bat first?" → Strategy)
# 2. Missing context detection ("Need pitch type to give advice")
# 3. Conversational flow (greetings, follow-ups)
#
# Information Requirements:
# Strategy queries require: format, opponent, pitch_type
# Statistical queries require: format only (may also need player/opponent)
#
# Loop Prevention:
# - Circuit breaker callback prevents infinite routing
# - Explicit instructions to stop if agents return without answers
orchestrator_agent = LlmAgent(
    name=CRICKET_COACH_ORCHESTRATOR_AGENT,
    model=model_config,
    instruction=f"""
    You are the VR Cricket Coach/Strategist Interface.
    
    **CONTEXT CONSUMPTION:**
    Look at the message immediately preceding this one. It contains the User's Identity and Preferences provided by the system.
    
    **ACTION:**
    Using that identity information, greet the user by name and proceed with the routing logic.

    ### ROUTING INSTRUCTIONS
    Classify the user's intent and route to the correct specialist:

    **FOR STRATEGY REQUESTS ("What should I do?", "Help me improve", "Give me advice"):**
    
    BEFORE transferring to `{GAME_PLAN_GENERATOR_AGENT}`, check if you have ALL required information:
    - Match format (T20, ODI, or Test)
    - Opponent name
    - Pitch type (Dry, Bouncy, Green, or Normal) is optional. If not provided, use None.
    
    IF MISSING ANY INFO (except pitch type):
    - Ask the user for the missing information clearly
    - List ALL missing items in one message
    - WAIT for their response (do NOT transfer to {GAME_PLAN_GENERATOR_AGENT} yet)

    IF USER RESPONDS WITH THE MISSING INFORMATION:
    - Transfer to `{GENERIC_RESPONDER_AGENT}` to handle the request.
    - Look for responses like "no pitch type", "no opponent"
    
    IF YOU HAVE ALL INFO:
    - Transfer to `{GAME_PLAN_GENERATOR_AGENT}` (which will gather data, create strategy, and deliver via commentator)
    
    **FOR STATS REQUESTS ("Show me data", "Stadium info", "Head to head"):**
    - Transfer to `stat_analyst_agent`
    
    **FOR CHIT-CHAT:**
    - Handle greetings and casual conversation yourself
    
    **LOOP PREVENTION:**
    - If an agent transfers back without an answer, apologize and say "I don't have that information"
    """,
    tools=[get_current_identity],
    sub_agents=[game_plan_generator_agent, stat_analyst_agent, generic_responder_agent] 
)

# ============================================================================
# ROOT AGENT - Main Entry Point
# ============================================================================
# Sequential workflow: Identity loading → Orchestration
#
# Design Pattern: Sequential Agent (not Parallel)
# Why? Identity MUST be loaded before orchestration. Sequential execution
# ensures this dependency is satisfied.
#
# Workflow:
# 1. identity_agent loads user context from session
# 2. Orchestrator receives identity in conversation history
# 3. Orchestrator uses identity for personalized routing
#
# Alternative Considered: Single agent with identity tool
# Rejected because: Identity loading would be optional, leading to
# inconsistent behavior when LLM forgets to call the tool
root_agent = SequentialAgent(
    name=ROOT_AGENT,
    sub_agents=[identity_agent, orchestrator_agent]
)

# ============================================================================
# CIRCUIT BREAKER ATTACHMENT
# ============================================================================
# Attach circuit breaker callbacks to critical agents to prevent loops
#
# Why These Agents?
# - root_agent: Catches loops at top level
# - identity_agent: Prevents repeated identity loading
# - orchestrator_agent: Prevents ping-pong routing (most common failure)
# - stat_analyst: Prevents tool call loops
# - game_plan_generator: Prevents sequential workflow loops
#
# Design Decision: We attach to specific agents rather than all agents
# to minimize callback overhead on leaf agents (commentators) that can't
# create loops (they have no sub-agents to transfer to)
root_agent.before_agent_callback = circuit_breaker
identity_agent.before_agent_callback = circuit_breaker
orchestrator_agent.before_agent_callback = circuit_breaker
stat_analyst_agent.before_agent_callback = circuit_breaker
game_plan_generator_agent.before_agent_callback = circuit_breaker