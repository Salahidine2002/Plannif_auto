import random

def h(state, goal_pos, goal_not):
    # Calculate the heuristic
    #return random.randint(0, 10)
    """
    Calculate a heuristic value based on the difference between the current state and the goal state.

    Args:
        state: The current state represented as a dictionary of variable-value pairs.
        act: The action being considered. This parameter might not be directly used in this simplistic heuristic but is included for compatibility.
        goal_pos: The positive goals as a dictionary of variable-value pairs that should be present for the goal to be achieved.
        goal_not: The negative goals as a dictionary of variable-value pairs that should not be present for the goal to be achieved.

    Returns:
        An integer representing the heuristic cost of reaching the goal state from the current state.
    """
    # Initialize the heuristic value to 0
    h_value = 0
    
    
    # For each positive goal condition, increase the heuristic value if it is not already satisfied in the current state
    for condition in goal_pos:
        if condition not in state:
            h_value += 1
            
    # For each negative goal condition (if applicable), increase the heuristic value if the condition is present in the current state
    for condition in goal_not:
        if condition in state:
            h_value += 1
            
    return h_value


def g(path_cost, state, action, next_state):
    # Calculate the uniform cost
    return path_cost+1
