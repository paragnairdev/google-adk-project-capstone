import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from google.genai import types

# Load environment variables
load_dotenv()

# Suppress ADK informational messages
logging.getLogger('google.adk').setLevel(logging.ERROR)
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

# Verify API key is set
if not os.getenv("GOOGLE_API_KEY"):
    print("⚠️  WARNING: GOOGLE_API_KEY not found in environment!")
    print("Please set it in .env file or export GOOGLE_API_KEY=your-key")
    print("Get your API key from: https://aistudio.google.com/app/apikey")

# Ensure Gemini API (not Vertex AI) is used
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

# Configuration
MODEL_NAME = "gemini-2.0-flash-lite"
APP_NAME = "vr_cricket_strategist"

# Dataset paths - go up to the workspace root
# Assuming this file is in agents/vr_cricket_strategist/
BASE_DIR = Path(__file__).parent.parent.parent
DATASET_DIR = BASE_DIR / "vr_cricket_dataset"
PLAYERS_CSV = DATASET_DIR / "players.csv"
MATCHES_CSV = DATASET_DIR / "matches.csv"

# Retry config for reliability
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)
