import asyncio
import os
from dotenv import load_dotenv
from google.adk.models.google_llm import Gemini
from agents.vr_cricket_coach.agent import (
    get_player_history,
    compute_safe_target_vs_opponent,
    get_toss_recommendation,
    get_safe_target_info
)

load_dotenv()

def test_data_functions():
    print("Testing data functions...")
    
    # Test get_player_history with format
    print("\n1. Testing get_player_history(format='T20')...")
    df_t20 = get_player_history("Karthik", game_format="T20")
    print(f"   Rows: {len(df_t20)}")
    if not df_t20.empty:
        formats = df_t20["format"].unique()
        print(f"   Formats found: {formats}")
        assert all(f.lower() == "t20" for f in formats)
    
    print("\n2. Testing get_player_history(format='Test')...")
    df_test = get_player_history("Karthik", game_format="Test")
    print(f"   Rows: {len(df_test)}")
    if not df_test.empty:
        formats = df_test["format"].unique()
        print(f"   Formats found: {formats}")
        assert all(f.lower() == "test" for f in formats)

    # Test compute_safe_target_vs_opponent with format
    print("\n3. Testing compute_safe_target_vs_opponent(format='T20')...")
    target_t20 = compute_safe_target_vs_opponent(opponent_name="Sid", game_format="T20")
    print(f"   T20 Safe Score: {target_t20.get('safe_score')}")
    
    print("\n4. Testing compute_safe_target_vs_opponent(format='Test')...")
    target_test = compute_safe_target_vs_opponent(opponent_name="Sid", game_format="Test")
    print(f"   Test Safe Score: {target_test.get('safe_score')}")
    
    # They should likely be different if data exists
    if target_t20.get('safe_score') and target_test.get('safe_score'):
        print(f"   Difference: {target_t20['safe_score']} vs {target_test['safe_score']}")

if __name__ == "__main__":
    test_data_functions()
