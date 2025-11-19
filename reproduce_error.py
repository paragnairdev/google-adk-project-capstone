import asyncio
import os
import sys
from dotenv import load_dotenv
from agents.vr_cricket_coach.agent import cricket_coach_app

load_dotenv()

# Ensure Gemini API (not Vertex AI) is used
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

async def run_test():
    print("Testing 'hi' message with cricket_coach_app...")
    try:
        # Create a session
        session_id = "test_session"
        
        # Simulate a user message
        user_message = "hi"
        
        print(f"Sending message: {user_message}")
        
        # App.process_message or similar?
        # Let's inspect the App object or try to run it.
        # Usually apps are run by a server.
        # But we might be able to invoke the agent directly.
        
        root_agent = cricket_coach_app.root_agent
        
        # We need to mock the invocation context if we call agent directly.
        # Or use a runner.
        
        # Let's try to use the agent's __call__ or invoke method if possible.
        # But ADK agents are complex.
        
        # Alternative: Check if there is a CLI runner in ADK.
        # But I don't know the API.
        
        # Let's try to inspect the root_agent object.
        print(f"Root agent: {root_agent}")
        
        # If I can't run it easily, I'll focus on the code logic.
        # But let's try to run it.
        
        # Assuming there is a way to run it.
        # Maybe: response = await root_agent(user_message)
        
        # Let's try to import a runner.
        from google.adk.runners import AgentRunner
        
        runner = AgentRunner(agent=root_agent)
        response = await runner.run(user_message, session_id=session_id)
        print(f"Response: {response}")

    except Exception as e:
        print(f"Caught exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
