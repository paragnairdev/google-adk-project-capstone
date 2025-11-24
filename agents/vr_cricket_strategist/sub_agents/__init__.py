"""
Sub-agents Package

This package contains all specialized agents for the VR Cricket Strategist.
Each module focuses on a specific aspect of the system.
"""

# Data collection agents
from .data_collectors import fact_finder_agent, stat_analyst_agent

# Strategy agents
from .strategy import tactician_agent

# Commentator personalities
from .commentators import (
    boycott_writer_agent,
    sidhu_writer_agent,
    nasser_writer_agent,
    harsha_writer_agent,
)

# Orchestrator agents
from .orchestrators import (
    commentator_router_agent,
    game_plan_generator_agent,
    generic_responder_agent,
)

__all__ = [
    # Data collectors
    'fact_finder_agent',
    'stat_analyst_agent',
    # Strategy
    'tactician_agent',
    # Commentators
    'boycott_writer_agent',
    'sidhu_writer_agent',
    'nasser_writer_agent',
    'harsha_writer_agent',
    # Orchestrators
    'commentator_router_agent',
    'game_plan_generator_agent',
    'generic_responder_agent',
]

