"""
Pytest configuration and shared fixtures for vr_cricket_strategist tests
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add the project root to the path to enable imports
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


@pytest.fixture
def sample_players_data():
    """Fixture providing sample player data"""
    return pd.DataFrame({
        'player_name': ['Alice', 'Bob', 'Charlie', 'Dave'],
        'team': ['India', 'England', 'Australia', 'New Zealand'],
        'batting_style': ['Aggressive', 'Moderate', 'Defensive', 'Moderate'],
        'role': ['Batsman', 'All-rounder', 'Bowler', 'Batsman']
    })


@pytest.fixture
def sample_matches_data():
    """Fixture providing sample match data"""
    return pd.DataFrame({
        'match_id': [1, 1, 2, 2, 3, 3, 4, 4],
        'player_name': ['Alice', 'Alice', 'Bob', 'Bob', 'Alice', 'Alice', 'Bob', 'Bob'],
        'opponent_name': ['Charlie', 'Charlie', 'Dave', 'Dave', 'Dave', 'Dave', 'Charlie', 'Charlie'],
        'format': ['T20', 'T20', 'ODI', 'ODI', 'T20', 'T20', 'T20', 'T20'],
        'pitch_type': ['Dry', 'Dry', 'Green', 'Green', 'Normal', 'Normal', 'Bouncy', 'Bouncy'],
        'stadium': [1, 1, 2, 2, 3, 3, 1, 1],
        'innings_number': [1, 2, 1, 2, 1, 2, 1, 2],
        'runs': [180, 160, 280, 260, 175, 180, 190, 170],
        'wickets': [7, 10, 5, 8, 9, 6, 8, 10],
        'result': ['Win', 'Loss', 'Win', 'Loss', 'Loss', 'Win', 'Win', 'Loss'],
        'toss_decision': ['Bat', 'Bowl', 'Bat', 'Bowl', 'Bowl', 'Bat', 'Bat', 'Bowl']
    })


@pytest.fixture
def mock_tool_context():
    """Fixture providing a mock ToolContext"""
    from unittest.mock import Mock
    
    context = Mock()
    session = Mock()
    state = {}
    session.state = state
    context.session = session
    
    return context


@pytest.fixture
def mock_tool_context_with_identity():
    """Fixture providing a mock ToolContext with identity set"""
    from unittest.mock import Mock
    
    context = Mock()
    session = Mock()
    state = {
        'player_name': 'TestPlayer',
        'team': 'TestTeam',
        'batting_style': 'Aggressive',
        'role': 'Batsman'
    }
    session.state = state
    context.session = session
    
    return context


@pytest.fixture
def sample_venue_trends_response():
    """Fixture providing sample venue trends response"""
    return {
        'avg_first_innings_score': 175.5,
        'win_rate_batting_first': 0.55,
        'win_rate_batting_second': 0.45,
        'total_matches': 20
    }


@pytest.fixture
def sample_head_to_head_response():
    """Fixture providing sample head-to-head response"""
    return {
        'matches_played': 10,
        'wins': 6,
        'losses': 4,
        'avg_runs_scored': 168.5
    }


@pytest.fixture
def sample_empty_matches_data():
    """Fixture providing empty matches dataframe with correct structure"""
    return pd.DataFrame(columns=[
        'match_id', 'player_name', 'opponent_name', 'format', 
        'pitch_type', 'stadium', 'innings_number', 'runs', 
        'wickets', 'result', 'toss_decision'
    ])


def pytest_configure(config):
    """Pytest configuration hook"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically"""
    for item in items:
        # Add 'unit' marker to tests by default
        if 'integration' not in item.keywords and 'slow' not in item.keywords:
            item.add_marker(pytest.mark.unit)

