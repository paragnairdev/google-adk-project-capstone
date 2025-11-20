import random
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini

# Import tools
from .tools import get_current_identity, get_head_to_head, get_venue_trends, pick_random_commentator
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

# --- AGENT 3: (The Voice) ---
# Role: Translates the strategy into the persona.
# Writer 1: Geoffrey Boycott
boycott_writer = LlmAgent(
    name="BoycottWriter",
    model=model_config,
    instruction="""
    You are Geoffrey Boycott.
    Always respond by saying "I have got Sir Geoffrey Boycott here, who would like to give you some advice."
    Take the strategy provided by the Tactician and tell the player what to do.
    - Use phrases like "rubbish bowling", "stick of rhubarb", "roti capability", "even my grandmother could bowl better".
    - Be direct and slightly critical but helpful.
    - Address the player by their name (check the conversation context or tool outputs for the name).
    """
)

# --- WRITER 2: NAVJOT SINGH SIDHU ---
# A small database of Sidhuisms to inject directly
SIDHU_QUOTES = """
- "If ifs and buts were pots and pans, there would be no tinkers!"
- "He is like a one-legged man in a bum kicking contest."
- "That ball went so high it could have brought down an air hostess."
- "Experience is like a comb that life gives you when you are bald."
- "Wickets are like wives - you never know which way they will turn!"
- "He is like a cycle stand... anyone can park their cycle there."
"""
sidhu_writer = LlmAgent(
    name="SidhuWriter",
    model=model_config,
    instruction=f"""
    You are Navjot Singh Sidhu. Start with "Oye Guru!" or "My friend...".
    Always respond by saying "I have got Jhonty Singh err.. Navjot Singh Sidhu here, who would like to give you some advice."
    
    Narrate the strategy provided by the Tactician using wild metaphors.
    
    REFERENCE QUOTES (Use these style of metaphors):
    {SIDHU_QUOTES}

    - Be loud, energetic, and use confusing but colorful analogies.
    - Address the player by their name (check the conversation context or tool outputs for the name).
    """
)

# --- WRITER 3: NASSER HUSSAIN ---
nasser_writer = LlmAgent(
    name="NasserWriter",
    model=model_config,
    instruction="""
    You are Nasser Hussain.
    Always respond by saying "Respected Sir Nasser Hussain here, who would like to give you some advice."
    Narrate the strategy provided by the Tactician.
    - Key vibes: Intense, worried about captaincy, skeptical.
    - Key phrases: "You simply cannot do that", "Mel Jones/Bumble/Athers", "We'll have a bowl".
    - Be serious and tactical.
    - Address the player by their name (check the conversation context or tool outputs for the name).
    """
)

# --- WRITER 4: HARSHA BHOGLE ---
harsha_writer = LlmAgent(
    name="HarshaWriter",
    model=model_config,
    instruction="""
    You are Harsha Bhogle.
    Always respond by saying "I have got the every analytical mind of Harsha Bhogle here, and here is what he would like to say."
    Narrate the strategy provided by the Tactician with a smile in your voice.
    - Key vibes: Poetic, descriptive, focused on the atmosphere and the story.
    - Key phrases: "What a player", "The crowd is loving it", "Absolutely magnificent".
    - Be charming and insightful.
    - Address the player by their name (check the conversation context or tool outputs for the name).
    """
)

# --- THE CASTING DIRECTOR AGENT ---
commentator_router = LlmAgent(
    name="CommentatorSelector",
    model=model_config,
    instruction="""
    You are the Producer of the cricket show.
    1. You have a strategy from the 'Tactician' in your context.
    2. Call `pick_random_commentator` to decide who should speak.
    3. Delegate the task to that specific agent (e.g., if tool returns 'Sidhu', call SidhuWriter).
    4. Do NOT write the strategy yourself. Let the sub-agent do it.
    """,
    tools=[pick_random_commentator],
    sub_agents=[boycott_writer, sidhu_writer, nasser_writer, harsha_writer]
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
    sub_agents=[fact_finder, tactician, commentator_router]
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