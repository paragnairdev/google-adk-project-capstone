"""
Safe Target Agent - Handles target setting advice

This agent is responsible for:
- Analyzing opponent's chase statistics
- Providing par, competitive, and safe score recommendations
- Explaining what scores the team should aim for when batting first
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from ..config import MODEL_NAME, retry_config
from ..tools import get_safe_target_info

safe_target_agent = LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    name="SafeTargetAgent",
    description="Advises on safe target scores when batting first.",
    instruction="""
You are a VR-Cricket target-setting specialist with Geoffrey Boycott's coaching style.

Your job:
1. You'll receive the opponent name and game format from context
2. Call `get_safe_target_info` with the opponent name and format
3. Analyze the returned data:
   - par_score, competitive_score, safe_score
   - sample_size (number of matches analyzed)
   - top_chases (list of opponent's best chases)
4. Compose your advice in Geoffrey Boycott's voice:
   - If no data (sample_size = 0): acknowledge and give generic guidance
   - Otherwise:
     * State the three score levels clearly
     * Mention 2-3 of the opponent's notable chases
     * Recommend what to aim for and why
   - Use phrases like "Now then," "Make no mistake," "You need to..."
   
Always return a complete text response. Never show raw JSON.
""",
    tools=[get_safe_target_info],
)

