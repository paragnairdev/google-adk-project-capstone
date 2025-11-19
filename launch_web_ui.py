"""
VR Cricket Coach - Web UI Launcher

This script launches the ADK web interface for the VR Cricket Coach agent,
providing a modern chat-like interface for interacting with the agent.

Usage:
    python launch_web_ui.py

The web UI will be available at http://localhost:8000
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key is set
if not os.getenv("GOOGLE_API_KEY"):
    print("⚠️  ERROR: GOOGLE_API_KEY not found in environment!")
    print("Please set it in .env file or export GOOGLE_API_KEY=your-key")
    print("Get your API key from: https://aistudio.google.com/app/apikey")
    sys.exit(1)

# Ensure Gemini API (not Vertex AI) is used
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

print("\n" + "="*80)
print("🏏 VR CRICKET COACH - WEB UI")
print("="*80)
print("\nStarting web interface...")
print("The web UI will be available at: http://localhost:8000")
print("\nPress Ctrl+C to stop the server\n")
print("="*80 + "\n")

# Get the agents directory path
agents_dir = Path(__file__).parent / "agents"

# Use ADK CLI to start the web UI
if __name__ == "__main__":
    try:
        subprocess.run(
            [
                "adk", "web",
                str(agents_dir),
                "--port", "8000",
                "--host", "0.0.0.0",
            ],
            check=True,
            env=os.environ.copy()
        )
    except KeyboardInterrupt:
        print("\n\n👋 Web UI stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting web UI: {e}")
        sys.exit(1)

