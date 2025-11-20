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
        """Test that fact_finder agent is defined"""
        from agents.vr_cricket_strategist.agent import fact_finder
        assert fact_finder is not None
    
    def test_fact_finder_configuration(self):
        """Test fact_finder agent configuration"""
        from agents.vr_cricket_strategist.agent import fact_finder
        
        assert fact_finder.name == "FactFinder"
        assert hasattr(fact_finder, 'model')
        assert hasattr(fact_finder, 'tools')
        # Should have tools for data retrieval
        assert len(fact_finder.tools) > 0
    
    def test_fact_finder_tools(self):
        """Test that fact_finder has correct tools"""
        from agents.vr_cricket_strategist.agent import fact_finder
        
        # Should have get_head_to_head and get_venue_trends
        tool_names = [tool.__name__ for tool in fact_finder.tools]
        assert 'get_head_to_head' in tool_names
        assert 'get_venue_trends' in tool_names
    
    def test_tactician_exists(self):
        """Test that tactician agent is defined"""
        from agents.vr_cricket_strategist.agent import tactician
        assert tactician is not None
    
    def test_tactician_configuration(self):
        """Test tactician agent configuration"""
        from agents.vr_cricket_strategist.agent import tactician
        
        assert tactician.name == "Tactician"
        assert hasattr(tactician, 'model')
        assert hasattr(tactician, 'instruction')
        # Tactician should have strategic decision logic
        assert 'strategy' in tactician.instruction.lower() or 'decision' in tactician.instruction.lower()
    
    def test_writer_agents_exist(self):
        """Test that all writer agents are defined"""
        from agents.vr_cricket_strategist.agent import (
            boycott_writer, sidhu_writer, nasser_writer, harsha_writer
        )
        assert boycott_writer is not None
        assert sidhu_writer is not None
        assert nasser_writer is not None
        assert harsha_writer is not None
    
    def test_boycott_writer_configuration(self):
        """Test boycott_writer agent configuration"""
        from agents.vr_cricket_strategist.agent import boycott_writer
        
        assert boycott_writer.name == "BoycottWriter"
        assert hasattr(boycott_writer, 'instruction')
        # Should have Geoffrey Boycott persona
        assert 'boycott' in boycott_writer.instruction.lower()
    
    def test_sidhu_writer_configuration(self):
        """Test sidhu_writer agent configuration"""
        from agents.vr_cricket_strategist.agent import sidhu_writer
        
        assert sidhu_writer.name == "SidhuWriter"
        assert hasattr(sidhu_writer, 'instruction')
        # Should have Navjot Singh Sidhu persona
        assert 'sidhu' in sidhu_writer.instruction.lower()
    
    def test_nasser_writer_configuration(self):
        """Test nasser_writer agent configuration"""
        from agents.vr_cricket_strategist.agent import nasser_writer
        
        assert nasser_writer.name == "NasserWriter"
        assert hasattr(nasser_writer, 'instruction')
        # Should have Nasser Hussain persona
        assert 'nasser' in nasser_writer.instruction.lower()
    
    def test_harsha_writer_configuration(self):
        """Test harsha_writer agent configuration"""
        from agents.vr_cricket_strategist.agent import harsha_writer
        
        assert harsha_writer.name == "HarshaWriter"
        assert hasattr(harsha_writer, 'instruction')
        # Should have Harsha Bhogle persona
        assert 'harsha' in harsha_writer.instruction.lower()
    
    def test_commentator_router_exists(self):
        """Test that commentator_router agent is defined"""
        from agents.vr_cricket_strategist.agent import commentator_router
        assert commentator_router is not None
    
    def test_commentator_router_configuration(self):
        """Test commentator_router agent configuration"""
        from agents.vr_cricket_strategist.agent import commentator_router
        
        assert commentator_router.name == "CommentatorSelector"
        assert hasattr(commentator_router, 'tools')
        assert hasattr(commentator_router, 'sub_agents')
        # Should have pick_random_commentator tool
        tool_names = [tool.__name__ for tool in commentator_router.tools]
        assert 'pick_random_commentator' in tool_names
    
    def test_commentator_router_sub_agents(self):
        """Test that commentator_router has all writer agents"""
        from agents.vr_cricket_strategist.agent import (
            commentator_router, boycott_writer, sidhu_writer, 
            nasser_writer, harsha_writer
        )
        
        assert len(commentator_router.sub_agents) == 4
        assert boycott_writer in commentator_router.sub_agents
        assert sidhu_writer in commentator_router.sub_agents
        assert nasser_writer in commentator_router.sub_agents
        assert harsha_writer in commentator_router.sub_agents
    
    def test_stat_analyst_exists(self):
        """Test that stat_analyst agent is defined"""
        from agents.vr_cricket_strategist.agent import stat_analyst
        assert stat_analyst is not None
    
    def test_stat_analyst_configuration(self):
        """Test stat_analyst agent configuration"""
        from agents.vr_cricket_strategist.agent import stat_analyst
        
        assert stat_analyst.name == "StatAnalyst"
        assert hasattr(stat_analyst, 'tools')
        # Should have data query tools
        assert len(stat_analyst.tools) > 0
    
    def test_stat_analyst_tools(self):
        """Test that stat_analyst has correct tools"""
        from agents.vr_cricket_strategist.agent import stat_analyst
        
        tool_names = [tool.__name__ for tool in stat_analyst.tools]
        assert 'get_venue_trends' in tool_names
        assert 'get_head_to_head' in tool_names


class TestCompositeAgents:
    """Tests for composite agents"""
    
    def test_game_plan_generator_exists(self):
        """Test that game_plan_generator is defined"""
        from agents.vr_cricket_strategist.agent import game_plan_generator
        assert game_plan_generator is not None
    
    def test_game_plan_generator_type(self):
        """Test that game_plan_generator is a SequentialAgent"""
        from agents.vr_cricket_strategist.agent import game_plan_generator, SequentialAgent
        assert isinstance(game_plan_generator, SequentialAgent)
    
    def test_game_plan_generator_configuration(self):
        """Test game_plan_generator configuration"""
        from agents.vr_cricket_strategist.agent import game_plan_generator
        
        assert game_plan_generator.name == "GamePlanGenerator"
        assert hasattr(game_plan_generator, 'description')
        assert hasattr(game_plan_generator, 'sub_agents')
    
    def test_game_plan_generator_sub_agents(self):
        """Test that game_plan_generator has correct sub-agents in order"""
        from agents.vr_cricket_strategist.agent import (
            game_plan_generator, fact_finder, tactician, commentator_router
        )
        
        sub_agents = game_plan_generator.sub_agents
        assert len(sub_agents) == 3
        assert sub_agents[0] == fact_finder
        assert sub_agents[1] == tactician
        assert sub_agents[2] == commentator_router
    
    def test_root_agent_exists(self):
        """Test that root_agent is defined"""
        from agents.vr_cricket_strategist.agent import root_agent
        assert root_agent is not None
    
    def test_root_agent_configuration(self):
        """Test root_agent configuration"""
        from agents.vr_cricket_strategist.agent import root_agent
        
        assert root_agent.name == "CricketCoachOrchestrator"
        assert hasattr(root_agent, 'tools')
        assert hasattr(root_agent, 'sub_agents')
        assert hasattr(root_agent, 'instruction')
    
    def test_root_agent_tools(self):
        """Test that root_agent has identity tool"""
        from agents.vr_cricket_strategist.agent import root_agent
        
        tool_names = [tool.__name__ for tool in root_agent.tools]
        assert 'get_current_identity' in tool_names
    
    def test_root_agent_sub_agents(self):
        """Test that root_agent has correct sub-agents"""
        from agents.vr_cricket_strategist.agent import (
            root_agent, game_plan_generator, stat_analyst
        )
        
        sub_agents = root_agent.sub_agents
        assert len(sub_agents) == 2
        assert game_plan_generator in sub_agents
        assert stat_analyst in sub_agents


class TestAgentInstructions:
    """Tests for agent instructions and personas"""
    
    def test_fact_finder_instruction_content(self):
        """Test that fact_finder has appropriate instructions"""
        from agents.vr_cricket_strategist.agent import fact_finder
        
        instruction = fact_finder.instruction.lower()
        # Should mention data retrieval and not giving advice
        assert 'data' in instruction
        assert 'tool' in instruction or 'call' in instruction
    
    def test_tactician_instruction_logic(self):
        """Test that tactician has decision logic"""
        from agents.vr_cricket_strategist.agent import tactician
        
        instruction = tactician.instruction.lower()
        # Should mention decision making
        assert 'decision' in instruction or 'strategy' in instruction
    
    def test_writer_personas(self):
        """Test that writer agents have correct personas"""
        from agents.vr_cricket_strategist.agent import (
            boycott_writer, sidhu_writer, nasser_writer, harsha_writer
        )
        
        # Boycott should mention Geoffrey Boycott
        assert 'Geoffrey Boycott' in boycott_writer.instruction or 'Boycott' in boycott_writer.instruction
        # Should have characteristic phrases
        assert 'rubbish' in boycott_writer.instruction.lower() or 'rhubarb' in boycott_writer.instruction.lower()
        
        # Sidhu should have metaphorical style
        assert 'Navjot Singh Sidhu' in sidhu_writer.instruction or 'Sidhu' in sidhu_writer.instruction
        
        # Nasser should have tactical style
        assert 'Nasser Hussain' in nasser_writer.instruction or 'Nasser' in nasser_writer.instruction
        
        # Harsha should have poetic style
        assert 'Harsha Bhogle' in harsha_writer.instruction or 'Harsha' in harsha_writer.instruction
    
    def test_commentator_router_instruction(self):
        """Test that commentator_router has routing logic"""
        from agents.vr_cricket_strategist.agent import commentator_router
        
        instruction = commentator_router.instruction.lower()
        # Should mention selecting commentator
        assert 'commentator' in instruction or 'pick' in instruction
    
    def test_stat_analyst_instruction(self):
        """Test that stat_analyst has data reporting instructions"""
        from agents.vr_cricket_strategist.agent import stat_analyst
        
        instruction = stat_analyst.instruction.lower()
        # Should focus on data and stats
        assert 'data' in instruction or 'stat' in instruction
        # Should mention tools
        assert 'tool' in instruction
    
    def test_root_agent_routing_logic(self):
        """Test that root_agent has routing logic"""
        from agents.vr_cricket_strategist.agent import root_agent
        
        instruction = root_agent.instruction
        # Should mention identity check
        assert 'get_current_identity' in instruction
        # Should mention routing
        assert 'route' in instruction.lower() or 'delegate' in instruction.lower()


class TestAgentDependencies:
    """Tests for agent dependencies and relationships"""
    
    def test_all_agents_have_model(self):
        """Test that all LLM agents have a model configured"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder, tactician, boycott_writer, sidhu_writer,
            nasser_writer, harsha_writer, commentator_router, 
            stat_analyst, root_agent
        )
        
        agents = [
            fact_finder, tactician, boycott_writer, sidhu_writer,
            nasser_writer, harsha_writer, commentator_router,
            stat_analyst, root_agent
        ]
        for agent in agents:
            assert hasattr(agent, 'model')
            assert agent.model is not None
    
    def test_agents_share_model_config(self):
        """Test that agents share the same model configuration"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder, tactician, boycott_writer, sidhu_writer,
            nasser_writer, harsha_writer, commentator_router,
            stat_analyst, root_agent, model_config
        )
        
        agents = [
            fact_finder, tactician, boycott_writer, sidhu_writer,
            nasser_writer, harsha_writer, commentator_router,
            stat_analyst, root_agent
        ]
        for agent in agents:
            assert agent.model == model_config
    
    def test_sequential_agent_workflow(self):
        """Test that sequential agent has proper workflow"""
        from agents.vr_cricket_strategist.agent import game_plan_generator
        
        # Sequential agent should process sub-agents in order
        assert hasattr(game_plan_generator, 'sub_agents')
        assert len(game_plan_generator.sub_agents) > 0
        
        # All sub-agents should have names
        for sub_agent in game_plan_generator.sub_agents:
            assert hasattr(sub_agent, 'name')
            assert sub_agent.name is not None


class TestAgentNaming:
    """Tests for agent naming conventions"""
    
    def test_agent_names_are_unique(self):
        """Test that all agents have unique names"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder, tactician, boycott_writer, sidhu_writer,
            nasser_writer, harsha_writer, commentator_router,
            stat_analyst, game_plan_generator, root_agent
        )
        
        agents = [
            fact_finder, tactician, boycott_writer, sidhu_writer,
            nasser_writer, harsha_writer, commentator_router,
            stat_analyst, game_plan_generator, root_agent
        ]
        names = [agent.name for agent in agents]
        
        # All names should be unique
        assert len(names) == len(set(names))
    
    def test_agent_names_are_descriptive(self):
        """Test that agent names are descriptive"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder, tactician, boycott_writer, sidhu_writer,
            nasser_writer, harsha_writer, commentator_router,
            stat_analyst, root_agent
        )
        
        agents_and_roles = [
            (fact_finder, 'fact'),
            (tactician, 'tactic'),
            (boycott_writer, 'boycott'),
            (sidhu_writer, 'sidhu'),
            (nasser_writer, 'nasser'),
            (harsha_writer, 'harsha'),
            (commentator_router, 'commentator'),
            (stat_analyst, 'stat'),
            (root_agent, 'coach')
        ]
        
        for agent, role_keyword in agents_and_roles:
            assert role_keyword.lower() in agent.name.lower()


class TestToolIntegration:
    """Tests for tool integration with agents"""
    
    def test_tools_are_callable(self):
        """Test that all tools assigned to agents are callable"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder, stat_analyst, commentator_router, root_agent
        )
        
        agents_with_tools = [fact_finder, stat_analyst, commentator_router, root_agent]
        
        for agent in agents_with_tools:
            for tool in agent.tools:
                assert callable(tool), f"Tool {tool} is not callable"
    
    def test_no_duplicate_tools_per_agent(self):
        """Test that agents don't have duplicate tools"""
        from agents.vr_cricket_strategist.agent import (
            fact_finder, stat_analyst, commentator_router, root_agent
        )
        
        agents_with_tools = [fact_finder, stat_analyst, commentator_router, root_agent]
        
        for agent in agents_with_tools:
            tool_names = [tool.__name__ for tool in agent.tools]
            # Check for duplicates
            assert len(tool_names) == len(set(tool_names)), \
                f"Agent {agent.name} has duplicate tools"

