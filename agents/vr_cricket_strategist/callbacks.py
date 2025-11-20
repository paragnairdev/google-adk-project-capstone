"""
Callback functions for the VR Cricket Strategist agent.
"""

# Configuration
MAX_RETRIES_ON_SAME_INPUT = 5  # Stop after 5 agent transfers/steps


async def circuit_breaker(callback_context):
    """
    Failsafe: Prevents an agent from processing the exact same input repeatedly.
    This detects 'Ping-Pong' loops (Root -> Agent -> Root).
    """
    # 1. Access Session & Agent Name
    try:
        session = callback_context._invocation_context.session
        agent_name = callback_context.agent.name
        
        # Extract the input text safely
        inputs = getattr(callback_context, 'inputs', {})
        # Normalize input to string for comparison (handles dicts or strings)
        current_input_str = str(inputs)
        
    except AttributeError:
        # If context structure is different, just skip safety check
        return

    state = session.state
    
    # 2. Define keys for session state
    # We store the last input seen by THIS specific agent
    last_input_key = f"last_input_{agent_name}"
    retry_count_key = f"retry_count_{agent_name}"
    
    # 3. Retrieve last input for this agent
    last_input = state.get(last_input_key, "")
    current_retries = state.get(retry_count_key, 0)
    
    # 4. Compare Logic
    if current_input_str == last_input:
        # SAME INPUT DETECTED: We are likely in a loop
        current_retries += 1
        print(f"🔄 Loop Warning: {agent_name} received duplicate input (Count: {current_retries})")
    else:
        # NEW INPUT: Reset counter
        current_retries = 0
        # Update the last input
        state[last_input_key] = current_input_str
    
    # Save the count back to state
    state[retry_count_key] = current_retries

    # 5. Trigger Break
    if current_retries > MAX_RETRIES_ON_SAME_INPUT:
        print(f"🚨 CIRCUIT BREAKER: Stopping {agent_name} after {current_retries} duplicate inputs.")
        
        error_instruction = (
            "\n\nSYSTEM OVERRIDE: You are in an infinite routing loop. "
            "You have received the exact same request multiple times. "
            "STOP. Do NOT transfer to another agent. "
            "Apologize to the user and ask for clarification."
        )
        
        # Force the instruction into the agent
        callback_context.agent.instruction += error_instruction

