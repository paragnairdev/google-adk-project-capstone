from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
from .data_loader import matches_df

def get_player_history(player_name: str, opponent_name: Optional[str] = None, game_format: Optional[str] = None) -> pd.DataFrame:
    """Get match history for a specific player, optionally filtered by opponent and format."""
    print(f"DEBUG: get_player_history called with player={player_name}, opponent={opponent_name}, format={game_format}")
    df = matches_df[matches_df["player_name"] == player_name].copy()
    if opponent_name:
        df = df[df["opponent_name"] == opponent_name]
    if game_format:
        # Case-insensitive match for format
        df = df[df["format"].str.lower() == game_format.lower()]
    print(f"DEBUG: get_player_history returning {len(df)} rows")
    return df


def compute_basic_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute basic batting metrics from match dataframe."""
    if df.empty:
        return {
            "innings": 0,
            "avg_runs": None,
            "avg_runrate": None,
            "avg_runs_per_wicket": None,
        }

    innings = len(df)
    avg_runs = df["runs"].mean()
    avg_runrate = (df["runs"] / df["overs"]).mean()

    # Avoid divide-by-zero issues
    wickets = df["wickets"].replace(0, np.nan)
    avg_rpw = (df["runs"] / wickets).mean() if not wickets.isna().all() else None

    return {
        "innings": int(innings),
        "avg_runs": float(round(avg_runs, 2)),
        "avg_runrate": float(round(avg_runrate, 2)),
        "avg_runs_per_wicket": float(round(avg_rpw, 2)) if avg_rpw is not None else None,
    }


def compute_safe_target_vs_opponent(opponent_name: Optional[str] = None, game_format: Optional[str] = None) -> Dict[str, Any]:
    """Calculate par, competitive, and safe target scores based on opponent's chasing history."""
    if opponent_name:
        opp_df = matches_df[
            (matches_df["player_name"] == opponent_name)
            & (matches_df["is_chasing"] == True)
        ]
    else:
        opp_df = matches_df[matches_df["is_chasing"] == True]

    if game_format:
        opp_df = opp_df[opp_df["format"].str.lower() == game_format.lower()]

    if opp_df.empty:
        return {
            "sample_size": 0,
            "par_score": None,
            "competitive_score": None,
            "safe_score": None,
            "note": "No chasing history found for this opponent.",
            "top_chases": [],
        }

    scores = opp_df["runs"].values
    par = int(np.percentile(scores, 50))
    comp = int(np.percentile(scores, 60))
    safe = int(np.percentile(scores, 75) + 5)  # add buffer

    # Get top 3 chases for context
    top_chases_df = (
        opp_df.sort_values("runs", ascending=False)
        .head(3)[["date", "runs", "overs", "wickets", "format", "pitch_type", "difficulty"]]
    )

    top_chases = top_chases_df.to_dict(orient="records")

    return {
        "sample_size": int(len(scores)),
        "par_score": par,
        "competitive_score": comp,
        "safe_score": safe,
        "note": "Heuristic based on opponent chasing scores.",
        "top_chases": top_chases,
    }


def brief_stats_text(player_name: str) -> str:
    """Generate a brief text summary of player statistics."""
    df = get_player_history(player_name)
    m = compute_basic_metrics(df)
    if m["innings"] == 0:
        return f"I couldn't find any innings for {player_name} in the dataset."

    return (
        f"{player_name} has played {m['innings']} innings.\n"
        f"- Average runs: {m['avg_runs']}\n"
        f"- Average run rate: {m['avg_runrate']} runs/over\n"
        f"- Average runs per wicket: {m['avg_runs_per_wicket']}"
    )
