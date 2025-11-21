"""
Custom Tools for VR Cricket Strategist

This module implements 5 custom tools that enable data-driven strategy generation:
1. get_current_identity - Session-based user identification with dev mode fallback
2. set_current_identity - Set the user's identity in the session state
3. pick_random_commentator - Personality selection for engaging delivery
4. get_venue_trends - Statistical analysis of pitch and venue patterns
5. get_head_to_head - Historical matchup analysis between players
6. get_player_stats - Comprehensive player performance metrics

Design Pattern: All tools use pandas for efficient in-memory data processing
on CSV datasets, providing sub-second query response times.
"""
import os
import random
from typing import Optional
from google.adk.tools import ToolContext
from .data_loader import matches_df

# ============================================================================
# DEVELOPMENT CONFIGURATION
# ============================================================================
# This profile is auto-injected when no session state exists, enabling
# quick testing without authentication flows. In production, this would be
# replaced with actual user authentication.
TEST_PROFILE = {
    "player_name": "Joe", # Change this to the player's name you want to test with. All players are in vr_cricket_dataset/players.csv
    "team": "England",
    "batting_style": "Moderate" # Change this to the player's batting style. All batting styles are in vr_cricket_dataset/players.csv
}

# ============================================================================
# TOOL 1: USER IDENTITY MANAGEMENT
# ============================================================================
def get_current_identity(tool_context: ToolContext):
    """
    Retrieves the current player's identity from ADK session state.
    
    Design Pattern: Uses ADK's built-in session management to maintain user
    context across conversation turns. This enables personalized responses
    and historical data lookups specific to each player.
    
    Behavior:
    1. First checks session state for existing identity
    2. If found, returns cached identity (fast path)
    3. If missing, auto-injects TEST_PROFILE for development mode
    
    Production Enhancement: In production, this would integrate with:
    - OAuth authentication flow
    - Discord/Steam user profiles
    - Tournament registration systems
    
    Args:
        tool_context: ADK ToolContext providing access to session state
        
    Returns:
        dict: Player identity with keys: player_name, team, batting_style, auto_injected
    """

    # log the state
    print("Getting state")
    print(f"Player name: {tool_context.state.get('user:player_name', 'Not found')}")
    print(f"Team: {tool_context.state.get('user:team', 'Not found')}")
    print(f"Batting style: {tool_context.state.get('user:batting_style', 'Not found')}")
    
    # Check if we already know who the player is (cached in session)
    player_name = tool_context.state.get("user:player_name")
    
    if player_name:
        # Fast path: return existing identity
        return {
            "player_name": player_name, 
            "team": tool_context.state.get('user:team'), 
            "batting_style": tool_context.state.get('user:batting_style'), 
            "auto_injected": False
        }

    # Development Mode: Auto-inject test profile for quick testing
    # This eliminates the need for authentication during development
    print("⚠️ [DEV MODE] No identity found. Auto-injecting test profile.")
    
    for key, value in TEST_PROFILE.items():
        tool_context.state[f"user:{key}"] = value
    
    return {
        "player_name": tool_context.state['user:player_name'], 
        "team": tool_context.state['user:team'], 
        "batting_style": tool_context.state['user:batting_style'], 
        "auto_injected": True
    }

# ============================================================================
# TOOL 2: SET USER IDENTITY
# ============================================================================
def set_current_identity(player_name: str, tool_context: ToolContext, team: Optional[str] = None, batting_style: Optional[str] = None):
    """
    Sets the user's identity in the session state.

    Args:
        player_name: The player's name
        tool_context: ADK ToolContext providing access to session state
        team: The player's team (optional, preserves existing value if not provided)
        batting_style: The player's batting style (optional, preserves existing value if not provided)

    Design Pattern: Uses ADK's built-in session management to maintain user
    context across conversation turns. This enables personalized responses
    and historical data lookups specific to each player.

    Behavior:
    1. Sets the user's identity in the session state
    2. If team or batting_style are not provided, preserves existing values from state
    3. Returns the user's identity

    Returns:
        dict: The user's identity
            player_name: player_name
            team: team (from parameter or existing state)
            batting_style: batting_style (from parameter or existing state)
    """

    # log the state
    print("Setting state")
    print(f"Player name: {tool_context.state.get('user:player_name', 'Not found')}")
    print(f"Team: {tool_context.state.get('user:team', 'Not found')}")
    print(f"Batting style: {tool_context.state.get('user:batting_style', 'Not found')}")
    # Always set the player name
    tool_context.state[f"user:player_name"] = player_name
    
    # Preserve existing values if new ones aren't provided
    if team is not None:
        tool_context.state[f"user:team"] = team
        
    if batting_style is not None:
        tool_context.state[f"user:batting_style"] = batting_style

    return get_current_identity(tool_context)

# ============================================================================
# TOOL 3: COMMENTATOR SELECTION
# ============================================================================
def pick_random_commentator() -> str:
    """
    Randomly selects one cricket commentator personality for response delivery.
    
    Design Decision: We use random selection rather than ML-based matching to
    maintain variety and entertainment value. Each commentator has distinct
    personality traits defined in their agent instructions.
    
    Returns:
        str: Commentator name ("Boycott", "Sidhu", "Nasser", or "Harsha")
    """
    options = ["Boycott", "Sidhu", "Nasser", "Harsha"]
    return random.choice(options)

# ============================================================================
# TOOL 4: VENUE & PITCH ANALYSIS
# ============================================================================
def get_venue_trends(format: str, pitch_type: Optional[str] = None, stadium: int = 0):
    """
    Analyzes historical match data to identify venue and pitch-specific patterns.
    
    Design Decision: Pre-aggregates statistics rather than storing pre-computed
    values to ensure flexibility when filtering by multiple dimensions (format,
    pitch, stadium).
    
    Algorithm:
    1. Filter dataset by format (T20/ODI/Test)
    2. Apply optional pitch_type filter (Green/Dry/Bouncy/Normal)
    3. Apply optional stadium filter for venue-specific analysis
    4. Calculate first innings average (target setting benchmark)
    5. Calculate win rates for batting first vs. chasing
    
    Use Case: Answers questions like "What's a safe score on a green pitch in T20?"
    or "Do teams chasing win more often at this venue?"
    
    Args:
        format: Match format (e.g., 'T20', 'ODI', 'Test')
        pitch_type: Optional pitch type (e.g., 'Dry', 'Bouncy', 'Green', 'Normal')
        stadium: Optional stadium ID (default=0 means all stadiums)
        
    Returns:
        dict: Contains avg_first_innings_score, win_rate_batting_first,
              win_rate_batting_second, total_matches
    """
    # Multi-stage filtering for performance: narrow by format first (largest reduction)
    filtered = matches_df[matches_df['format'] == format]
    
    # Apply pitch filter if specified
    if pitch_type:
        filtered = filtered[matches_df['pitch_type'] == pitch_type]
    
    # Apply stadium filter if specified (future enhancement for venue-specific analysis)
    if stadium != 0 and 'stadium' in matches_df.columns:
        filtered = filtered[filtered['stadium'] == stadium]
    
    # Handle empty result set gracefully
    if len(filtered) == 0:
        return {
            "error": f"No data found for pitch_type='{pitch_type}' and format='{format}'",
            "avg_first_innings_score": 0,
            "win_rate_batting_first": 0.0,
            "win_rate_batting_second": 0.0
        }
    
    # Calculate first innings statistics (teams batting first)
    first_innings = filtered[filtered['innings_number'] == 1]
    avg_first_innings_score = round(first_innings['runs'].mean(), 2) if len(first_innings) > 0 else 0
    
    # Calculate batting first win rate
    # Note: 'Win' in first innings means the team that batted first won
    wins_batting_first = len(first_innings[first_innings['result'] == 'Win'])
    total_batting_first = len(first_innings)
    win_rate_batting_first = round(wins_batting_first / total_batting_first, 2) if total_batting_first > 0 else 0.0
    
    # Calculate chasing win rate (batting second)
    second_innings = filtered[filtered['innings_number'] == 2]
    wins_batting_second = len(second_innings[second_innings['result'] == 'Win'])
    total_batting_second = len(second_innings)
    win_rate_batting_second = round(wins_batting_second / total_batting_second, 2) if total_batting_second > 0 else 0.0
    
    return {
        "avg_first_innings_score": avg_first_innings_score,
        "win_rate_batting_first": win_rate_batting_first,
        "win_rate_batting_second": win_rate_batting_second,
        "total_matches": len(filtered) // 2  # Each match = 2 innings records
    }

# ============================================================================
# TOOL 5: HEAD-TO-HEAD MATCHUP ANALYSIS
# ============================================================================
def get_head_to_head(player_name: str, opponent_name: str, format: str, pitch_type: Optional[str] = None, stadium: int = 0):
    """
    Analyzes historical performance against a specific opponent.
    
    Design Decision: Filters from the player's perspective to provide
    personalized insights. This enables queries like "How do I perform
    against Wizheart in T20s on green pitches?"
    
    Behavior:
    - Focuses on matchups: player vs specific opponent
    - Accounts for format-specific dynamics (T20 vs Test strategies differ)
    - Optional pitch/venue filtering for contextual analysis
    
    Use Case: "I'm facing Ragz tomorrow - what's my record against him?"
    This tool powers the tactical recommendation by identifying weaknesses
    in specific matchups.
    
    Args:
        player_name: The player requesting analysis (typically from session)
        opponent_name: The opponent they're facing
        format: Match format (e.g., 'T20', 'ODI', 'Test')
        pitch_type: Optional pitch type filter
        stadium: Optional stadium filter
        
    Returns:
        dict: Contains matches_played, wins, losses, avg_runs_scored
    """
    # Multi-condition filter: player, opponent, and format
    filtered = matches_df[
        (matches_df['format'] == format) & 
        (matches_df['player_name'] == player_name) & 
        (matches_df['opponent_name'] == opponent_name)    
    ]
    
    # Apply optional pitch filter for context-specific analysis
    if pitch_type:
        filtered = filtered[matches_df['pitch_type'] == pitch_type]
    
    # Apply optional stadium filter
    if stadium != 0 and 'stadium' in matches_df.columns:
        filtered = filtered[filtered['stadium'] == stadium]
    
    # Handle case where no matchup history exists
    if len(filtered) == 0:
        return {
            "error": f"No data found for pitch_type='{pitch_type}' and format='{format}'",
            "matches_played": 0,
            "wins": 0,
            "losses": 0,
            "avg_runs_scored": 0
        }
    
    # Aggregate matchup statistics
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


# ============================================================================
# TOOL 6: COMPREHENSIVE PLAYER STATISTICS
# ============================================================================
def get_player_stats(player_name: str, format: str):
    """
    Generates comprehensive player performance statistics for a specific format.
    
    Design Decision: Calculates all metrics on-demand rather than pre-computing
    to ensure real-time accuracy when dataset is updated. Uses pandas vectorized
    operations for performance (sub-second response on 1000+ match records).
    
    Calculated Metrics:
    - Basic: matches, total runs, total overs
    - Averages: batting average (runs per match)
    - Performance: strike rate (runs per 100 balls)
    - Milestones: hundreds, fifties, ducks
    - Advanced: double/triple/quadruple/quintuple hundreds (VR Cricket specific)
    - Bowling: wickets, economy rate
    
    Use Case: Answers queries like "What's my T20 batting average?" or
    "Show me my career stats in ODI format"
    
    Implementation Note: Strike rate calculation assumes 6 balls per over
    (standard cricket rule), converting overs to balls before percentage calculation.
    
    Args:
        player_name: Name of the player
        format: Match format (e.g., 'T20', 'ODI', 'Test')
    
    Returns:
        dict: Nested dictionary with player_name, format, and stats sub-dictionary
              containing all performance metrics
    """
    # Filter dataset to player's matches in specified format
    filtered = matches_df[
        (matches_df['player_name'] == player_name) & 
        (matches_df['format'] == format)
    ]
    
    # Handle case where player has no matches in this format
    if len(filtered) == 0:
        return {
            "player_name": player_name,
            "format": format,
            "stats": {
                "matches": 0,
                "runs": 0,
                "overs": 0,
                "average": 0,
                "strike_rate": 0,
                "double_hundreds": 0,
                "triple_hundreds": 0,
                "quadruple_hundreds": 0,
                "quintuple_hundreds": 0,
                "hundreds": 0,
                "fifties": 0,
                "ducks": 0,
                "wickets": 0,
                "economy": 0,
            }
        }
    
    # Aggregate basic statistics using pandas vectorized operations
    matches = len(filtered)
    total_runs = int(filtered['runs'].sum())
    total_overs = int(filtered['overs'].sum())
    total_wickets = int(filtered['wickets'].sum())
    
    # Milestone achievements (pre-recorded in dataset)
    total_hundreds = int(filtered['hundreds'].sum())
    total_double_hundreds = int(filtered['double_hundreds'].sum())
    total_triple_hundreds = int(filtered['triple_hundreds'].sum())
    total_quadruple_hundreds = int(filtered['quadruple_hundreds'].sum())
    total_quintuple_hundreds = int(filtered['quintuple_hundreds'].sum())
    total_ducks = int(filtered['ducks'].sum())

    # Calculate batting average (total runs divided by matches played)
    # Note: In VR Cricket, we use per-match average rather than traditional
    # cricket's "runs per dismissal" since VR matches always have fixed overs
    average = round(total_runs / matches, 2) if matches > 0 else 0
    
    # Calculate strike rate (runs scored per 100 balls faced)
    # Conversion: 1 over = 6 balls in cricket
    total_balls = total_overs * 6
    strike_rate = round((total_runs / total_balls) * 100, 2) if total_balls > 0 else 0
    
    # Calculate fifties: innings between 50-99 runs (100+ counts as hundreds)
    fifties = len(filtered[(filtered['runs'] >= 50) & (filtered['runs'] < 100)])
    
    # Calculate economy rate: runs conceded per over (bowling metric)
    # Lower economy = better bowling performance
    economy = round(total_runs / total_overs, 2) if total_overs > 0 else 0
    
    return {
        "player_name": player_name,
        "format": format,
        "stats": {
            "matches": matches,
            "runs": total_runs,
            "overs": total_overs,
            "average": average,
            "strike_rate": strike_rate,
            "hundreds": total_hundreds,
            "fifties": fifties,
            "wickets": total_wickets,
            "economy": economy,
            "double_hundreds": total_double_hundreds,
            "triple_hundreds": total_triple_hundreds,
            "quadruple_hundreds": total_quadruple_hundreds,
            "quintuple_hundreds": total_quintuple_hundreds,
            "ducks": total_ducks,
        }
    }

