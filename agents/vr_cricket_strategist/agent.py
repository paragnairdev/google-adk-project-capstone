# agents/root.py
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini

# Import tools
from .tools import get_current_identity, get_head_to_head, get_venue_trends
from .config import retry_config

# Common Model Config
model_config = Gemini(model="gemini-2.5-flash", retry_options=retry_config)

# --- AGENT 1: FACT FINDER (The Intern) ---
# Role: Fetches raw data only. No opinions.
fact_finder = LlmAgent(
    name="FactFinder",
    model=model_config,
    instruction="""
    You are a data retrieval specialist.
    1. Identify the pitch type, opponent, and format from the conversation history.
    2. Call `get_head_to_head` to see the record against this opponent.
    3. Call `get_venue_trends` to see pitch behavior.
    4. Output ONLY the raw data summaries. Do not give advice.
    """,
    tools=[get_head_to_head, get_venue_trends]
)

# --- AGENT 2: TACTICIAN (The Brain) ---
# Role: Analyzes the data from FactFinder and decides on a strategy.
tactician = LlmAgent(
    name="Tactician",
    model=model_config,
    instruction="""
    You are a senior cricket analyst.
    Review the data provided by the FactFinder in the context.
    
    DECISION LOGIC:
    - If user loses chasing > 60% of the time -> Recommend Batting First.
    - If pitch is 'Green' or 'Overcast' -> Recommend Bowling First (unless weak at chasing).
    - If opponent is 'Wizheart' (strong player) -> Recommend conservative target setting.
    
    Output a structured strategic plan. Be logical and cold.
    """
)

# --- AGENT 3: BOYCOTT WRITER (The Voice) ---
# Role: Translates the strategy into the persona.
boycott_writer = LlmAgent(
    name="BoycottWriter",
    model=model_config,
    instruction="""
    You are Geoffrey Boycott.
    Take the strategy provided by the Tactician and tell the player what to do.
    - Use phrases like "rubbish bowling", "stick of rhubarb", "roti capability".
    - Be direct and slightly critical but helpful.
    - Address the player by their name (check the conversation context or tool outputs for the name).
    """
)

# --- WRAPPING IT UP: THE SEQUENTIAL AGENT ---
game_plan_generator = SequentialAgent(
    name="GamePlanGenerator",
    description="Generates a detailed match strategy using data analysis.",
    sub_agents=[fact_finder, tactician, boycott_writer]
)

# --- THE ROOT AGENT ---
root_agent = LlmAgent(
    name="CricketCoachOrchestrator",
    model=model_config,
    instruction="""
    You are the VR Cricket Coach Interface.
    
    ### PHASE 1: IDENTITY CHECK (CRITICAL)
    - ALWAYS start every turn by looking for the user's identity.
    - Call `get_current_identity` immediately if you haven't already.
    - If the tool returns "Auto-logged in", inform the user you've loaded their profile.

    ### PHASE 2: ROUTING
    Once identity is established, route the user's request to the correct specialist:
    
    1. **Strategy / Toss / Game Plans**:
       - Delegate to `GamePlanGenerator`.
    
    2. **Chit-Chat**:
       - Handle greetings yourself. 
       - IMPORTANT: Address the user by their name ONLY IF you have successfully retrieved it from the identity tool.
       - If you don't know the name yet, just say "Player".
    """,
    # REMOVED: The direct usage of "{player_name}" in the string above.
    # REASON: It prevents the crash on the first turn.
    
    tools=[get_current_identity],
    sub_agents=[game_plan_generator] 
)