# VR Cricket Strategist: AI-Powered Match Intelligence

## Problem Statement

**VR Cricket** is a competitive gaming phenomenon where players participate in virtual cricket tournaments. Unlike real cricket where teams control both batting and bowling, VR Cricket players face unique strategic constraints: they can only bat and make high-level decisions—the game engine handles bowling and fielding automatically.

Players constantly face critical tournament decisions: Should I bat first or chase? What's a safe target to set on this pitch type? When should I declare my innings in a Test match? What are my chances of successfully chasing this target based on my historical performance?

Professional esports teams employ data analysts with access to sophisticated tools and historical databases. However, casual VR Cricket tournament players lack this strategic intelligence. They're making crucial decisions that determine tournament advancement based purely on gut feeling.

The traditional approach relies on intuition and limited memory. Players might remember their last few matches but can't instantly recall statistical patterns across hundreds of virtual games. They need real-time, data-driven insights but lack resources to analyze complex performance datasets.

This creates a gap: democratizing VR Cricket strategy. How do we bring esports-level analysis to casual tournament players, making data-driven decision-making accessible, instant, and personalized for the virtual cricket gaming community?

## Why Agents?

Agents are the perfect solution for VR Cricket tournament strategy because the problem requires orchestrating multiple specialized tasks that must work together intelligently.

**Task Decomposition**: VR Cricket tournament strategy isn't a single query—it requires gathering historical tournament data, analyzing virtual pitch conditions, calculating win probabilities, formulating tactical advice (bat first vs. chase, when to declare), and delivering insights in an engaging way. Each is a distinct specialization. A multi-agent system creates focused experts: one agent retrieves data, another analyzes statistics, a third formulates strategy, and commentator agents deliver insights.

**Dynamic Routing**: User queries vary wildly. One player might ask "What's my batting average in T20 tournaments?", while another asks "Should I bat first on a green pitch?" or "When should I declare?" A root orchestrator agent intelligently routes requests to the appropriate specialist, ensuring efficient responses without forcing a single monolithic LLM to handle all scenarios.

**Sequential Workflows**: Strategic analysis follows a natural pipeline: gather tournament history → analyze patterns → formulate advice → deliver in engaging format. Sequential agents perfectly model this workflow, ensuring each step completes before the next begins.

**Personality & Engagement**: Gaming isn't just data—it's entertainment. By using multiple commentator agents (mimicking legends like Geoffrey Boycott, Navjot Sidhu, Nasser Hussain, and Harsha Bhogle), we deliver strategic insights with personality and flair, making the VR Cricket experience engaging rather than robotic.

**Reliability & Observability**: Agents can fail or enter infinite loops. By using callbacks and circuit breakers, we monitor agent behavior, prevent ping-pong routing issues, and ensure system reliability—critical for tournament players making time-sensitive decisions.

## What I Created

**VR Cricket Strategist** is a production-ready multi-agent system built with Google's Agent Development Kit (ADK) and powered by Gemini 2.5 Flash. It provides personalized, data-driven tournament strategy for VR Cricket players through an intelligent hierarchy of specialized AI agents. The system helps players make critical decisions: bat first or chase, when to declare, and what targets are safe based on their historical tournament performance.

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

ADK's session management maintains user context. Session state stores user identity (player name, team, batting style), request history, retry counts, and last inputs for loop detection. This enables personalized responses tailored to individual playing styles.

### Observability: Circuit Breaker Callback

A custom `before_agent_callback` monitors agent transfers. If an agent receives the same input more than 5 times (indicating a ping-pong loop), the circuit breaker injects override instructions, forcing the agent to stop and apologize. This prevents infinite loops and ensures graceful failure.

### Agent Evaluation & Testing

**79 comprehensive tests** covering unit tests for all tools, agent configuration validation, data integrity, tool-agent integration, and edge case handling (empty data, missing values, invalid formats). Includes pytest configuration, HTML coverage reports, and test fixtures.

### Technology Stack
- **Google ADK**: Multi-agent framework, session management, tool integration
- **Gemini 2.5 Flash**: Powers all LLM agents with retry logic for reliability
- **CSV Database**: 100+ historical VR Cricket tournament matches with players, teams, pitch types, venues, and results
- **Web UI**: ADK's built-in playground for interactive testing during tournaments
- **Python 3.13**: Modern Python with type hints and async support
- **pytest**: Comprehensive testing framework

## Demo

**Example Query**: "I'm playing against Wizheart in a T20 VR Cricket tournament on a green pitch with overcast conditions. Should I bat first or chase?"

**System Flow**:
1. Root agent calls `get_current_identity()` → identifies user as "Joe" from England
2. Routes to GamePlanGenerator (sequential workflow begins)
3. FactFinder calls `get_head_to_head("Joe", "Wizheart", "T20")` and `get_venue_trends("T20", "Green")`
4. Tactician analyzes: Green pitch shows 58% win rate for teams batting second, Joe has won 3/7 matches chasing against Wizheart, average first innings score is 165
5. CommentatorRouter calls `pick_random_commentator()` → selects "Nasser"
6. NasserWriter delivers: *"Right then, Joe. Looking at your tournament history, I'd strongly recommend bowling first here. Green pitches in VR Cricket show teams chasing win 58% of the time, and you've historically struggled setting targets against Wizheart—you've only defended successfully once in your last 5 encounters. The average first innings score is 165, so if you chase, aim for calculated aggression. Set a target of 15-20 runs above average in your powerplay, and you should be on track..."*

**Example Query 2**: "I'm at 450/5 in a Test match after 100 overs. Should I declare or keep batting?"

**System Response**: *"Geoffrey Boycott here. Look, you're in a commanding position at 450 for 5. On this pitch type, teams batting second average 380 in Test matches. I'd bat on for another 10-15 overs—get yourself to 500-520. That extra cushion is worth more than the time cost. Remember, in VR Cricket tournaments, declarations can't be reversed. Better to be 70 runs safer than 5 overs shorter. Patience wins Test matches, lad."*

*(Screenshots/video showing web UI interactions with personality-driven responses)*

## The Build

### Development Process

**Data Pipeline**: Created synthetic VR Cricket tournament data (Test/ODI/T20 formats, multiple pitch types, match outcomes).

**Tools & Agents**: Built 5 pandas-based tools, then implemented agents bottom-up—leaf agents (FactFinder, Tactician, Commentators) → orchestrators → composites → root.

**Session & Observability**: Integrated ADK's session service for user context and circuit breaker callback to prevent infinite loops.

**Testing & UI**: Built 79-test suite with pytest; used ADK's web UI for demonstrations.

### Key Technologies
- **Google ADK**: Multi-agent orchestration, tool integration, session management
- **Gemini 2.5 Flash**: With retry configuration for resilience
- **Python Pandas**: Data analysis and CSV processing
- **pytest**: Testing and coverage analysis

### Key Challenges Solved
- **Agent Loop Prevention**: Circuit breaker callback detects and stops infinite routing—critical for tournament players needing quick decisions
- **Session State Management**: Maintaining user identity and tournament history across conversation turns
- **Tool Parameter Inference**: Agents learn to extract parameters (format, pitch type, opponent) from natural language queries
- **Personality Consistency**: Each commentator agent maintains distinct voice through carefully crafted instructions, making the VR Cricket experience entertaining
- **Context-Aware Recommendations**: Agents understand the constraints of VR Cricket (batting-only decisions) and provide relevant strategic advice

## If I Had More Time

**ML Win Probability**: Implement models predicting chase success rates and optimal Test match declaration timing based on historical patterns.

**Live Tournament Integration**: Connect to VR Cricket APIs for real-time in-game strategy suggestions and dynamic performance analysis between innings.

**Voice Interface**: Add speech-to-text/text-to-speech, allowing players to verbally query strategies and receive audio responses—perfect for streaming.

**Discord Bot**: Deploy as a Discord bot for tournament communities with channel-integrated queries, tournament statistics, and leaderboards.

**Mobile App**: React Native companion with push notifications for tournament reminders, pre-match briefings, and post-game analysis.

**Real Tournament Data**: Integrate with VR Cricket platforms to automatically import real tournament data, expanding beyond synthetic datasets.

**Team Collaboration**: Multi-user support with shared session state for team strategy rooms and collaborative decision-making.

**Replay Analysis**: Connect with VR Cricket replay systems to analyze batting patterns, identify weaknesses, and suggest improvements.

**Agent Simulations**: Create scenarios where agents simulate matches based on historical data, predicting tournament bracket outcomes.

---

**Repository**: github.com/[your-username]/google-adk (not shared publicly to protect API keys)
**Built with**: Google Agent Development Kit, Gemini 2.5 Flash, Python 3.13
