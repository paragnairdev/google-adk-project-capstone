# VR Cricket Strategist: AI-Powered Match Intelligence

## Problem Statement

Cricket strategy separates winners from losers. Teams constantly face critical decisions: Should we bat or bowl first? What bowling changes should we make in the death overs? How does our team perform against this opponent on this pitch type?

Professional cricket teams employ analytics departments and coaching staff with sophisticated data analysis tools and historical databases. Amateur cricket players, club teams, and casual players lack access to this strategic intelligence.

The traditional approach relies on intuition and limited manual analysis. Coaches might remember key matches but can't instantly recall statistical patterns across hundreds of games. Players need real-time, data-driven insights but lack resources or time to analyze complex datasets during matches.

This creates a gap: democratizing cricket strategy. How do we bring professional-level analysis to everyday players, making data-driven decision-making accessible, instant, and personalized?

## Why Agents?

Agents are the perfect solution for cricket strategy because the problem requires orchestrating multiple specialized tasks that must work together intelligently.

**Task Decomposition**: Cricket strategy isn't a single query—it requires gathering historical data, analyzing pitch conditions, calculating statistics, formulating tactical advice, and delivering insights in an engaging way. Each of these is a distinct specialization. A multi-agent system allows us to create focused experts: one agent retrieves data, another analyzes statistics, a third formulates strategy, and commentator agents deliver insights.

**Dynamic Routing**: User queries vary wildly. One user might ask "What's my batting average?", while another asks "Should I bat first on a green pitch?" A root orchestrator agent can intelligently route requests to the appropriate specialist, ensuring efficient and accurate responses without forcing a single monolithic LLM to handle all scenarios.

**Sequential Workflows**: Strategic analysis follows a natural pipeline: first gather facts, then analyze patterns, then formulate advice, finally deliver in an engaging format. Sequential agents perfectly model this workflow, ensuring each step completes before the next begins.

**Personality & Engagement**: Cricket isn't just data—it's entertainment. By using multiple commentator agents (mimicking legends like Geoffrey Boycott, Navjot Sidhu, Nasser Hussain, and Harsha Bhogle), we deliver strategic insights with personality and flair, making the experience engaging rather than robotic.

**Reliability & Observability**: Agents can fail or enter infinite loops. By using callbacks and circuit breakers, we monitor agent behavior, prevent ping-pong routing issues, and ensure system reliability—something that would be nearly impossible with a single LLM endpoint.

## What I Created

**VR Cricket Strategist** is a production-ready multi-agent system built with Google's Agent Development Kit (ADK) and powered by Gemini 2.5 Flash. It provides personalized, data-driven cricket strategy through an intelligent hierarchy of specialized AI agents.

### Architecture Overview
*(See architecture diagram - showing agent hierarchy and data flow)*

**Root Orchestrator Agent**: The entry point that identifies the user via session state and routes queries to the appropriate specialist. It handles greetings and delegates complex requests.

**GamePlanGenerator (Sequential Agent)**: Orchestrates the complete strategy workflow through three sub-agents in sequence:
- **FactFinder**: Retrieves historical head-to-head records and venue trends from the match database
- **Tactician**: Analyzes the data and formulates strategic recommendations using cricket-specific decision logic
- **CommentatorRouter**: Selects a personality and delegates insight delivery

**StatAnalyst Agent**: Handles pure data queries about player statistics, stadium information, and historical records. Equipped with direct access to all statistical tools.

**Commentator Agents (4 personalities)**: Each agent has distinct instructions mimicking real cricket commentators:
- **BoycottWriter**: Analytical and critical, focusing on technical details
- **SidhuWriter**: Entertaining with metaphors and enthusiastic delivery
- **NasserWriter**: Balanced tactical analysis with modern insights
- **HarshaWriter**: Eloquent storytelling with deep cricket knowledge

### Custom Tools (5 integrated)

1. **`get_venue_trends(format, pitch_type, stadium)`**: Analyzes historical match data to calculate average first innings scores, win rates for batting first vs. second, filtered by pitch conditions and venue.

2. **`get_head_to_head(player_name, opponent_name, format, pitch_type, stadium)`**: Retrieves win/loss records and performance statistics for specific matchups.

3. **`get_player_stats(player_name, format)`**: Computes comprehensive player statistics including matches played, runs, averages, strike rates, centuries, fifties, ducks, wickets, and economy.

4. **`get_current_identity(tool_context)`**: Accesses session state to identify the current user. Includes a developer mode that auto-injects test profiles for seamless testing.

5. **`pick_random_commentator()`**: Randomly selects from the four commentator personalities to add variety to responses.

### Sessions & State Management

The system uses ADK's session management to maintain user context across conversations. Session state stores:
- User identity (player name, team, batting style)
- Request history and retry counts
- Last input seen by each agent (for loop detection)

This enables personalized responses—the system knows who you are and tailors advice to your playing style and team.

### Observability: Circuit Breaker Callback

A custom `before_agent_callback` monitors agent transfers. If an agent receives the same input more than 5 times (indicating a ping-pong loop), the circuit breaker injects override instructions, forcing the agent to stop and apologize. This prevents infinite loops and ensures graceful failure.

### Agent Evaluation & Testing

**79 comprehensive tests** covering unit tests for all tools, agent configuration validation, data integrity, tool-agent integration, and edge case handling (empty data, missing values, invalid formats). Includes pytest configuration, HTML coverage reports, and test fixtures.

### Technology Stack
- **Google ADK**: Multi-agent framework, session management, tool integration
- **Gemini 2.5 Flash**: Powers all LLM agents with retry logic for reliability
- **CSV Database**: 100+ historical matches with players, teams, pitch types, venues, and results
- **Web UI**: ADK's built-in playground for interactive testing
- **Python 3.13**: Modern Python with type hints and async support
- **pytest**: Comprehensive testing framework

## Demo

**Example Query**: "We're playing on a green pitch with overcast conditions against Wizheart's team in a T20 match. What should be our strategy?"

**System Flow**:
1. Root agent calls `get_current_identity()` → identifies user as "Joe" from England
2. Routes to GamePlanGenerator (sequential workflow begins)
3. FactFinder calls `get_head_to_head("Joe", "Wizheart", "T20")` and `get_venue_trends("T20", "Green")`
4. Tactician analyzes: Green pitch + overcast = favorable for bowling, Wizheart has 65% win rate batting first
5. CommentatorRouter calls `pick_random_commentator()` → selects "Nasser"
6. NasserWriter delivers: *"Right then, Joe. The conditions are absolutely in your favor here—green top, overcast skies, that's a seamer's paradise. Wizheart's team has a strong record chasing, but you've got to bowl first and exploit these conditions early. Get the new ball swinging, attack with two slips, and aim to have them 3 down inside the powerplay..."*

*(Screenshot/video would show the web UI interaction here)*

## The Build

### Development Process

**Data Pipeline**: Created synthetic cricket match data with multiple formats (Test, ODI, T20), pitch types (Green, Dry, Bouncy, Normal), and outcomes.

**Custom Tools**: Built 5 specialized pandas-based tools for data analysis, filtering and aggregating match statistics.

**Agent Creation**: Implemented bottom-up—leaf agents first (FactFinder, Tactician, Commentators), then orchestrators (CommentatorRouter), composite agents (GamePlanGenerator), and finally the root orchestrator.

**Session Management**: Integrated ADK's session service for user context and identity tracking via `get_current_identity()`.

**Observability**: Implemented circuit breaker callback after discovering ping-pong loops during testing.

**Testing**: Built 79-test suite using pytest, covering all components with unit and integration tests.

**UI Integration**: Used ADK's web UI for interactive testing and demonstrations.

### Key Technologies
- **Google ADK**: The foundation—multi-agent orchestration, tool integration, session management
- **Gemini API**: Gemini 2.5 Flash with retry configuration for resilience
- **Python Pandas**: Data analysis and CSV processing
- **pytest & pytest-cov**: Testing and coverage analysis

### Key Challenges Solved
- **Agent Loop Prevention**: Circuit breaker callback detects and stops infinite routing
- **Session State Management**: Maintaining user identity across conversation turns
- **Tool Parameter Inference**: Agents learn to extract parameters (format, pitch type) from natural language
- **Personality Consistency**: Each commentator agent maintains distinct voice through carefully crafted instructions

## If I Had More Time

**Advanced Analytics**: Implement ML models for predictive analysis—predicting match outcomes, suggesting optimal batting orders, forecasting player performance based on conditions.

**Real-time Data Integration**: Connect to live cricket APIs (Cricbuzz, ESPN Cricinfo) for real-time match updates and statistics. The agent could provide in-game strategy adjustments.

**Voice Interface**: Add speech-to-text input and text-to-speech output, allowing players to verbally ask questions during practice sessions and receive audio responses from their favorite commentator.

**Deployment to Cloud**: Deploy using Agent Engine on Google Cloud Platform with proper scaling, monitoring, and production logging. Set up CI/CD pipelines for automated testing and deployment.

**Mobile App**: Build a React Native mobile app with push notifications for match reminders, pre-game strategy briefings, and post-game analysis.

**Expanded Database**: Partner with cricket leagues to integrate actual historical match data, expanding from synthetic data to real-world statistics across thousands of professional and amateur matches.

**Team Collaboration**: Add multi-user support where entire teams can collaborate, sharing strategies and insights. Include role-based access (captain, coach, player) with different permission levels.

**Video Analysis Integration**: Integrate with video analysis tools, allowing agents to analyze ball-by-ball video footage and provide visual feedback on technique and strategy.

**Agent-to-Agent Tournaments**: Create competitive scenarios where agents representing different teams play strategic chess matches, simulating entire cricket matches based on probabilistic outcomes.

---

**Repository**: github.com/[your-username]/google-adk (not shared publicly to protect API keys)
**Built with**: Google Agent Development Kit, Gemini 2.5 Flash, Python 3.13
