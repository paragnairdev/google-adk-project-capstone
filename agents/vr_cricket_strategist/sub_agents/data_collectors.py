"""
Data Collection Agents

These agents are responsible for fetching and analyzing raw data:
- FactFinder: Retrieves head-to-head and venue data
- StatAnalyst: Provides detailed statistical analysis
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from ..tools import (
    get_head_to_head, 
    get_venue_trends, 
    get_player_stats
)
from ..config import retry_config

# Common Model Config
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)


fact_finder = LlmAgent(
    name="FactFinder",
    model=model_config,
    instruction="""
    You are a data retrieval specialist.
    1. Identify the pitch type, opponent, and format from the conversation history.
    2. Call `get_head_to_head` to see the record against this opponent.
    3. Call `get_venue_trends` to see pitch behavior.
    4. Output ONLY the raw data summaries. Do not give advice.
    """,
    tools=[get_head_to_head, get_venue_trends]
)


stat_analyst = LlmAgent(
    name="StatAnalyst",
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

