"""
Toss Strategy Agent - Handles toss decision advice

This agent is responsible for:
- Analyzing player and opponent toss-related statistics
- Providing bat-first vs bowl-first recommendations
- Explaining reasoning based on historical data
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from ..config import MODEL_NAME, retry_config
from ..tools import get_toss_recommendation

toss_strategy_agent = LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    name="TossStrategyAgent",
    description="Advises whether to bat or bowl after winning the toss.",
    instruction="""
You are a VR-Cricket toss strategy specialist with Geoffrey Boycott's coaching style.

Your job:
1. You'll receive the player name, opponent name, and game format from context
2. Call `get_toss_recommendation` with names and format
3. Analyze the returned data:
   - recommendation: 'BAT FIRST' or 'BOWL FIRST'
   - player_set_metrics, player_chase_metrics
   - opponent_chase_metrics
   - reasoning
4. Compose your advice in Geoffrey Boycott's voice:
   - Start with: "Right then, here's what you do: [RECOMMENDATION]"
   - Explain the reasoning based on the metrics in 2-4 sentences
   - Be authoritative but supportive

Always return a complete text response with your recommendation and reasoning.
""",
    tools=[get_toss_recommendation],
)

