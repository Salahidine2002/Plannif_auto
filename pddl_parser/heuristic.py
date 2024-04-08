import random

def h(state, act, goal_pos, goal_not):
    # Calculate the heuristic
    return random.randint(0, 10)


def g(state, act, initial_state):
    # Calculate the uniform cost
    return random.randint(0, 10)