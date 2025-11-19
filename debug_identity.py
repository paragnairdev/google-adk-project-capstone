import asyncio
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from agents.vr_cricket_coach.agent import identity_agent

load_dotenv()
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

async def test_identity_agent():
    print("Testing IdentityAgent...")
    
    # We need to run the agent.
    # LlmAgent doesn't have a simple 'run' method that takes text directly without a runner?
    # Let's check available methods on identity_agent.
    print(f"Agent type: {type(identity_agent)}")
    print(f"Agent name: {identity_agent.name}")
    
    # We can try to use the internal _process_turn if accessible, but better to use a runner.
    # Since I couldn't import AgentRunner before, let's try to find where it is.
    
    # Let's list the google.adk package contents if possible.
    # Or just try to inspect the agent object to see how to invoke it.
    
    # If we can't run it, we can at least check the instructions and tools.
    
    # Let's try to manually invoke the tool it uses.
    from agents.vr_cricket_coach.agent import get_player_identity
    
    class MockContext:
        def __init__(self):
            self.state = {}
            
    ctx = MockContext()
    print(f"Tool result (empty state): {get_player_identity(ctx)}")
    
    ctx.state["user:player_name"] = "Karthik"
    print(f"Tool result (with state): {get_player_identity(ctx)}")

if __name__ == "__main__":
    asyncio.run(test_identity_agent())
