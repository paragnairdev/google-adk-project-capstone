"""
Sub-agents Package

This package contains all specialized agents for the VR Cricket Strategist.
Each module focuses on a specific aspect of the system.
"""

# Data collection agents
from .data_collectors import fact_finder, stat_analyst

# Strategy agents
from .strategy import tactician

# Commentator personalities
from .commentators import (
    boycott_writer,
    sidhu_writer,
    nasser_writer,
    harsha_writer,
)

# Orchestrator agents
from .orchestrators import (
    commentator_router,
    game_plan_generator,
    fallback_agent,
)

__all__ = [
    # Data collectors
    'fact_finder',
    'stat_analyst',
    # Strategy
    'tactician',
    # Commentators
    'boycott_writer',
    'sidhu_writer',
    'nasser_writer',
    'harsha_writer',
    # Orchestrators
    'commentator_router',
    'game_plan_generator',
    'fallback_agent',
]

