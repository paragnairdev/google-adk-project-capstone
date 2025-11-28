#!/bin/bash
# VR Cricket Strategist - Web UI Launcher Script
# This script activates the virtual environment and starts the web UI

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "========================================"
echo "🏏 VR Cricket Strategist - Web UI"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found!${NC}"
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
else
    # Activate virtual environment
    echo -e "${GREEN}✓${NC} Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    echo "Please create a .env file with your GOOGLE_API_KEY"
    echo "Example: echo 'GOOGLE_API_KEY=your-key-here' > .env"
    exit 1
fi

# Start the web UI
echo -e "${GREEN}✓${NC} Starting web UI..."
echo ""
echo -e "${BLUE}Web UI will be available at: http://localhost:8000${NC}"
echo -e "${BLUE}Server logs will be written to: server.log${NC}"
echo -e "${BLUE}Session database: cricket_strategist_sessions.db${NC}"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the ADK web command with session persistence
adk web agents --log_level DEBUG --port 8000 --host 0.0.0.0 --session_service_uri "sqlite:///cricket_strategist_sessions.db" > server.log 2>&1

