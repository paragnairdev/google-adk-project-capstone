import pandas as pd
from .config import DATASET_DIR, PLAYERS_CSV, MATCHES_CSV

# Load datasets
print(f"📂 Loading data from {DATASET_DIR}...")
try:
    players_df = pd.read_csv(PLAYERS_CSV)
    matches_df = pd.read_csv(MATCHES_CSV)
    print(f"✅ Loaded {len(players_df)} players and {len(matches_df)} match records")
except FileNotFoundError as e:
    print(f"❌ Error: Could not find dataset files in {DATASET_DIR}")
    print(f"   Make sure players.csv and matches.csv exist in vr_cricket_dataset/")
    raise
