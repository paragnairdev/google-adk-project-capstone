# tools/identity_tools.py
import os
import random
from typing import Optional
from google.adk.tools import ToolContext
from .data_loader import matches_df

# Helper to define test data
TEST_PROFILE = {
    "player_name": "Wizheart",
    "team": "England",
    "batting_style": "Moderate",
    "role": "Player"
}


def pick_random_commentator() -> str:
    """Randomly selects one cricket commentator name."""
    options = ["Boycott", "Sidhu", "Nasser", "Harsha"]
    return random.choice(options)

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
def get_venue_trends(format: str, pitch_type: Optional[str] = None, stadium: int = 0):
    """
    Fetches average scores and win rates for a specific pitch and format.
    
    Args:
        pitch_type: Type of pitch (e.g., 'Dry', 'Bouncy', 'Green', 'Normal')
        format: Match format (e.g., 'T20', 'ODI', 'Test')
        stadium: Stadium ID to filter by (default=0 means all stadiums)
    """
    # Filter matches by format first
    filtered = matches_df[matches_df['format'] == format]
    
    # Then filter by pitch_type if provided
    if pitch_type:
        filtered = filtered[matches_df['pitch_type'] == pitch_type]
    
    # If stadium is specified (not 0) and stadium column exists, filter by stadium
    if stadium != 0 and 'stadium' in matches_df.columns:
        filtered = filtered[filtered['stadium'] == stadium]
    
    if len(filtered) == 0:
        return {
            "error": f"No data found for pitch_type='{pitch_type}' and format='{format}'",
            "avg_first_innings_score": 0,
            "win_rate_batting_first": 0.0,
            "win_rate_batting_second": 0.0
        }
    
    # Calculate average first innings score
    first_innings = filtered[filtered['innings_number'] == 1]
    avg_first_innings_score = round(first_innings['runs'].mean(), 2) if len(first_innings) > 0 else 0
    
    # Calculate win rate batting first (innings_number == 1 and result == 'Win')
    wins_batting_first = len(first_innings[first_innings['result'] == 'Win'])
    total_batting_first = len(first_innings)
    win_rate_batting_first = round(wins_batting_first / total_batting_first, 2) if total_batting_first > 0 else 0.0
    
    # Calculate win rate batting second (innings_number == 2 and result == 'Win')
    second_innings = filtered[filtered['innings_number'] == 2]
    wins_batting_second = len(second_innings[second_innings['result'] == 'Win'])
    total_batting_second = len(second_innings)
    win_rate_batting_second = round(wins_batting_second / total_batting_second, 2) if total_batting_second > 0 else 0.0
    
    return {
        "avg_first_innings_score": avg_first_innings_score,
        "win_rate_batting_first": win_rate_batting_first,
        "win_rate_batting_second": win_rate_batting_second,
        "total_matches": len(filtered) // 2  # Each match has 2 innings
    }

def get_head_to_head(player_name: str, opponent_name: str, format: str, pitch_type: Optional[str] = None, stadium: int = 0):
    """
    Returns win/loss record and stats against a specific opponent.
    """
    # Filter matches by format first
    filtered = matches_df[
        (matches_df['format'] == format) & 
        (matches_df['player_name'] == player_name) & 
        (matches_df['opponent_name'] == opponent_name)    
    ]
    
    # Then filter by pitch_type if provided
    if pitch_type:
        filtered = filtered[matches_df['pitch_type'] == pitch_type]
    
    # If stadium is specified (not 0) and stadium column exists, filter by stadium
    if stadium != 0 and 'stadium' in matches_df.columns:
        filtered = filtered[filtered['stadium'] == stadium]
    
    if len(filtered) == 0:
        return {
            "error": f"No data found for pitch_type='{pitch_type}' and format='{format}'",
            "matches_played": 0,
            "wins": 0,
            "losses": 0,
            "avg_runs_scored": 0
        }
    
    # Calculate win/loss record
    wins = len(filtered[filtered['result'] == 'Win'])
    losses = len(filtered[filtered['result'] == 'Loss'])
    matches_played = len(filtered)
    avg_runs_scored = filtered['runs'].mean()
    
    return {
        "matches_played": matches_played,
        "wins": wins,
        "losses": losses,
        "avg_runs_scored": avg_runs_scored
    }