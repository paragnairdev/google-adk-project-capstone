"""
Data Collection Agents

These agents are responsible for fetching and analyzing raw data:
- FactFinder: Retrieves head-to-head and venue data (Phase 1 of strategy workflow)
- StatAnalyst: Provides detailed statistical analysis (Direct routing from orchestrator)

Design Pattern: Structured Data Collection
FactFinder outputs JSON which is stored in an output_key for downstream processing.
This design:
1. Reduces token usage (concise JSON format)
2. Enables structured data flow between agents
3. Maintains data integrity (no interpretation at collection phase)
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from ..tools import (
    get_head_to_head, 
    get_venue_trends, 
    get_player_stats
)
from ..config import retry_config
from ..constants import FACT_FINDER_AGENT, STAT_ANALYST_AGENT, FACT_FINDER_OUTPUT

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)


# ============================================================================
# FACT FINDER AGENT
# ============================================================================
# Purpose: Gather contextual data for strategy formulation (Phase 1)
#
# Behavior: Structured JSON Output
# - Calls tools based on conversation context
# - Outputs JSON data stored in an output_key
# - JSON output flows to next agent (Tactician) for analysis
#
# Why JSON Output?
# Traditional approach: FactFinder → summarize data → Tactician → analyze summary
# This approach: FactFinder → JSON data → Tactician → analyze data
# Benefits: Structured format, efficient data flow, no information loss
#
# Tools Used:
# - get_head_to_head: Historical matchup data
# - get_venue_trends: Pitch/venue statistics
fact_finder_agent = LlmAgent(
    name=FACT_FINDER_AGENT,
    description="Retrieves head-to-head and venue data and outputs JSON to output_key",
    model=model_config,
    instruction="""
    You are phase 1 of a 3-phase sequential workflow.
    
    When you are called, ALL required info is ALREADY in the conversation: opponent, format, pitch type.
    
    YOUR JOB:
    1. Extract data (player name, opponent, format, and pitch type) from conversation history
    2. Call `get_head_to_head` with player_name, opponent_name, and format
    3. Call `get_venue_trends` with pitch_type and format
    4. Output *only* json
    """,
    tools=[get_head_to_head, get_venue_trends],
    output_key=FACT_FINDER_OUTPUT,
)


# ============================================================================
# STAT ANALYST AGENT
# ============================================================================
# Purpose: Handle direct statistical queries (bypassing strategy workflow)
#
# Routing: Orchestrator → StatAnalyst (direct)
# Not part of sequential workflow - handles queries like:
# - "What's my T20 average?"
# - "Show me head-to-head vs Ragz"
# - "What's the average score on green pitches?"
#
# Design Decision: Separate from FactFinder because:
# 1. Different presentation: User-facing vs. agent-facing
# 2. Different behavior: Formats output nicely vs. silent execution
# 3. Different use case: Direct queries vs. strategy input
#
# Behavior: Data Reporting (not interpretation)
# - Calls tools based on user query
# - Presents results in readable format
# - NO strategic advice (stays in lane as "analyst")
stat_analyst_agent = LlmAgent(
    name=STAT_ANALYST_AGENT,
    description="Provides detailed statistical analysis",
    model=model_config,
    instruction="""
    You are the Team Data Analyst.
    Your job is to query the database and report raw numbers accurately.
    
    TOOLS & RULES:
    1. Use `get_venue_trends` for stadium or pitch info.
    2. **IMPORTANT:** The tool `get_venue_trends` requires a 'format'.
    3. Use `get_head_to_head` for head-to-head records.
    4. **IMPORTANT:** The tool `get_head_to_head` requires a 'player_name', 'opponent_name' & 'format'.
       - Pass `stadium=7` (as an integer) to the tool.
    5. Use `get_player_stats` for player stats.
    6. **IMPORTANT:** The tool `get_player_stats` requires a 'player_name' & 'format'.

    OUTPUT FORMAT:
    - Present data in a clean bulleted list or small table.
    - Do NOT give advice (that is the Coach's job). Just give the numbers.
    """,
    tools=[get_venue_trends, get_head_to_head, get_player_stats] 
)

