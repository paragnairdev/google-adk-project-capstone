"""
Intent Router Agent - Classifies user requests

This agent is responsible for:
- Analyzing user messages
- Classifying intent (toss_decision, safe_target, unsupported)
- Extracting game format if mentioned
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

from ..config import MODEL_NAME, retry_config

intent_agent = LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    name="IntentRouter",
    description="Classifies what strategy question the user is asking.",
    instruction="""
You classify the user's latest request into one of three intents:

- toss_decision : They won the toss and need to decide whether to bat or bowl first
- safe_target   : They are batting first and need to know what's a safe target score
- unsupported   : Anything else

Analyze the user's message and return a string in this format:
"intent game_format"

Examples:
"toss_decision T20"
"safe_target ODI"
"toss_decision" (if format not specified)
"unsupported"

Valid intents: toss_decision, safe_target, unsupported
Valid formats: T20, ODI, Test

Return ONLY the string.
""",
)

