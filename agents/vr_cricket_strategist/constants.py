"""
Agent Name Constants

This module centralizes all agent names used throughout the VR Cricket Strategist system.
Using constants ensures consistency and makes it easy to reference agent names in instructions.

Naming Convention: snake_case with _agent suffix (as per ADK documentation)
Examples: root_agent, identity_agent, fact_finder_agent
"""

# ============================================================================
# ROOT LEVEL AGENTS
# ============================================================================
ROOT_AGENT = "root_agent"
IDENTITY_AGENT = "identity_agent"
CRICKET_COACH_ORCHESTRATOR_AGENT = "cricket_coach_orchestrator_agent"

# ============================================================================
# ORCHESTRATOR AGENTS
# ============================================================================
GAME_PLAN_GENERATOR_AGENT = "game_plan_generator_agent"
COMMENTATOR_SELECTOR_AGENT = "commentator_selector_agent"
GENERIC_RESPONDER_AGENT = "generic_responder_agent"

# ============================================================================
# DATA COLLECTION AGENTS
# ============================================================================
FACT_FINDER_AGENT = "fact_finder_agent"
STAT_ANALYST_AGENT = "stat_analyst_agent"

# ============================================================================
# STRATEGY AGENTS
# ============================================================================
TACTICIAN_AGENT = "tactician_agent"

# ============================================================================
# COMMENTATOR AGENTS
# ============================================================================
BOYCOTT_WRITER_AGENT = "boycott_writer_agent"
SIDHU_WRITER_AGENT = "sidhu_writer_agent"
NASSER_WRITER_AGENT = "nasser_writer_agent"
HARSHA_WRITER_AGENT = "harsha_writer_agent"

# ============================================================================
# UTILITY AGENTS
# ============================================================================
SEARCH_AGENT = "search_agent"

