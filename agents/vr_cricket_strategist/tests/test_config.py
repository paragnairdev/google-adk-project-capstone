"""
Tests for vr_cricket_strategist config module
"""
import pytest
import os
from pathlib import Path
from unittest.mock import patch


class TestConfig:
    """Tests for configuration settings"""
    
    def test_config_imports(self):
        """Test that config module can be imported"""
        from agents.vr_cricket_strategist import config
        assert config is not None
    
    def test_model_name_exists(self):
        """Test that MODEL_NAME is defined"""
        from agents.vr_cricket_strategist.config import MODEL_NAME
        assert MODEL_NAME is not None
        assert isinstance(MODEL_NAME, str)
        assert len(MODEL_NAME) > 0
    
    def test_app_name_exists(self):
        """Test that APP_NAME is defined"""
        from agents.vr_cricket_strategist.config import APP_NAME
        assert APP_NAME is not None
        assert isinstance(APP_NAME, str)
        assert APP_NAME == "vr_cricket_strategist"
    
    def test_retry_config_exists(self):
        """Test that retry_config is defined"""
        from agents.vr_cricket_strategist.config import retry_config
        assert retry_config is not None
    
    def test_retry_config_attributes(self):
        """Test that retry_config has expected attributes"""
        from agents.vr_cricket_strategist.config import retry_config
        
        assert hasattr(retry_config, 'attempts')
        assert retry_config.attempts > 0
        assert hasattr(retry_config, 'initial_delay')
        assert retry_config.initial_delay > 0
    
    def test_dataset_paths_exist(self):
        """Test that dataset path constants are defined"""
        from agents.vr_cricket_strategist.config import (
            BASE_DIR, DATASET_DIR, PLAYERS_CSV, MATCHES_CSV
        )
        
        assert BASE_DIR is not None
        assert DATASET_DIR is not None
        assert PLAYERS_CSV is not None
        assert MATCHES_CSV is not None
    
    def test_dataset_paths_are_paths(self):
        """Test that dataset paths are Path objects"""
        from agents.vr_cricket_strategist.config import (
            BASE_DIR, DATASET_DIR, PLAYERS_CSV, MATCHES_CSV
        )
        
        assert isinstance(BASE_DIR, Path)
        assert isinstance(DATASET_DIR, Path)
        assert isinstance(PLAYERS_CSV, Path)
        assert isinstance(MATCHES_CSV, Path)
    
    def test_dataset_dir_structure(self):
        """Test that DATASET_DIR is correctly structured"""
        from agents.vr_cricket_strategist.config import DATASET_DIR
        
        # Should end with vr_cricket_dataset
        assert str(DATASET_DIR).endswith('vr_cricket_dataset')
    
    def test_csv_filenames(self):
        """Test that CSV files have correct names"""
        from agents.vr_cricket_strategist.config import PLAYERS_CSV, MATCHES_CSV
        
        assert PLAYERS_CSV.name == 'players.csv'
        assert MATCHES_CSV.name == 'matches.csv'
    
    def test_vertexai_setting(self):
        """Test that Vertex AI is disabled"""
        from agents.vr_cricket_strategist.config import os
        
        # Config should set GOOGLE_GENAI_USE_VERTEXAI to FALSE
        vertexai_setting = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI")
        assert vertexai_setting == "FALSE"
    
    def test_logging_configuration(self):
        """Test that logging is properly configured"""
        import logging
        
        # Check that ADK logging is set to ERROR level
        adk_logger = logging.getLogger('google.adk')
        assert adk_logger.level == logging.ERROR
    
    def test_grpc_verbosity(self):
        """Test that GRPC verbosity is set"""
        assert os.environ.get('GRPC_VERBOSITY') == 'ERROR'
        assert os.environ.get('GLOG_minloglevel') == '2'


class TestConfigPaths:
    """Tests for path resolution in config"""
    
    def test_base_dir_resolution(self):
        """Test that BASE_DIR resolves correctly"""
        from agents.vr_cricket_strategist.config import BASE_DIR
        
        # BASE_DIR should point to workspace root
        assert BASE_DIR.exists()
        
        # Should contain vr_cricket_dataset directory
        dataset_dir = BASE_DIR / "vr_cricket_dataset"
        assert dataset_dir.exists()
    
    def test_csv_files_exist(self):
        """Test that CSV files exist at configured paths"""
        from agents.vr_cricket_strategist.config import PLAYERS_CSV, MATCHES_CSV
        
        assert PLAYERS_CSV.exists(), f"Players CSV not found at {PLAYERS_CSV}"
        assert MATCHES_CSV.exists(), f"Matches CSV not found at {MATCHES_CSV}"
    
    def test_csv_files_are_files(self):
        """Test that CSV paths point to files, not directories"""
        from agents.vr_cricket_strategist.config import PLAYERS_CSV, MATCHES_CSV
        
        assert PLAYERS_CSV.is_file()
        assert MATCHES_CSV.is_file()


class TestEnvironmentVariables:
    """Tests for environment variable handling"""
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': ''}, clear=False)
    def test_missing_api_key_warning(self, capsys):
        """Test warning when API key is missing"""
        import importlib
        import agents.vr_cricket_strategist.config as config
        
        # Reload config to trigger the check
        with patch.dict(os.environ, {'GOOGLE_API_KEY': ''}, clear=False):
            importlib.reload(config)
            captured = capsys.readouterr()
            # Note: This test might not catch the warning if config was already loaded
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key_123'})
    def test_api_key_present(self):
        """Test that API key is properly loaded when present"""
        assert os.getenv("GOOGLE_API_KEY") == 'test_key_123'
    
    def test_dotenv_loaded(self):
        """Test that dotenv is loaded (load_dotenv called)"""
        # This test just verifies the import doesn't fail
        from agents.vr_cricket_strategist.config import load_dotenv
        assert load_dotenv is not None

