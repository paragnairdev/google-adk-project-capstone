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

# --- AGENT 4: STAT ANALYST (The Reporter) ---
# Role: Handles specific data lookups (Stadiums, Stats, Trends)
stat_analyst = LlmAgent(
    name="StatAnalyst",
    model=model_config,
    instruction="""
    You are the Team Data Analyst.
    Your job is to query the database and report raw numbers accurately.
    
    TOOLS & RULES:
    1. Use `get_venue_trends` for stadium or pitch info.
    2. **IMPORTANT:** The tool `get_venue_trends` requires a 'format'.
    3. Use `get_head_to_head` for head-to-head records.
    4. **IMPORTANT:** The tool `get_head_to_head` requires a 'player_name', 'opponent_name' & 'format'.
       - Pass `stadium=7` (as an integer) to the tool.
    
    OUTPUT FORMAT:
    - Present data in a clean bulleted list or small table.
    - Do NOT give advice (that is the Coach's job). Just give the numbers.
    """,
    tools=[get_venue_trends, get_head_to_head] 
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
    
    ### PHASE 1: IDENTITY
    - ALWAYS call `get_current_identity` first.

    ### PHASE 2: ROUTING
    Classify the user's intent and route to the correct specialist:
    
    1. **Strategy / Advice / "What should I do?"**:
       - Delegate to `GamePlanGenerator`.
       
    2. **Specific Stats / "Show me data" / "Stadium Info"**:
       - Delegate to `StatAnalyst`. <--- NEW PATH
       
    3. **Chit-Chat**:
       - Handle greetings yourself.
    """,
    tools=[get_current_identity],
    # 🚀 REGISTER THE NEW AGENT HERE
    sub_agents=[game_plan_generator, stat_analyst] 
)