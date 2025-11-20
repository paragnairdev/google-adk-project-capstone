# Quick Start Guide - VR Cricket Strategist

## Installation

1. **Activate the virtual environment:**
   ```bash
   cd /Users/parag.nair/Documents/github/learning/google-adk
   source venv/bin/activate
   ```

2. **Verify installation:**
   ```bash
   pip list | grep google-adk
   ```
   You should see `google-adk` version 1.18.0 or higher.

## Google Cloud Setup

Before running the agent, you need to authenticate with Google Cloud:

### Option 1: Using API Key (Easiest)

1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a `.env` file in the project root:
   ```bash
   echo "GOOGLE_API_KEY=your-api-key-here" > .env
   ```

### Option 2: Using Service Account

1. Create a Google Cloud project
2. Enable Vertex AI API
3. Create a service account and download credentials
4. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   ```

## Running the Agent

### Demo Mode (Recommended for First Run)

Run predefined test queries:
```bash
python -m agents.vr_cricket_strategist.agent
```

This will demonstrate:
- Pitch condition analysis
- Death overs bowling strategy
- DLS calculation for rain-affected matches

### Running Tests

Run the test suite:
```bash
pytest agents/vr_cricket_strategist/tests/
```

Run tests with coverage:
```bash
pytest agents/vr_cricket_strategist/tests/ --cov=agents/vr_cricket_strategist --cov-report=html
```

Then ask questions like:
```
You: What bowling attack should I use on a bouncy pitch?
You: We need 78 runs in 10 overs with 7 wickets in hand. What's our strategy?
You: Who are the best death bowlers in IPL 2024?
```

Type `exit` or `quit` to end the session.

## Sample Queries

### Strategy Questions
- "We won the toss on a green pitch in overcast conditions. Should we bat or bowl?"
- "How should we approach the powerplay while chasing 180 in a T20?"

### Tactical Questions
- "Suggest a field placement for Jasprit Bumrah bowling to Jos Buttler in death overs"
- "What bowling changes should we make at the 35-over mark in an ODI?"

### Analysis Questions
- "Analyze the pitch conditions at Wankhede Stadium for T20 cricket"
- "Calculate the revised target if we lose 5 overs in rain, currently at 120/2 in 20 overs"

### Current Events (Uses Google Search)
- "What's the latest news about India's pace attack?"
- "Who won the last IPL and what was their winning strategy?"
- "What's the current form of Pat Cummins in Test cricket?"

## Troubleshooting

### "API key not found"
- Make sure you've set `GOOGLE_API_KEY` in `.env` or as environment variable
- Or set `GOOGLE_APPLICATION_CREDENTIALS` for service account

### "Module not found: google.adk"
- Ensure virtual environment is activated: `source venv/bin/activate`
- Reinstall if needed: `pip install google-adk`

### "Rate limit exceeded"
- The agent has retry logic built-in
- Wait a few moments and try again
- Check your Google Cloud quotas

## Next Steps

1. Modify the custom tools in `agents/vr_cricket_strategist/tools.py`
2. Add more cricket-specific functions (e.g., run rate calculators, player statistics)
3. Integrate with cricket APIs for real-time match data
4. Extend the test suite with more scenarios
5. Add multi-agent workflows (e.g., separate agents for batting, bowling, fielding strategies)

## Tips

- The agent works best with specific, detailed questions
- Provide context (format, situation, conditions) for better recommendations
- The agent can search for current cricket news and stats using Google Search
- Custom tools provide tactical calculations without internet dependency

Happy strategizing! 🏏

