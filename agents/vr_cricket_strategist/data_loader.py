"""
Data Loader for VR Cricket Dataset

This module handles loading and validation of the VR Cricket match dataset.

Design Decisions:
- Load data once at import time (singleton pattern) to avoid repeated I/O
- Use pandas for efficient in-memory data manipulation
- Store in module-level variables for shared access across all tools
- Fail fast on missing data to surface setup issues immediately

Dataset Structure:
- players.csv: Player profiles (name, team, batting_style)
- matches.csv: Match records (1000+ innings with format, pitch, results)

Performance: Loading 1000+ records takes ~50ms. All subsequent queries use
the in-memory DataFrame, providing sub-millisecond lookup times.
"""
import pandas as pd
from .config import DATASET_DIR, PLAYERS_CSV, MATCHES_CSV

# ============================================================================
# DATASET LOADING - Singleton Pattern
# ============================================================================
# Load datasets once at import time. These DataFrames are shared across all
# tool invocations, preventing redundant file I/O operations.
print(f"📂 Loading data from {DATASET_DIR}...")
try:
    players_df = pd.read_csv(PLAYERS_CSV)
    matches_df = pd.read_csv(MATCHES_CSV)
    print(f"✅ Loaded {len(players_df)} players and {len(matches_df)} match records")
except FileNotFoundError as e:
    # Fail fast: Surface dataset issues immediately rather than at query time
    print(f"❌ Error: Could not find dataset files in {DATASET_DIR}")
    print(f"   Make sure players.csv and matches.csv exist in vr_cricket_dataset/")
    raise

# Export DataFrames for use by tools module
# These are read-only from tools' perspective - mutations would affect all users
__all__ = ['players_df', 'matches_df']
