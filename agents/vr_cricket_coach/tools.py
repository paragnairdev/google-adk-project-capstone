from typing import Any, Dict, Optional
import pandas as pd
from google.adk.tools import ToolContext
from .analytics import (
    get_player_history,
    compute_basic_metrics,
    compute_safe_target_vs_opponent,
    brief_stats_text
)

def save_player_identity(tool_context: ToolContext, player_name: str) -> Dict[str, Any]:
    """Save the current player's name in session state."""
    print(f"DEBUG: save_player_identity called with {player_name}")
    tool_context.state["user:player_name"] = player_name
    return {"status": "success", "player_name": player_name}


def get_player_identity(tool_context: ToolContext) -> Dict[str, Any]:
    """Retrieve current player identity from session state."""
    print("DEBUG: get_player_identity called")
    name = tool_context.state.get("user:player_name")
    if not name:
        print("DEBUG: get_player_identity returning not_found")
        return {"status": "not_found"}
    print(f"DEBUG: get_player_identity returning {name}")
    return {"status": "success", "player_name": name}


def get_brief_stats(player_name: str) -> Dict[str, Any]:
    """Return brief summary stats for the given player."""
    print(f"DEBUG: get_brief_stats called with {player_name}")
    text = brief_stats_text(player_name)
    print(f"DEBUG: get_brief_stats returning: {text[:50]}...")
    return {"status": "success", "summary": text}


def get_toss_recommendation(player_name: str, opponent_name: Optional[str] = None, game_format: Optional[str] = None) -> Dict[str, Any]:
    """Compute toss recommendation based on player's performance when setting vs chasing."""
    df_player = get_player_history(player_name, opponent_name, game_format)
    df_opp = get_player_history(opponent_name, player_name, game_format) if opponent_name else pd.DataFrame()

    if df_player.empty:
        return {
            "status": "insufficient_data",
            "message": "Not enough history for you vs this opponent.",
        }

    # Player: setting vs chasing
    df_set = df_player[df_player["is_chasing"] == False]
    df_chase = df_player[df_player["is_chasing"] == True]
    metrics_set = compute_basic_metrics(df_set)
    metrics_chase = compute_basic_metrics(df_chase)

    # Opponent chasing performance
    df_opp_chasing = df_opp[df_opp["is_chasing"] == True] if not df_opp.empty else pd.DataFrame()
    opp_chase = compute_basic_metrics(df_opp_chasing) if not df_opp_chasing.empty else None

    recommendation = "BOWL FIRST"
    reasoning = []

    reasoning.append(f"Your avg when setting a target: {metrics_set['avg_runs']}")
    reasoning.append(f"Your avg when chasing: {metrics_chase['avg_runs']}")

    if opp_chase and opp_chase["avg_runs"] is not None:
        reasoning.append(f"Opponent's avg when chasing: {opp_chase['avg_runs']}")

    # Simple rule: if you're clearly better setting and opponent isn't great chasing, bat first
    if (
        metrics_set["avg_runs"] is not None
        and metrics_chase["avg_runs"] is not None
        and metrics_set["avg_runs"] > metrics_chase["avg_runs"]
        and opp_chase
        and opp_chase["avg_runs"] is not None
        and opp_chase["avg_runs"] < metrics_set["avg_runs"]
    ):
        recommendation = "BAT FIRST"

    return {
        "status": "success",
        "recommendation": recommendation,
        "player_set_metrics": metrics_set,
        "player_chase_metrics": metrics_chase,
        "opponent_chase_metrics": opp_chase,
        "reasoning": reasoning,
    }


def get_safe_target_info(opponent_name: Optional[str] = None, game_format: Optional[str] = None) -> Dict[str, Any]:
    """Return heuristic par/competitive/safe target vs opponent when batting first."""
    info = compute_safe_target_vs_opponent(opponent_name, game_format)
    return {"status": "success", **info}


def get_matchup_stats(player_name: str, opponent_name: str, game_format: Optional[str] = None) -> Dict[str, Any]:
    """
    Get comprehensive matchup statistics for both player and opponent.
    This demonstrates PARALLEL data fetching capability.
    In a real implementation, these could be async calls to different data sources.
    """
    # Fetch both player's and opponent's stats (simulating parallel data access)
    player_history = get_player_history(player_name, opponent_name, game_format)
    opponent_history = get_player_history(opponent_name, player_name, game_format)
    
    player_metrics = compute_basic_metrics(player_history)
    opponent_metrics = compute_basic_metrics(opponent_history)
    
    return {
        "status": "success",
        "player_name": player_name,
        "opponent_name": opponent_name,
        "player_metrics": player_metrics,
        "opponent_metrics": opponent_metrics,
        "head_to_head_matches": len(player_history),
    }
