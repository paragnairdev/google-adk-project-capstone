# Google ADK Learning Projects

This repository contains examples and custom agents built with Google's Agent Development Kit (ADK).

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install google-adk
```

3. Set up Google Cloud credentials (required for ADK):
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
# OR
export GOOGLE_API_KEY="your-api-key"
```

## Projects

### VR Cricket Strategist 🏏

**Location:** `agents/vr_cricket_strategist/`

A sophisticated cricket strategy assistant that provides tactical advice for various game situations.

**Features:**
- ✅ Data-driven analysis using CSV match history
- ✅ Strategic advice for Test, ODI, and T20 formats
- ✅ Comprehensive test suite with pytest

**Data Requirements:**
- `vr_cricket_dataset/players.csv` - Player profiles
- `vr_cricket_dataset/matches.csv` - Match history

**Usage:**

Launch web UI for interactive testing:
```bash
./launch_web_ui.sh
# Or: python launch_web_ui.py
```
Then open http://localhost:8000

Run demo mode with predefined queries:
```bash
python -m agents.vr_cricket_strategist.agent
```

Run tests:
```bash
pytest agents/vr_cricket_strategist/tests/
```

**Example Queries:**
- "We're playing on a green pitch with overcast conditions. What should be our strategy?"
- "It's the death overs in a T20. The opposition needs 45 runs from 24 balls. What bowling changes should we use?"
- "Analyze a dusty pitch in humid conditions for a Test match"
- "What's a safe target when batting first on a flat pitch?"

**Custom Tools:**
1. `analyze_pitch_conditions()` - Analyzes pitch and weather for strategic recommendations
2. `calculate_dls_target()` - Calculates revised targets for rain-affected matches
3. `suggest_bowling_changes()` - Recommends bowling rotations based on match situation
4. `get_match_stats()` - Retrieves historical match data for analysis

## Examples Directory

The `examples/` directory contains various ADK patterns:
- Basic agent creation
- Multi-agent workflows
- Sequential and parallel agent patterns
- Loop workflows with refinement
- Custom tool integration
- MCP (Model Context Protocol) integration
- Agent memory and sessions

## Resources

- [Google ADK Documentation](https://cloud.google.com/vertex-ai/docs/agent-development-kit)
- [Google ADK GitHub](https://github.com/google/adk)
- [Gemini API](https://ai.google.dev/)

## License

MIT

