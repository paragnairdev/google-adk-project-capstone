"""
Configuration Module for VR Cricket Strategist

This module centralizes all configuration, environment setup, and logging.

Design Decisions:
- Single source of truth for all paths and settings
- Environment validation at startup (fail fast)
- Automatic log cleanup to prevent disk space issues
- Configured for Gemini API (not Vertex AI) for simpler authentication

Logging Strategy:
- Application logs: logger.log (DEBUG level for troubleshooting)
- ADK logs: Suppressed (ERROR only) to reduce noise
- Web UI logs: Separate files for clean separation
"""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from google.genai import types

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================
# Load API keys and credentials from .env file
load_dotenv()

# Clean up previous log files to prevent clutter
# This runs on each application start to ensure fresh logs
for log_file in ["logger.log", "web.log", "tunnel.log"]:
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleaned up {log_file}")

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
# Suppress verbose ADK/gRPC logs (only show errors)
# Design Decision: ADK generates excessive INFO logs that clutter debugging
logging.getLogger('google.adk').setLevel(logging.ERROR)
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

# Configure application logging with DEBUG level for comprehensive troubleshooting
logging.basicConfig(
    filename="logger.log",
    level=logging.DEBUG,
    format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
)

# ============================================================================
# API AUTHENTICATION VALIDATION
# ============================================================================
# Verify API key is configured before agent initialization
# This prevents cryptic errors during agent invocation
if not os.getenv("GOOGLE_API_KEY"):
    print("⚠️  WARNING: GOOGLE_API_KEY not found in environment!")
    print("Please set it in .env file or export GOOGLE_API_KEY=your-key")
    print("Get your API key from: https://aistudio.google.com/app/apikey")

# Force usage of Gemini API instead of Vertex AI
# Design Decision: Gemini API is simpler for prototyping (no GCP project required)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
MODEL_NAME = "gemini-2.0-flash-lite"  # Fast, cost-effective model for real-time responses
APP_NAME = "vr_cricket_strategist"

# ============================================================================
# DATASET PATHS
# ============================================================================
# Calculate paths relative to this file's location
# Structure: agents/vr_cricket_strategist/config.py -> workspace_root/vr_cricket_dataset/
BASE_DIR = Path(__file__).parent.parent.parent  # Navigate up to workspace root
DATASET_DIR = BASE_DIR / "vr_cricket_dataset"
PLAYERS_CSV = DATASET_DIR / "players.csv"
MATCHES_CSV = DATASET_DIR / "matches.csv"

# ============================================================================
# RELIABILITY CONFIGURATION
# ============================================================================
# Exponential backoff retry configuration for API resilience
# Design Decision: Aggressive retries (5 attempts) ensure reliability during
# rate limiting or transient API failures
retry_config = types.HttpRetryOptions(
    attempts=5,              # Maximum retry attempts
    exp_base=7,              # Exponential backoff base (7^n seconds)
    initial_delay=1,         # Start with 1 second delay
    http_status_codes=[      # Retry on these status codes
        429,  # Rate limit exceeded
        500,  # Internal server error
        503,  # Service unavailable
        504,  # Gateway timeout
    ],
)
