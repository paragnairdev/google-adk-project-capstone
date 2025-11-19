# VR Cricket Coach - Complete Guide

## Overview

The **VR Cricket Coach** is a sophisticated multi-agent system adapted from your Kaggle notebook to run locally. It provides data-driven cricket strategy recommendations based on actual match history.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Root Agent                               │
│              (Orchestrator with Geoffrey Boycott personality)    │
└─────────────────┬───────────────────────────────────────────────┘
                  │
      ┌───────────┴────────────┬──────────────┬──────────────────┐
      │                        │              │                  │
┌─────▼─────┐          ┌──────▼──────┐  ┌───▼──────────┐  ┌────▼────────┐
│ Identity  │          │   Intent    │  │    Toss      │  │   Tools     │
│   Agent   │          │   Router    │  │   Strategy   │  │ & Memory    │
└───────────┘          └─────────────┘  │    Agent     │  └─────────────┘
                                        └──────────────┘
```

### Agent Roles

1. **Identity Agent**
   - Manages player onboarding
   - Tracks player identity in session state
   - Provides brief stats summary

2. **Intent Router**
   - Classifies user questions into:
     - `toss_decision`: Bat or bowl after winning toss?
     - `safe_target`: What score to set when batting first?
     - `unsupported`: Anything else

3. **Toss Strategy Agent**
   - Analyzes player's batting/bowling performance
   - Compares opponent's chasing ability
   - Provides data-backed recommendations

4. **Root Agent (Orchestrator)**
   - Coordinates all sub-agents
   - Handles conversation flow
   - Manages memory and session state
   - Responds with Geoffrey Boycott's personality

## Key Differences from Kaggle Version

| Aspect | Kaggle Version | Local Version |
|--------|----------------|---------------|
| **Imports** | `kaggle_secrets`, `IPython` | `python-dotenv` |
| **API Key** | Kaggle secrets | `.env` file or environment |
| **Paths** | `/kaggle/input/...` | `./vr_cricket_dataset/` |
| **Execution** | Jupyter notebook cells | Command-line Python script |
| **Output** | Notebook cells | Terminal with clean formatting |
| **Magic Commands** | `%%writefile`, `!adk` | Pure Python |

## Data Schema

### players.csv
```csv
player_id,player_name,batting_style,preferred_format,skill_rating,aggression,consistency
1,Wizheart,Anchor,Test,88,0.78,0.41
```

### matches.csv
```csv
match_id,date,format,pitch_type,difficulty,innings_number,player_name,opponent_name,
runs,overs,wickets,is_chasing,result,hundreds,...
```

## Usage

### Demo Mode (Recommended First Run)

Shows 3 different scenarios with multiple agents and session memory:

```bash
python vr_cricket_coach.py
```

**Demo scenarios:**
1. Karthik vs Sid - Toss decision
2. Wizheart vs Ragz - Safe target
3. Wizheart continuation - Memory recall

### Interactive Mode

Have a real conversation with the coach:

```bash
python vr_cricket_coach.py --interactive
```

## Example Conversations

### Session 1: First-time user

```
You: Hi there
Coach: Hello! Who am I talking to (player name)?

You: I'm Karthik
Coach: Welcome, Karthik! Here are your brief stats...
       Karthik has played 156 innings.
       - Average runs: 89.45
       - Average run rate: 5.23 runs/over
       - Average runs per wicket: 21.34

You: Should I bat or bowl against Sid if I win the toss?
Coach: Recommendation: BAT FIRST
       
       You average 92.3 when setting a target and 85.1 when chasing.
       Meanwhile, Sid averages only 78.4 when chasing against you.
       Given your superior batting-first record and Sid's weaker 
       chasing performance, I'd advise putting runs on the board.
```

### Session 2: Safe target query

```
You: I'm Wizheart
Coach: Welcome back, Wizheart! Your stats show...

You: What's a safe target against Ragz when batting first?
Coach: Based on Ragz's chasing history (42 innings):
       
       Par score: ~125
       Competitive score: ~142
       Safe score: ~165
       
       Notable chases by Ragz:
       • 198 runs off 20 overs (2024-07-15, T20, Bouncy, Insane)
       • 187 runs off 18.5 overs (2024-08-03, T20, Flat, Ultra Insane)
       • 176 runs off 19 overs (2024-06-22, T20, Dry, Insane)
       
       Right then, you'll want to aim for at least 165 to have a 
       comfortable cushion. Ragz has shown he can chase big totals 
       on good pitches, so don't be conservative—proper batting, 
       proper runs on the board.
```

### Session 3: Multi-turn with memory

```
You: What about against Zafi?
Coach: [Remembers you're Wizheart from earlier in session]
       
       Against Zafi (23 chasing innings):
       Par: ~110, Competitive: ~128, Safe: ~145
       
       Zafi isn't quite the chaser that Ragz is...
```

## Features Explained

### 1. Session State Management

Player identity is stored in session state:
```python
tool_context.state["user:player_name"] = player_name
```

This allows the agent to remember who you are across multiple questions in the same session.

### 2. Automatic Memory Persistence

After each turn, the session is saved to memory:
```python
async def auto_save_to_memory(callback_context):
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )
```

### 3. Intent-Based Routing

The Intent Router classifies questions and routes them to appropriate agents:
- "Should I bat or bowl?" → `toss_decision` → Toss Strategy Agent
- "What's a safe target?" → `safe_target` → Safe Target calculation
- "Tell me about pitch" → `unsupported` → Polite explanation

### 4. Data-Driven Recommendations

**Toss Decision Logic:**
```python
if (player_better_at_setting AND opponent_weak_at_chasing):
    recommendation = "BAT FIRST"
else:
    recommendation = "BOWL FIRST"
```

**Safe Target Calculation:**
```python
par_score = 50th percentile of opponent's chases
competitive = 60th percentile
safe = 75th percentile + 5 run buffer
```

### 5. Agent Tool Wrapping

Sub-agents are wrapped as tools for the root agent:
```python
identity_tool = AgentTool(identity_agent)
intent_tool = AgentTool(intent_agent)
toss_tool = AgentTool(toss_strategy_agent)
```

This allows agents to call other agents as if they were functions.

## Extending the Agent

### Adding New Intents

1. Update the Intent Router's instruction to recognize new intent
2. Create a specialized agent for that intent (optional)
3. Add handling logic in Root Agent's instruction
4. Add any required tools

Example: Adding "fielding_positions" intent:

```python
fielding_agent = LlmAgent(
    name="FieldingAgent",
    instruction="Suggest field placements based on match situation...",
    tools=[get_fielding_setup],
    output_key="fielding_advice",
)

# Add to root agent
root_agent = LlmAgent(
    ...
    tools=[..., AgentTool(fielding_agent), get_fielding_setup],
)
```

### Adding New Data Sources

```python
# Load additional data
weather_df = pd.read_csv(DATASET_DIR / "weather.csv")

# Create new tool
def get_weather_impact(date: str, venue: str) -> Dict[str, Any]:
    weather = weather_df[
        (weather_df["date"] == date) & 
        (weather_df["venue"] == venue)
    ]
    return {"temperature": ..., "humidity": ..., "recommendation": ...}

# Add to relevant agent
toss_strategy_agent = LlmAgent(
    ...
    tools=[get_toss_recommendation, get_weather_impact],
)
```

## Troubleshooting

### "No module named 'pandas'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "GOOGLE_API_KEY not found"
```bash
echo "GOOGLE_API_KEY=your-key-here" > .env
```

### "Could not find dataset files"
Ensure directory structure:
```
google-adk/
├── vr_cricket_coach.py
└── vr_cricket_dataset/
    ├── players.csv
    └── matches.csv
```

### Agent gives wrong player stats
Check that player names match exactly (case-sensitive):
```python
matches_df["player_name"].unique()
```

### Session not remembering context
Make sure you're using the same `session_id` across calls:
```python
await run_session(queries, session_name="same_session_name")
```

## Performance Tips

1. **Use descriptive session names** for easier debugging
2. **Keep queries specific** - mention opponent names explicitly
3. **Let identity flow naturally** - don't repeat "I'm X" every time
4. **Memory accumulates** - long sessions have more context

## Comparison with VR Cricket Strategist

| Feature | Coach (Data-Driven) | Strategist (General) |
|---------|--------------------|--------------------|
| **Input** | Historical match CSVs | No data required |
| **Recommendations** | Personalized to player | Generic best practices |
| **Agents** | 4 (orchestrated) | 1 (standalone) |
| **Memory** | Session + long-term | Stateless |
| **Best for** | Regular players | One-off strategy questions |
| **Toss advice** | Stats-based | Pitch/conditions-based |
| **Targets** | Opponent-specific | DLS calculations |

## Next Steps

1. ✅ Test with demo mode
2. ✅ Try interactive mode
3. 🔄 Add your own match data to CSVs
4. 🔄 Create new intents (bowling changes, fielding, etc.)
5. 🔄 Deploy with FastAPI web interface
6. 🔄 Integrate with live cricket APIs

## Code Structure

```
vr_cricket_coach.py
├── Imports & Config (lines 1-55)
├── Data Loading (lines 57-70)
├── Data Functions (lines 75-170)
├── Tool Functions (lines 175-250)
├── Agent Definitions (lines 255-430)
├── Memory Callback (lines 433-437)
├── Runner Setup (lines 442-450)
├── Session Helper (lines 453-495)
└── Main Execution (lines 500-600)
```

---

**Built with Google ADK • Adapted from Kaggle • Ready for Production** 🏏

