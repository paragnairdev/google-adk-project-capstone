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

### 1. VR Cricket Coach 🏏 (Data-Driven Multi-Agent System)

**File:** `vr_cricket_coach.py`

A sophisticated multi-agent cricket strategy assistant that uses real match data to provide personalized recommendations.

**🌐 Web UI Now Available!** Launch with `./launch_web_ui.sh` for a modern chat interface at http://localhost:8000

> **Note:** Web UI requires the `agents/` directory structure. See [README_WEB_UI.md](README_WEB_UI.md) for details.

**Architecture:**
- **Identity Agent**: Manages player onboarding and identity across sessions
- **Intent Router**: Classifies user questions (toss_decision, safe_target, unsupported)
- **Toss Strategy Agent**: Provides data-backed toss recommendations
- **Root Agent**: Orchestrates all sub-agents with Geoffrey Boycott's personality

**Features:**
- ✅ Data-driven analysis using CSV match history
- ✅ Multi-agent orchestration with intent routing
- ✅ Session management with automatic memory persistence
- ✅ Player identity tracking across conversations
- ✅ Percentile-based safe target calculations
- ✅ Historical performance vs specific opponents

**Data Requirements:**
- `vr_cricket_dataset/players.csv` - Player profiles
- `vr_cricket_dataset/matches.csv` - Match history

**Usage:**

Run demo mode (shows multi-session examples):
```bash
python vr_cricket_coach.py
```

Run interactive mode (terminal):
```bash
python vr_cricket_coach.py --interactive
```

Run web UI (chatbot interface):
```bash
./launch_web_ui.sh
# Or directly:
python launch_web_ui.py
```

The web UI will be available at `http://localhost:8000` with a modern chat interface.

**Example Queries:**
- "Hi, I'm Karthik" → Identity onboarding
- "Should I bat or bowl against Sid if I win the toss?" → Toss recommendation
- "What's a safe target against Ragz when batting first?" → Safe target analysis
- Session memory automatically persists context

**Custom Tools:**
1. `save_player_identity()` / `get_player_identity()` - Session state management
2. `get_brief_stats()` - Player statistics summary
3. `get_toss_recommendation()` - Bat/bowl decision based on historical data
4. `get_safe_target_info()` - Percentile-based target calculations with top chases

---

### 2. VR Cricket Strategist 🏏 (General Purpose)

**File:** `vr_cricket_strategist.py`

A general-purpose cricket strategy assistant for tactical advice without requiring data files.

**Features:**
- Pitch condition analysis with weather considerations
- Bowling change recommendations for different match phases
- Simplified DLS calculations for rain-affected matches
- Real-time cricket news and player form via Google Search
- Strategic advice for Test, ODI, and T20 formats

**Usage:**

Run demo mode with predefined queries:
```bash
python vr_cricket_strategist.py
```

Run interactive mode:
```bash
python vr_cricket_strategist.py --interactive
```

**Example Queries:**
- "We're playing on a green pitch with overcast conditions. What should be our strategy?"
- "It's the death overs in a T20. The opposition needs 45 runs from 24 balls. What bowling changes should we use?"
- "Analyze a dusty pitch in humid conditions for a Test match"
- "What's the current form of Virat Kohli in T20 cricket?"

**Custom Tools:**
1. `analyze_pitch_conditions()` - Analyzes pitch and weather for strategic recommendations
2. `calculate_dls_target()` - Calculates revised targets for rain-affected matches
3. `suggest_bowling_changes()` - Recommends bowling rotations based on match situation
4. `google_search` - Fetches current cricket news and player statistics

---

### Which Agent Should You Use?

| Feature | VR Cricket Coach | VR Cricket Strategist |
|---------|------------------|----------------------|
| **Data Required** | Yes (CSV files) | No |
| **Personalization** | Player-specific insights | General advice |
| **Multi-Agent** | Yes (4 agents) | No (single agent) |
| **Memory** | Automatic session memory | Stateless |
| **Toss Decisions** | Data-backed recommendations | Rule-based |
| **Safe Targets** | Opponent-specific percentiles | General guidelines |
| **Best For** | Regular players with history | General strategy, pitch analysis |

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

