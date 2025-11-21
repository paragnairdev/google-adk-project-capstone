"""
Callback functions for the VR Cricket Strategist agent.

This module implements the Circuit Breaker pattern to prevent infinite agent loops.

Design Pattern: Circuit Breaker
- Monitors agent invocations for duplicate inputs
- Tracks per-agent retry counts in session state
- Breaks execution after threshold to prevent resource exhaustion
- Provides graceful degradation by injecting override instructions

Why This Matters:
In multi-agent systems, routing errors can cause "ping-pong" loops where agents
continuously transfer requests back and forth. Without intervention, these loops:
1. Consume API quota rapidly
2. Create poor user experience (long waits, no response)
3. Mask underlying routing logic errors

The circuit breaker detects these patterns and stops execution gracefully.
"""

# ============================================================================
# CONFIGURATION
# ============================================================================
MAX_RETRIES_ON_SAME_INPUT = 5  # Stop after 5 duplicate inputs to same agent


# ============================================================================
# CIRCUIT BREAKER IMPLEMENTATION
# ============================================================================
async def circuit_breaker(callback_context):
    """
    Prevents infinite agent routing loops by detecting duplicate inputs.
    
    Implementation Details:
    This callback runs BEFORE each agent invocation (before_agent_callback).
    It compares the current input against the last input this agent received.
    
    Behavior:
    1. First invocation: Records input, allows execution
    2. Subsequent invocations with NEW input: Resets counter, allows execution
    3. Duplicate input detected: Increments counter, allows execution (with warning)
    4. Counter exceeds threshold: Injects override instruction, breaks loop
    
    State Management:
    Uses ADK session state to track:
    - last_input_{agent_name}: Last input string seen by this agent
    - retry_count_{agent_name}: Number of consecutive duplicate inputs
    
    Design Decision: We track state per-agent rather than globally because
    different agents may legitimately receive similar inputs in a workflow.
    Only repeated inputs to the SAME agent indicate a loop.
    
    Args:
        callback_context: ADK callback context containing agent and session info
    """
    # Access session and agent information from callback context
    try:
        session = callback_context._invocation_context.session
        agent_name = callback_context.agent.name
        
        # Extract and normalize input for comparison
        inputs = getattr(callback_context, 'inputs', {})
        # Convert to string to handle both dict and string inputs uniformly
        current_input_str = str(inputs)
        
    except AttributeError:
        # Graceful degradation: If context structure is unexpected, skip check
        # This ensures the callback doesn't break agent execution
        return

    state = session.state
    
    # Define session state keys (namespaced by agent to avoid collisions)
    last_input_key = f"last_input_{agent_name}"
    retry_count_key = f"retry_count_{agent_name}"
    
    # Retrieve historical state for this agent
    last_input = state.get(last_input_key, "")
    current_retries = state.get(retry_count_key, 0)
    
    # Loop Detection: Compare current input against last input
    if current_input_str == last_input:
        # DUPLICATE DETECTED: Same input received multiple times
        current_retries += 1
        print(f"🔄 Loop Warning: {agent_name} received duplicate input (Count: {current_retries})")
        
        # Behavior: Allow execution to continue but track the repeat
        # This handles legitimate retries (e.g., tool failures) while
        # still monitoring for problematic patterns
    else:
        # NEW INPUT: Reset the loop detection counter
        current_retries = 0
        # Update last input to current for next comparison
        state[last_input_key] = current_input_str
    
    # Persist updated retry count to session
    state[retry_count_key] = current_retries

    # Circuit Breaker Activation: Break the loop when threshold exceeded
    if current_retries > MAX_RETRIES_ON_SAME_INPUT:
        print(f"🚨 CIRCUIT BREAKER: Stopping {agent_name} after {current_retries} duplicate inputs.")
        
        # Override Strategy: Inject emergency instructions into agent
        # This modifies the agent's behavior mid-execution to force a stop
        error_instruction = (
            "\n\nSYSTEM OVERRIDE: You are in an infinite routing loop. "
            "You have received the exact same request multiple times. "
            "STOP. Do NOT transfer to another agent. "
            "Apologize to the user and ask for clarification."
        )
        
        # Append override to agent's existing instructions
        # The agent will prioritize this override due to recency bias in LLM attention
        callback_context.agent.instruction += error_instruction
        
        # Note: We don't raise an exception here because we want the agent to
        # gracefully inform the user, not crash the entire workflow

