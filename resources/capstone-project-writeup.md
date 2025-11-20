# VR Cricket Strategist: AI-Powered Match Intelligence

## Problem
Cricket teams need real-time, data-driven strategic insights. Traditional coaching relies on intuition, missing patterns in historical data. Players need instant answers: "Should we bat first?" "What's our record against this opponent?"

## Solution
VR Cricket Strategist is a multi-agent AI system powered by Google ADK and Gemini delivering personalized strategy by analyzing match history, pitch conditions, and opponent records through AI commentator personalities.

## Architecture & ADK Concepts

**Multi-Agent System:**
Root orchestrator routes to specialized sub-agents. Sequential workflow: GamePlanGenerator → FactFinder → Tactician → CommentatorRouter. StatAnalyst handles data retrieval. Four commentator agents deliver insights in unique styles.

**Custom Tools (5):**
`get_venue_trends` (pitch analysis), `get_head_to_head` (opponent performance), `get_player_stats` (analytics), `get_current_identity` (session ID), `pick_random_commentator` (personality selection).

**Sessions & State:**
Session state tracks user identity and request history. Circuit breaker callback prevents infinite loops by monitoring duplicate requests.

**Observability:**
Custom circuit breaker with logging monitors agent transfers, stopping ping-pong loops after 5 duplicate inputs.

**Agent Evaluation:**
79 tests covering tools, agents, configuration, and data integrity with pytest coverage.

**Tech:**
Gemini 2.5 Flash, CSV database (100+ matches), web UI, retry logic.

## Value
Democratizes professional cricket analysis for amateurs. Players get instant, data-backed strategy that previously required expensive coaching staff.

## Implementation
Built with ADK's multi-agent framework using sequential workflows, custom data analysis tools, session management for context, callbacks for loop prevention, and comprehensive testing. Data pipeline processes historical matches to power real-time strategic recommendations.
