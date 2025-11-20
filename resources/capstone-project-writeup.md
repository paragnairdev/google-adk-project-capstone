# VR Cricket Strategist: AI-Powered Match Intelligence

## Problem Statement

**VR Cricket** is a competitive gaming phenomenon where players participate in virtual tournaments. Unlike real cricket, VR Cricket has unique constraints: players only control batting and high-level decisions—the game engine handles bowling and fielding automatically.

Players constantly face critical decisions: Should I bat first or chase? What's a safe target on this pitch type? When should I declare in a Test match? What are my chances of chasing this target?

Professional esports teams employ data analysts with sophisticated tools and databases. Casual tournament players lack this intelligence. They make crucial decisions affecting tournament advancement based purely on gut feeling and limited memory of recent matches. They can't instantly recall statistical patterns across hundreds of games or access real-time, data-driven insights.

**The gap**: How do we democratize VR Cricket strategy, bringing esports-level analysis to casual players with instant, personalized, data-driven decision-making?

## Why Agents?

Agents perfectly solve VR Cricket strategy by orchestrating multiple specialized tasks intelligently.

**Task Decomposition**: Strategy requires gathering historical data, analyzing pitch conditions, calculating probabilities, formulating tactics (bat first vs. chase, declaration timing), and delivering engaging insights. A multi-agent system creates focused experts: data retrieval, statistical analysis, strategy formulation, and personality-driven delivery.

**Dynamic Routing**: Queries vary wildly—from "What's my T20 batting average?" to "Should I bat first on green pitch?" or "When should I declare?" A root orchestrator intelligently routes requests to appropriate specialists without forcing a monolithic LLM to handle everything.

**Sequential Workflows**: Analysis follows a natural pipeline: gather history → analyze patterns → formulate advice → deliver engagingly. Sequential agents model this perfectly, ensuring each step completes before the next.

**Personality & Engagement**: Gaming is entertainment, not just data. Multiple commentator agents (Geoffrey Boycott, Navjot Sidhu, Nasser Hussain, Harsha Bhogle) deliver strategic insights with personality, making VR Cricket engaging rather than robotic.

**Reliability & Observability**: Callbacks and circuit breakers monitor agent behavior, prevent ping-pong routing loops, and ensure reliability—critical for time-sensitive tournament decisions.

## What I Created

**VR Cricket Strategist** is a production-ready multi-agent system built with Google's ADK and Gemini 2.5 Flash. It delivers personalized, data-driven tournament strategy through specialized AI agents, helping players decide: bat first or chase, when to declare, and safe target scores based on historical performance.

### Architecture Overview
*(See architecture diagram)*

**Root Orchestrator**: Identifies users via session state and routes queries to specialists.

**GamePlanGenerator (Sequential)**: Three-agent workflow—FactFinder (retrieves historical data) → Tactician (formulates strategy using tournament-specific logic) → CommentatorRouter (selects personality).

**StatAnalyst**: Handles data queries about player statistics and historical records with direct tool access.

**Commentator Agents (4)**: BoycottWriter (analytical/critical), SidhuWriter (entertaining/metaphors), NasserWriter (tactical/modern), HarshaWriter (eloquent/storytelling).

### Custom Tools (5)

1. **`get_venue_trends`**: Calculates average scores and win rates by pitch type and venue
2. **`get_head_to_head`**: Retrieves matchup records and performance stats
3. **`get_player_stats`**: Computes comprehensive player statistics (matches, runs, averages, strike rates, centuries, etc.)
4. **`get_current_identity`**: Accesses session state for user identification with dev mode auto-injection
5. **`pick_random_commentator`**: Randomly selects commentator personalities

### Sessions & State Management

ADK's session management maintains user context: player identity, request history, retry counts, and last inputs for loop detection. This enables personalized, style-specific responses.

### Observability: Circuit Breaker Callback

A custom `before_agent_callback` monitors agent transfers. If an agent receives identical input 5+ times (ping-pong loop), the circuit breaker injects override instructions to stop gracefully, preventing infinite loops.

### Testing & Technology

**79 comprehensive tests** covering tools, agent configuration, data integrity, integration, and edge cases. Includes pytest configuration, HTML coverage reports, and fixtures.

**Stack**: Google ADK (orchestration, sessions, tools) • Gemini 2.5 Flash (with retry logic) • CSV Database (100+ matches) • ADK Web UI • Python 3.13 • pytest

## Demo

**Example Query**: "I'm playing against Ragz in a T20 VR Cricket tournament on a green pitch with overcast conditions. Should I bat first or chase?"

**System Flow**:
1. Root agent calls `get_current_identity()` → identifies user as "Joe" from England
2. Routes to GamePlanGenerator (sequential workflow begins)
3. FactFinder calls `get_head_to_head("Joe", "Ragz", "T20")` and `get_venue_trends("T20", "Green")`
4. Tactician analyzes: Green pitch shows 58% win rate for teams batting second, Joe has won 3/7 matches chasing against Ragz, average first innings score is 165
5. CommentatorRouter calls `pick_random_commentator()` → selects "Nasser"
6. NasserWriter delivers: *"Right then, Joe. Looking at your tournament history, I'd strongly recommend bowling first here. Green pitches in VR Cricket show teams chasing win 58% of the time, and you've historically struggled setting targets against Ragz—you've only defended successfully once in your last 5 encounters. The average first innings score is 165, so if you chase, aim for calculated aggression. Set a target of 15-20 runs above average in your powerplay, and you should be on track..."*

**Example Query 2**: "I'm at 450/5 in a Test match after 100 overs. Should I declare or keep batting?"

**System Response**: *"Geoffrey Boycott here. Look, you're in a commanding position at 450 for 5. On this pitch type, teams batting second average 380 in Test matches. I'd bat on for another 10-15 overs—get yourself to 500-520. That extra cushion is worth more than the time cost. Remember, in VR Cricket tournaments, declarations can't be reversed. Better to be 70 runs safer than 5 overs shorter. Patience wins Test matches, lad."*

*(Screenshots/video showing web UI interactions with personality-driven responses)*

## The Build

### Development Process

**Data Pipeline**: Created synthetic VR Cricket data (Test/ODI/T20, multiple pitch types, outcomes).

**Tools & Agents**: Built 5 pandas-based tools, then agents bottom-up—leaf agents (FactFinder, Tactician, Commentators) → orchestrators → root.

**Observability**: Integrated session service and circuit breaker callback preventing infinite loops.

**Testing**: Built 79-test suite with pytest; used ADK's web UI for demos.

### Key Challenges Solved
- **Agent Loop Prevention**: Circuit breaker detects and stops infinite routing—critical for quick tournament decisions
- **Session State Management**: Maintaining user identity across conversation turns
- **Tool Parameter Inference**: Extracting parameters (format, pitch, opponent) from natural language
- **Personality Consistency**: Each commentator maintains distinct voice through crafted instructions
- **Context-Aware Strategy**: Understanding VR Cricket constraints (batting-only decisions)

## If I Had More Time

**ML Win Probability**: Implement models predicting chase success and optimal declaration timing.

**Live Tournament Integration**: Connect to VR Cricket APIs for real-time in-game strategy and dynamic analysis.

**Voice Interface**: Add speech-to-text/text-to-speech for verbal queries—perfect for streaming.

**Discord Bot**: Deploy for tournament communities with integrated queries, statistics, and leaderboards.

**Real Tournament Data**: Auto-import from VR Cricket platforms, expanding beyond synthetic datasets.

**Agent Simulations**: Simulate matches based on historical data, predicting bracket outcomes.

---

**Repository**: github.com/paragnairdev/google-adk-project-capstone
**Built with**: Google Agent Development Kit, Gemini 2.5 Flash, Python 3.13
