# tools/identity_tools.py
import os
from google.adk.tools import ToolContext

# Helper to define test data
TEST_PROFILE = {
    "player_name": "Wizheart",
    "team": "England",
    "batting_style": "Moderate",
    "role": "Player"
}

def get_current_identity(tool_context: ToolContext):
    """
    Retrieves the current player's identity.
    FOR TESTING: If no player is found, automatically logs in as 'Wizheart'.
    """
    session = tool_context.session
    state = session.state
    
    # 1. Check if we already know who the player is
    player_name = state.get("player_name")
    
    if player_name:
        return f"User is logged in as {player_name} ({state.get('team')})."

    # 2. If missing, inject TEST_PROFILE (The "Dev Mode" Hack)
    # We assume if you are using this tool and state is empty, you are testing.
    print("⚠️ [DEV MODE] No identity found. Auto-injecting test profile.")
    
    for key, value in TEST_PROFILE.items():
        state[key] = value
        
    return f"DEBUG: Auto-logged in as test user '{TEST_PROFILE['player_name']}'."

# Assume 'df' is your loaded dataframe or database connection
def get_venue_trends(pitch_type: str, format: str):
    """
    Fetches average scores and win rates for a specific pitch and format.
    """
    # ... logic to filter your past 2 years of data ...
    # Example Return:
    return {
        "avg_first_innings_score": 185,
        "win_rate_batting_first": 0.45,
        "win_rate_batting_second": 0.55,
        "common_dismissal": "caught_behind"
    }

def get_head_to_head(player_id: str, opponent_id: str):
    """
    Returns win/loss record and stats against a specific opponent.
    """
    # ... logic to query database ...
    return {
        "matches_played": 10,
        "wins": 4,
        "losses": 6,
        "avg_runs_scored": 150
    }