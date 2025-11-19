"""
Sub-agents module for VR Cricket Coach

This module provides specialized agents for different aspects of cricket coaching:
- IdentityAgent: Player identification and onboarding
- IntentRouter: Request classification
- TossStrategyAgent: Toss decision advice
- SafeTargetAgent: Target setting advice
- GenericAdvisorAgent: General cricket queries with web search

Each agent is wrapped in an AgentTool for use by the root orchestrator.
"""

from google.adk.tools import AgentTool

from .identity_agent import identity_agent
from .intent_agent import intent_agent
from .toss_strategy_agent import toss_strategy_agent
from .safe_target_agent import safe_target_agent
from .generic_advisor_agent import generic_advisor_agent

# Create Agent Tools for sub-agents
identity_tool = AgentTool(identity_agent)
intent_tool = AgentTool(intent_agent)
toss_tool = AgentTool(toss_strategy_agent)
target_tool = AgentTool(safe_target_agent)
generic_tool = AgentTool(generic_advisor_agent)

# Export agents and tools
__all__ = [
    # Individual agents
    "identity_agent",
    "intent_agent",
    "toss_strategy_agent",
    "safe_target_agent",
    "generic_advisor_agent",
    # Agent tools (wrapped for use by root agent)
    "identity_tool",
    "intent_tool",
    "toss_tool",
    "target_tool",
    "generic_tool",
]

