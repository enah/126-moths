import random

def simulate(initial_state, prob_white=0.9, max_steps=10000, fraction=True):
    """
    Returns True if white moths are completely eliminated within max_steps;
    False if gray moths are eliminated. If fraction=True, returns fraction of 
    gray moths if no absorbing state is reached. Otherwise, returns False 
    unless all moths turn grey.

    initial_state: A dictionary mapping genotypes (strings) to initial 
        numbers of moths of that genotype.
    prob_white: The probability that a white moth is killed during
        the state transition phase.
    max_steps: The maximum allowed time steps.
    fraction: If true, the function returns the final fraction of grey moths. 
        If false, the function returns whether or not all moths are grey. 
    """
    pop_size = sum([initial_state[genotype] for genotype in initial_state])
   
    curr_state = initial_state
    for step in range(1, max_steps + 1):
        curr_state = transition(curr_state, pop_size, prob_white)
        if all_gg(curr_state):
            return True # Eliminated white moths
        elif all_ww(curr_state):
            return False 
    return curr_state['gg'] / pop_size if fraction else False

def transition(curr_state, pop_size, prob_white):
    """
    Takes in a current state and returns a new state 
    after one moth has been born and one has died.

    p_w: The probability that a white moth is killed in 
    the death phase.
    
    """
    new_state = dict(curr_state)
    child = new_child(curr_state, pop_size)
    new_state[child] += 1

    dead_moth = kill_moth(new_state, prob_white)
    new_state[dead_moth] -= 1

    return new_state 

def all_gg(state):
    """
    Returns True if the white allele has been eliminated.
    """
    return state['wg'] == 0 and state['ww'] == 0

def all_ww(state):
    """
    Returns True if the gray allele has been eliminated.
    """
    return state['wg'] == 0 and state['gg'] == 0

def random_moth(state, pop_size):
    """
    Returns a string in {'ww', 'wg', 'gg'}, representing a 
    random moth from the population in state.
    """
    x = random.randint(0, pop_size - 1)
    if x < state['ww']:
        return 'ww'
    elif x < state['ww'] + state['wg']:
        return 'wg'
    return 'gg'

def new_child(state, pop_size):
    """
    Returns a string in {'ww', 'wg', 'gg'} representing 
    a child born to two random parents from the population in state.
    """
    parent1, parent2 = random_moth(state, pop_size), random_moth(state, pop_size)
    child = random.choice(parent1) + random.choice(parent2)
    if child == 'gw':
        child = 'wg' # avoiding KeyErrors
    return child

def kill_moth(state, prob_white):
    """
    Returns a string in {'ww', 'wg', 'gg'} representing a moth to kill. 
    Moth is white with prob_white, gray with 1 - prob_white.
    """
    if state['gg'] == 0 or random.random() < prob_white:
        total_white = state['ww'] + state['wg']
        if random.randint(0, total_white - 1) < state['ww']:
            return 'ww'
        return 'wg'
    return 'gg'