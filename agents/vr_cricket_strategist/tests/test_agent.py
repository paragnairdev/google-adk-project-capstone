"""
Tests for vr_cricket_strategist agent configuration
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


class TestAgentImports:
    """Tests for agent module imports"""
    
    def test_agent_module_imports(self):
        """Test that agent module can be imported"""
        from agents.vr_cricket_strategist import agent
        assert agent is not None
    
    def test_required_imports_present(self):
        """Test that required imports are available"""
        from agents.vr_cricket_strategist.agent import (
            LlmAgent, SequentialAgent, Gemini
        )
        assert LlmAgent is not None
        assert SequentialAgent is not None
        assert Gemini is not None


class TestAgentConfiguration:
    """Tests for agent configuration"""
    
    def test_model_config_exists(self):
        """Test that model_config is defined"""
        from agents.vr_cricket_strategist.agent import model_config
        assert model_config is not None
    
    def test_model_config_type(self):
        """Test that model_config is a Gemini instance"""
        from agents.vr_cricket_strategist.agent import model_config, Gemini
        assert isinstance(model_config, Gemini)
    
    def test_model_name(self):
        """Test that model is configured correctly"""
        from agents.vr_cricket_strategist.agent import model_config
        assert hasattr(model_config, 'model')
        # Model should be set to a valid Gemini model
        assert 'gemini' in model_config.model.lower()


class TestSubAgents:
    """Tests for individual sub-agents"""
    
    def test_fact_finder_exists(self):
        """Test that fact_finder_agent is defined"""
        from agents.vr_cricket_strategist.agent import fact_finder_agent
        assert fact_finder_agent is not None
    
    def test_fact_finder_configuration(self):
        """Test fact_finder_agent configuration"""
        from agents.vr_cricket_strategist.agent import fact_finder_agent
        
        assert fact_finder_agent.name == "fact_finder_agent"
        assert hasattr(fact_finder_agent, 'model')
        assert hasattr(fact_finder_agent, 'tools')
        # Should have tools for data retrieval
        assert len(fact_finder_agent.tools) > 0
    
    def test_fact_finder_tools(self):
        """Test that fact_finder_agent has correct tools"""
        from agents.vr_cricket_strategist.agent import fact_finder_agent
        
        # Should have get_head_to_head and get_venue_trends
        tool_names = [tool.__name__ for tool in fact_finder_agent.tools]
        assert 'get_head_to_head' in tool_names
        assert 'get_venue_trends' in tool_names
    
    def test_tactician_exists(self):
        """Test that tactician_agent is defined"""
        from agents.vr_cricket_strategist.agent import tactician_agent
        assert tactician_agent is not None
    
    def test_tactician_configuration(self):
        """Test tactician_agent configuration"""
        from agents.vr_cricket_strategist.agent import tactician_agent
        
        assert tactician_agent.name == "tactician_agent"
        assert hasattr(tactician_agent, 'model')
        assert hasattr(tactician_agent, 'instruction')
        # Tactician should have strategic decision logic
        assert 'strategy' in tactician_agent.instruction.lower() or 'decision' in tactician_agent.instruction.lower()
    
    def test_writer_agents_exist(self):
        """Test that all writer agents are defined"""
        from agents.vr_cricket_strategist.agent import (
            boycott_writer_agent, sidhu_writer_agent, nasser_writer_agent, harsha_writer_agent
        )
        assert boycott_writer_agent is not None
        assert sidhu_writer_agent is not None
        assert nasser_writer_agent is not None
        assert harsha_writer_agent is not None
    
    def test_boycott_writer_configuration(self):
        """Test boycott_writer_agent configuration"""
        from agents.vr_cricket_strategist.agent import boycott_writer_agent
        
        assert boycott_writer_agent.name == "boycott_writer_agent"
        assert hasattr(boycott_writer_agent, 'instruction')
        # Should have Geoffrey Boycott persona
        assert 'boycott' in boycott_writer_agent.instruction.lower()
    
    def test_sidhu_writer_configuration(self):
        """Test sidhu_writer_agent configuration"""
        from agents.vr_cricket_strategist.agent import sidhu_writer_agent
        
        assert sidhu_writer_agent.name == "sidhu_writer_agent"
        assert hasattr(sidhu_writer_agent, 'instruction')
        # Should have Navjot Singh Sidhu persona
        assert 'sidhu' in sidhu_writer_agent.instruction.lower()
    
    def test_nasser_writer_configuration(self):
        """Test nasser_writer_agent configuration"""
        from agents.vr_cricket_strategist.agent import nasser_writer_agent
        
        assert nasser_writer_agent.name == "nasser_writer_agent"
        assert hasattr(nasser_writer_agent, 'instruction')
        # Should have Nasser Hussain persona
        assert 'nasser' in nasser_writer_agent.instruction.lower()
    
    def test_harsha_writer_configuration(self):
        """Test harsha_writer_agent configuration"""
        from agents.vr_cricket_strategist.agent import harsha_writer_agent
        
        assert harsha_writer_agent.name == "harsha_writer_agent"
        assert hasattr(harsha_writer_agent, 'instruction')
        # Should have Harsha Bhogle persona
        assert 'harsha' in harsha_writer_agent.instruction.lower()
    
    def test_commentator_router_exists(self):
        """Test that commentator_router_agent is defined"""
        from agents.vr_cricket_strategist.agent import commentator_router_agent
        assert commentator_router_agent is not None
    
    def test_commentator_router_configuration(self):
        """Test commentator_router_agent configuration"""
        from agents.vr_cricket_strategist.agent import commentator_router_agent
        
        assert commentator_router_agent.name == "commentator_selector_agent"
        assert hasattr(commentator_router_agent, 'tools')
        assert hasattr(commentator_router_agent, 'sub_agents')
        # Should have pick_random_commentator tool
        tool_names = [tool.__name__ for tool in commentator_router_agent.tools]
        assert 'pick_random_commentator' in tool_names
    
    def test_commentator_router_sub_agents(self):
        """Test that commentator_router_agent has all writer agents"""
        from agents.vr_cricket_strategist.agent import (
            commentator_router_agent, boycott_writer_agent, sidhu_writer_agent, 
            nasser_writer_agent, harsha_writer_agent
        )
        
        assert len(commentator_router_agent.sub_agents) == 4
        assert boycott_writer_agent in commentator_router_agent.sub_agents
        assert sidhu_writer_agent in commentator_router_agent.sub_agents
        assert nasser_writer_agent in commentator_router_agent.sub_agents
        assert harsha_writer_agent in commentator_router_agent.sub_agents
    
    def test_stat_analyst_exists(self):
        """Test that stat_analyst_agent is defined"""
        from agents.vr_cricket_strategist.agent import stat_analyst_agent
        assert stat_analyst_agent is not None
    
    def test_stat_analyst_configuration(self):
        """Test stat_analyst_agent configuration"""
        from agents.vr_cricket_strategist.agent import stat_analyst_agent
        
        assert stat_analyst_agent.name == "stat_analyst_agent"
        assert hasattr(stat_analyst_agent, 'tools')
        # Should have data query tools
        assert len(stat_analyst_agent.tools) > 0
    
    def test_stat_analyst_tools(self):
        """Test that stat_analyst_agent has correct tools"""
        from agents.vr_cricket_strategist.agent import stat_analyst_agent
        
        tool_names = [tool.__name__ for tool in stat_analyst_agent.tools]
        assert 'get_venue_trends' in tool_names
        assert 'get_head_to_head' in tool_names
        assert 'get_player_stats' in tool_names
    
    def test_fallback_agent_exists(self):
        """Test that generic_responder_agent is defined"""
        from agents.vr_cricket_strategist.agent import generic_responder_agent
        assert generic_responder_agent is not None
    
    def test_fallback_agent_configuration(self):
        """Test generic_responder_agent configuration"""
        from agents.vr_cricket_strategist.agent import generic_responder_agent
        
        assert generic_responder_agent.name == "generic_responder_agent"
        assert hasattr(generic_responder_agent, 'instruction')
        # Should mention fallback/handler
        assert 'fallback' in generic_responder_agent.instruction.lower() or 'handler' in generic_responder_agent.instruction.lower()


class TestCompositeAgents:
    """Tests for composite agents"""
    
    def test_game_plan_generator_exists(self):
        """Test that game_plan_generator_agent is defined"""
        from agents.vr_cricket_strategist.agent import game_plan_generator_agent
        assert game_plan_generator_agent is not None
    
    def test_game_plan_generator_type(self):
        """Test that game_plan_generator_agent is a SequentialAgent"""
        from agents.vr_cricket_strategist.agent import game_plan_generator_agent, SequentialAgent
        assert isinstance(game_plan_generator_agent, SequentialAgent)
    
    def test_game_plan_generator_configuration(self):
        """Test game_plan_generator_agent configuration"""
        from agents.vr_cricket_strategist.agent import game_plan_generator_agent
        
        assert game_plan_generator_agent.name == "game_plan_generator_agent"
        assert hasattr(game_plan_generator_agent, 'description')
        assert hasattr(game_plan_generator_agent, 'sub_agents')
    
    def test_game_plan_generator_sub_agents(self):
        """Test that game_plan_generator_agent has correct sub-agents in order"""
        from agents.vr_cricket_strategist.agent import (
            game_plan_generator_agent, fact_finder_agent, tactician_agent, commentator_router_agent
        )
        
        sub_agents = game_plan_generator_agent.sub_agents
        assert len(sub_agents) == 3
        assert sub_agents[0] == fact_finder_agent
        assert sub_agents[1] == tactician_agent
        assert sub_agents[2] == commentator_router_agent
    
    def test_root_agent_exists(self):
        """Test that root_agent and its components are defined"""
        from agents.vr_cricket_strategist.agent import (
            root_agent, orchestrator_agent, identity_agent
        )
        assert root_agent is not None
        assert orchestrator_agent is not None
        assert identity_agent is not None
    
    def test_root_agent_configuration(self):
        """Test root_agent configuration"""
        from agents.vr_cricket_strategist.agent import root_agent, SequentialAgent
        
        assert root_agent.name == "root_agent"
        assert isinstance(root_agent, SequentialAgent)
        assert hasattr(root_agent, 'sub_agents')

    def test_orchestrator_agent_configuration(self):
        """Test orchestrator_agent configuration"""
        from agents.vr_cricket_strategist.agent import orchestrator_agent
        
        assert orchestrator_agent.name == "cricket_coach_orchestrator_agent"
        assert hasattr(orchestrator_agent, 'tools')
        assert hasattr(orchestrator_agent, 'sub_agents')
        assert hasattr(orchestrator_agent, 'instruction')
    
    def test_orchestrator_agent_tools(self):
        """Test that orchestrator_agent has identity tool"""
        from agents.vr_cricket_strategist.agent import orchestrator_agent
        
        tool_names = [tool.__name__ for tool in orchestrator_agent.tools]
        assert 'get_current_identity' in tool_names
    
    def test_root_agent_sub_agents(self):
        """Test that root_agent has correct sub-agents"""
        from agents.vr_cricket_strategist.agent import (
            root_agent, orchestrator_agent, identity_agent
        )
        
        sub_agents = root_agent.sub_agents
        assert len(sub_agents) == 2
        assert identity_agent in sub_agents
        assert orchestrator_agent in sub_agents

    def test_orchestrator_sub_agents(self):
        """Test that orchestrator_agent has correct sub-agents"""
        from agents.vr_cricket_strategist.agent import (
            orchestrator_agent, game_plan_generator_agent, stat_analyst_agent, generic_responder_agent
        )

        sub_agents = orchestrator_agent.sub_agents
        assert len(sub_agents) == 3
        assert game_plan_generator_agent in sub_agents
        assert stat_analyst_agent in sub_agents
        assert generic_responder_agent in sub_agents


class TestAgentInstructions:
    """Tests for agent instructions and personas"""
    
    def test_fact_finder_instruction_content(self):
        """Test that fact_finder_agent has appropriate instructions"""
        from agents.vr_cricket_strategist.agent import fact_finder_agent
        
        instruction = fact_finder_agent.instruction.lower()
        # Should mention data retrieval and not giving advice
        assert 'data' in instruction
        assert 'tool' in instruction or 'call' in instruction
    
    def test_tactician_instruction_logic(self):
        """Test that tactician_agent has decision logic"""
        from agents.vr_cricket_strategist.agent import tactician_agent
        
        instruction = tactician_agent.instruction.lower()
        # Should mention decision making
        assert 'decision' in instruction or 'strategy' in instruction
    
    def test_writer_personas(self):
        """Test that writer agents have correct personas"""
        from agents.vr_cricket_strategist.agent import (
            boycott_writer_agent, sidhu_writer_agent, nasser_writer_agent, harsha_writer_agent
        )
        
        # Boycott should mention Geoffrey Boycott
        assert 'Geoffrey Boycott' in boycott_writer_agent.instruction or 'Boycott' in boycott_writer_agent.instruction
        # Should have characteristic phrases
        assert 'rubbish' in boycott_writer_agent.instruction.lower() or 'rhubarb' in boycott_writer_agent.instruction.lower()
        
        # Sidhu should have metaphorical style
        assert 'Navjot Singh Sidhu' in sidhu_writer_agent.instruction or 'Sidhu' in sidhu_writer_agent.instruction
        
        # Nasser should have tactical style
        assert 'Nasser Hussain' in nasser_writer_agent.instruction or 'Nasser' in nasser_writer_agent.instruction
        
        # Harsha should have poetic style
        assert 'Harsha Bhogle' in harsha_writer_agent.instruction or 'Harsha' in harsha_writer_agent.instruction
    
    def test_commentator_router_instruction(self):
        """Test that commentator_router_agent has routing logic"""
        from agents.vr_cricket_strategist.agent import commentator_router_agent
        
        instruction = commentator_router_agent.instruction.lower()
        # Should mention selecting commentator
        assert 'commentator' in instruction or 'pick' in instruction
    
    def test_stat_analyst_instruction(self):
        """Test that stat_analyst_agent has data reporting instructions"""
        from agents.vr_cricket_strategist.agent import stat_analyst_agent
        
        instruction = stat_analyst_agent.instruction.lower()
        # Should focus on data and stats
        assert 'data' in instruction or 'stat' in instruction
        # Should mention tools
        assert 'tool' in instruction
    
    def test_root_agent_routing_logic(self):
        """Test that orchestrator_agent has routing logic"""
        from agents.vr_cricket_strategist.agent import orchestrator_agent, identity_agent
        
        # Identity agent should handle identity
        assert 'get_current_identity' in identity_agent.instruction
        
        instruction = orchestrator_agent.instruction
        # Should mention identity is established
        assert 'identity' in instruction.lower()
        # Should mention routing
        assert 'route' in instruction.lower() or 'delegate' in instruction.lower()


class TestAgentDependencies:
    """Tests for agent dependencies and relationships"""
    
    def test_all_agents_have_model(self):
        """Test that all LLM agents have a model configured"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder_agent, tactician_agent, boycott_writer_agent, sidhu_writer_agent,
            nasser_writer_agent, harsha_writer_agent, commentator_router_agent, 
            stat_analyst_agent, orchestrator_agent, generic_responder_agent
        )
        
        # Main agents should have model_config
        agents_with_model = [
            fact_finder_agent, tactician_agent, boycott_writer_agent, sidhu_writer_agent,
            nasser_writer_agent, harsha_writer_agent, commentator_router_agent,
            stat_analyst_agent, orchestrator_agent
        ]
        for agent in agents_with_model:
            assert hasattr(agent, 'model')
            assert agent.model is not None
        
        # Generic responder agent also has a model attribute (even if empty string)
        assert hasattr(generic_responder_agent, 'model')
    
    def test_agents_share_model_config(self):
        """Test that agents share the same model configuration"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder_agent, tactician_agent, boycott_writer_agent, sidhu_writer_agent,
            nasser_writer_agent, harsha_writer_agent, commentator_router_agent,
            stat_analyst_agent, orchestrator_agent, model_config
        )
        
        # Only test agents that should have model_config
        # (generic_responder_agent doesn't have model_config)
        agents = [
            fact_finder_agent, tactician_agent, boycott_writer_agent, sidhu_writer_agent,
            nasser_writer_agent, harsha_writer_agent, commentator_router_agent,
            stat_analyst_agent, orchestrator_agent
        ]
        for agent in agents:
            assert agent.model == model_config
    
    def test_sequential_agent_workflow(self):
        """Test that sequential agent has proper workflow"""
        from agents.vr_cricket_strategist.agent import game_plan_generator_agent
        
        # Sequential agent should process sub-agents in order
        assert hasattr(game_plan_generator_agent, 'sub_agents')
        assert len(game_plan_generator_agent.sub_agents) > 0
        
        # All sub-agents should have names
        for sub_agent in game_plan_generator_agent.sub_agents:
            assert hasattr(sub_agent, 'name')
            assert sub_agent.name is not None


class TestAgentNaming:
    """Tests for agent naming conventions"""
    
    def test_agent_names_are_unique(self):
        """Test that all agents have unique names"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder_agent, tactician_agent, boycott_writer_agent, sidhu_writer_agent,
            nasser_writer_agent, harsha_writer_agent, commentator_router_agent,
            stat_analyst_agent, game_plan_generator_agent, root_agent, generic_responder_agent,
            orchestrator_agent, identity_agent
        )
        
        agents = [
            fact_finder_agent, tactician_agent, boycott_writer_agent, sidhu_writer_agent,
            nasser_writer_agent, harsha_writer_agent, commentator_router_agent,
            stat_analyst_agent, game_plan_generator_agent, root_agent, generic_responder_agent,
            orchestrator_agent, identity_agent
        ]
        names = [agent.name for agent in agents]
        
        # All names should be unique
        assert len(names) == len(set(names))
    
    def test_agent_names_are_descriptive(self):
        """Test that agent names are descriptive"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder_agent, tactician_agent, boycott_writer_agent, sidhu_writer_agent,
            nasser_writer_agent, harsha_writer_agent, commentator_router_agent,
            stat_analyst_agent, orchestrator_agent, root_agent, generic_responder_agent
        )
        
        agents_and_roles = [
            (fact_finder_agent, 'fact'),
            (tactician_agent, 'tactic'),
            (boycott_writer_agent, 'boycott'),
            (sidhu_writer_agent, 'sidhu'),
            (nasser_writer_agent, 'nasser'),
            (harsha_writer_agent, 'harsha'),
            (commentator_router_agent, 'commentator'),
            (stat_analyst_agent, 'stat'),
            (orchestrator_agent, 'coach'),
            (root_agent, 'root'),
            (generic_responder_agent, 'responder')
        ]
        
        for agent, role_keyword in agents_and_roles:
            assert role_keyword.lower() in agent.name.lower()


class TestToolIntegration:
    """Tests for tool integration with agents"""
    
    def test_tools_are_callable(self):
        """Test that all tools assigned to agents are callable"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder_agent, stat_analyst_agent, commentator_router_agent, orchestrator_agent
        )
        
        agents_with_tools = [fact_finder_agent, stat_analyst_agent, commentator_router_agent, orchestrator_agent]
        
        for agent in agents_with_tools:
            for tool in agent.tools:
                assert callable(tool), f"Tool {tool} is not callable"
    
    def test_no_duplicate_tools_per_agent(self):
        """Test that agents don't have duplicate tools"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder_agent, stat_analyst_agent, commentator_router_agent, orchestrator_agent
        )
        
        agents_with_tools = [fact_finder_agent, stat_analyst_agent, commentator_router_agent, orchestrator_agent]
        
        for agent in agents_with_tools:
            tool_names = [tool.__name__ for tool in agent.tools]
            # Check for duplicates
            assert len(tool_names) == len(set(tool_names)), \
                f"Agent {agent.name} has duplicate tools"

