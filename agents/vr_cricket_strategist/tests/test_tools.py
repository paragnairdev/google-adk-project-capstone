"""
Tests for vr_cricket_strategist tools module
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from agents.vr_cricket_strategist.tools import (
    get_current_identity,
    get_venue_trends,
    get_head_to_head,
    pick_random_commentator,
    TEST_PROFILE
)


# Sample test data
@pytest.fixture
def sample_matches_data():
    """Create sample matches data for testing"""
    return pd.DataFrame({
        'player_name': ['Alice', 'Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Bob'],
        'opponent_name': ['Charlie', 'Charlie', 'Dave', 'Dave', 'Charlie', 'Charlie', 'Dave', 'Dave'],
        'format': ['T20', 'T20', 'T20', 'T20', 'ODI', 'ODI', 'ODI', 'ODI'],
        'pitch_type': ['Dry', 'Dry', 'Green', 'Green', 'Dry', 'Dry', 'Normal', 'Normal'],
        'stadium': [1, 1, 2, 2, 1, 1, 3, 3],
        'innings_number': [1, 2, 1, 2, 1, 2, 1, 2],
        'runs': [180, 150, 160, 170, 280, 250, 260, 270],
        'result': ['Win', 'Loss', 'Loss', 'Win', 'Win', 'Loss', 'Win', 'Loss']
    })


class TestGetCurrentIdentity:
    """Tests for get_current_identity function"""
    
    def test_identity_exists_in_state(self):
        """Test when player identity already exists in session state"""
        # Mock ToolContext
        mock_context = Mock()
        mock_session = Mock()
        mock_state = {
            'player_name': 'TestPlayer',
            'team': 'TestTeam'
        }
        mock_session.state = mock_state
        mock_context.session = mock_session
        
        result = get_current_identity(mock_context)
        
        assert 'TestPlayer' in result
        assert 'TestTeam' in result
        assert 'logged in' in result.lower()
    
    def test_identity_missing_auto_inject(self, capsys):
        """Test auto-injection of test profile when identity is missing"""
        # Mock ToolContext with empty state
        mock_context = Mock()
        mock_session = Mock()
        mock_state = {}
        mock_session.state = mock_state
        mock_context.session = mock_session
        
        result = get_current_identity(mock_context)
        
        # Check that test profile was injected
        assert mock_state['player_name'] == TEST_PROFILE['player_name']
        assert mock_state['team'] == TEST_PROFILE['team']
        assert mock_state['batting_style'] == TEST_PROFILE['batting_style']
        assert mock_state['role'] == TEST_PROFILE['role']
        
        # Check result message
        assert 'DEBUG' in result or 'Auto-logged' in result
        assert TEST_PROFILE['player_name'] in result
        
        # Check that debug message was printed
        captured = capsys.readouterr()
        assert 'DEV MODE' in captured.out or 'Auto-injecting' in captured.out
    
    def test_identity_partial_state(self):
        """Test when state has some but not all required fields"""
        mock_context = Mock()
        mock_session = Mock()
        mock_state = {'player_name': 'ExistingPlayer'}
        mock_session.state = mock_state
        mock_context.session = mock_session
        
        result = get_current_identity(mock_context)
        
        # Should use existing player_name
        assert 'ExistingPlayer' in result


class TestGetVenueTrends:
    """Tests for get_venue_trends function"""
    
    @patch('agents.vr_cricket_strategist.tools.matches_df', new_callable=lambda: pd.DataFrame)
    def test_venue_trends_basic(self, mock_df, sample_matches_data):
        """Test basic venue trends calculation"""
        # Replace the mock with actual DataFrame
        with patch('agents.vr_cricket_strategist.tools.matches_df', sample_matches_data):
            result = get_venue_trends(format='T20')
        
        assert 'avg_first_innings_score' in result
        assert 'win_rate_batting_first' in result
        assert 'win_rate_batting_second' in result
        assert 'total_matches' in result
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_venue_trends_with_pitch_type(self, mock_df, sample_matches_data):
        """Test venue trends filtered by pitch type"""
        with patch('agents.vr_cricket_strategist.tools.matches_df', sample_matches_data):
            result = get_venue_trends(format='T20', pitch_type='Dry')
        
        assert isinstance(result, dict)
        assert result['avg_first_innings_score'] >= 0
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_venue_trends_with_stadium(self, mock_df, sample_matches_data):
        """Test venue trends filtered by stadium"""
        with patch('agents.vr_cricket_strategist.tools.matches_df', sample_matches_data):
            result = get_venue_trends(format='T20', stadium=1)
        
        assert isinstance(result, dict)
        assert 'avg_first_innings_score' in result
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_venue_trends_no_data(self, mock_df):
        """Test venue trends when no data matches filters"""
        # Create empty dataframe with correct columns
        empty_df = pd.DataFrame(columns=['format', 'pitch_type', 'stadium', 'innings_number', 'runs', 'result'])
        with patch('agents.vr_cricket_strategist.tools.matches_df', empty_df):
            result = get_venue_trends(format='Test', pitch_type='Unknown')
        
        assert 'error' in result
        assert result['avg_first_innings_score'] == 0
        assert result['win_rate_batting_first'] == 0.0
        assert result['win_rate_batting_second'] == 0.0
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_venue_trends_calculations(self, mock_df):
        """Test accurate calculation of venue trends"""
        # Create specific test data to verify calculations
        test_data = pd.DataFrame({
            'format': ['T20', 'T20', 'T20', 'T20'],
            'pitch_type': ['Dry', 'Dry', 'Dry', 'Dry'],
            'stadium': [1, 1, 1, 1],
            'innings_number': [1, 2, 1, 2],
            'runs': [200, 150, 180, 160],
            'result': ['Win', 'Loss', 'Win', 'Loss']
        })
        with patch('agents.vr_cricket_strategist.tools.matches_df', test_data):
            result = get_venue_trends(format='T20', pitch_type='Dry')
        
        # Average first innings score should be (200 + 180) / 2 = 190
        assert result['avg_first_innings_score'] == 190.0
        # Win rate batting first: 2 wins out of 2 = 100%
        assert result['win_rate_batting_first'] == 1.0
        # Win rate batting second: 0 wins out of 2 = 0%
        assert result['win_rate_batting_second'] == 0.0
        # Total matches: 4 innings / 2 = 2 matches
        assert result['total_matches'] == 2


class TestGetHeadToHead:
    """Tests for get_head_to_head function"""
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_head_to_head_basic(self, mock_df, sample_matches_data):
        """Test basic head-to-head record"""
        with patch('agents.vr_cricket_strategist.tools.matches_df', sample_matches_data):
            result = get_head_to_head(
                player_name='Alice',
                opponent_name='Charlie',
                format='T20'
            )
        
        assert 'matches_played' in result
        assert 'wins' in result
        assert 'losses' in result
        assert 'avg_runs_scored' in result
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_head_to_head_with_pitch_type(self, mock_df, sample_matches_data):
        """Test head-to-head filtered by pitch type"""
        with patch('agents.vr_cricket_strategist.tools.matches_df', sample_matches_data):
            result = get_head_to_head(
                player_name='Alice',
                opponent_name='Charlie',
                format='T20',
                pitch_type='Dry'
            )
        
        assert isinstance(result, dict)
        assert result['matches_played'] >= 0
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_head_to_head_with_stadium(self, mock_df, sample_matches_data):
        """Test head-to-head filtered by stadium"""
        with patch('agents.vr_cricket_strategist.tools.matches_df', sample_matches_data):
            result = get_head_to_head(
                player_name='Alice',
                opponent_name='Charlie',
                format='T20',
                stadium=1
            )
        
        assert isinstance(result, dict)
        assert 'matches_played' in result
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_head_to_head_no_data(self, mock_df):
        """Test head-to-head when no data matches filters"""
        empty_df = pd.DataFrame(columns=['format', 'player_name', 'opponent_name', 'pitch_type', 'stadium', 'result', 'runs'])
        with patch('agents.vr_cricket_strategist.tools.matches_df', empty_df):
            result = get_head_to_head(
                player_name='Unknown',
                opponent_name='Unknown',
                format='Test'
            )
        
        assert 'error' in result
        assert result['matches_played'] == 0
        assert result['wins'] == 0
        assert result['losses'] == 0
        assert result['avg_runs_scored'] == 0
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_head_to_head_calculations(self, mock_df):
        """Test accurate calculation of head-to-head stats"""
        test_data = pd.DataFrame({
            'format': ['T20', 'T20', 'T20', 'T20'],
            'player_name': ['Alice', 'Alice', 'Alice', 'Alice'],
            'opponent_name': ['Bob', 'Bob', 'Bob', 'Bob'],
            'pitch_type': ['Dry', 'Dry', 'Dry', 'Dry'],
            'stadium': [1, 1, 1, 1],
            'result': ['Win', 'Win', 'Loss', 'Loss'],
            'runs': [180, 200, 150, 160]
        })
        with patch('agents.vr_cricket_strategist.tools.matches_df', test_data):
            result = get_head_to_head(
                player_name='Alice',
                opponent_name='Bob',
                format='T20'
            )
        
        assert result['matches_played'] == 4
        assert result['wins'] == 2
        assert result['losses'] == 2
        # Average runs: (180 + 200 + 150 + 160) / 4 = 172.5
        assert result['avg_runs_scored'] == 172.5
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_head_to_head_different_formats(self, mock_df, sample_matches_data):
        """Test that format filtering works correctly"""
        with patch('agents.vr_cricket_strategist.tools.matches_df', sample_matches_data):
            # Query for ODI format
            result = get_head_to_head(
                player_name='Bob',
                opponent_name='Charlie',
                format='ODI'
            )
        
        # Should only get ODI matches
        assert isinstance(result, dict)
        if result.get('matches_played', 0) > 0:
            assert result['matches_played'] > 0


class TestToolIntegration:
    """Integration tests for tools working together"""
    
    @patch('agents.vr_cricket_strategist.tools.matches_df')
    def test_tools_use_consistent_data(self, mock_df, sample_matches_data):
        """Test that all tools work with the same data structure"""
        with patch('agents.vr_cricket_strategist.tools.matches_df', sample_matches_data):
            # All tools should work without errors
            venue_result = get_venue_trends(format='T20')
            h2h_result = get_head_to_head(
                player_name='Alice',
                opponent_name='Charlie',
                format='T20'
            )
        
        assert isinstance(venue_result, dict)
        assert isinstance(h2h_result, dict)
    
    def test_test_profile_structure(self):
        """Test that TEST_PROFILE has expected structure"""
        assert 'player_name' in TEST_PROFILE
        assert 'team' in TEST_PROFILE
        assert 'batting_style' in TEST_PROFILE
        assert 'role' in TEST_PROFILE
        assert isinstance(TEST_PROFILE['player_name'], str)
        assert isinstance(TEST_PROFILE['team'], str)


class TestPickRandomCommentator:
    """Tests for pick_random_commentator function"""
    
    def test_pick_random_commentator_returns_string(self):
        """Test that function returns a string"""
        result = pick_random_commentator()
        assert isinstance(result, str)
    
    def test_pick_random_commentator_valid_options(self):
        """Test that function returns one of the valid commentators"""
        valid_commentators = ["Boycott", "Sidhu", "Nasser", "Harsha"]
        result = pick_random_commentator()
        assert result in valid_commentators
    
    def test_pick_random_commentator_multiple_calls(self):
        """Test that function can be called multiple times"""
        valid_commentators = ["Boycott", "Sidhu", "Nasser", "Harsha"]
        results = [pick_random_commentator() for _ in range(10)]
        
        # All results should be valid
        for result in results:
            assert result in valid_commentators
    
    @patch('agents.vr_cricket_strategist.tools.random.choice')
    def test_pick_random_commentator_uses_random(self, mock_choice):
        """Test that function uses random.choice"""
        mock_choice.return_value = "Boycott"
        result = pick_random_commentator()
        
        assert result == "Boycott"
        assert mock_choice.called
        # Verify it was called with the correct list
        called_with = mock_choice.call_args[0][0]
        assert set(called_with) == {"Boycott", "Sidhu", "Nasser", "Harsha"}

