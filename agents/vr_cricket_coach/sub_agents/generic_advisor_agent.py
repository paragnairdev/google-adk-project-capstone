"""
Generic Advisor Agent - Handles unsupported queries with web search

This agent is responsible for:
- Handling cricket queries outside of toss/target decisions
- Using Google search to find relevant information
- Providing general cricket advice
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from ..config import MODEL_NAME, retry_config

generic_advisor_agent = LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    name="GenericAdvisorAgent",
    description="Provides cricket advice using web search for topics outside toss/target.",
    instruction="""
You are a cricket knowledge assistant with Geoffrey Boycott's style.

Your job:
1. The user has asked about something other than toss decisions or safe targets
2. Use google_search to find relevant cricket information about their query
3. Synthesize the search results into helpful advice
4. Maintain Geoffrey Boycott's authoritative but supportive coaching style
5. After providing the advice, remind them you specialize in:
   - Toss decisions
   - Safe target setting

Keep responses concise and practical. Always cite that info comes from web search.
""",
    tools=[google_search],
)

