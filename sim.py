import random

def simulate(initial_state, prob_white_death=0.8, max_steps=10000):
    """
    Returns the number of time steps it takes to get absorbed 
    into the state where all moths are gg; if it instead gets
    absorbed into the state where all moths are ww, it returns False
    """
    pop_size = sum([initial_state[genotype] for genotype in initial_state])
   
    curr_state = initial_state
    for step in range(1, max_steps + 1):
        curr_state = transition(curr_state, pop_size, prob_white_death)
        if all_gg(curr_state):
            return step
        elif all_ww(curr_state):
            return False
    return False

def all_gg(state):
    return state['wg'] == 0 and state['ww'] == 0

def all_ww(state):
    return state['wg'] == 0 and state['gg'] == 0

def random_moth(state, pop_size):
    """
    Takes in a state and returns a string in ('ww', 'wg', 'gg')
    that represents a randomly chosen moth from that population.
    """
    x = random.randint(0, pop_size - 1)
    if x < state['ww']:
        return 'ww'
    elif x < state['ww'] + state['wg']:
        return 'wg'
    return 'gg'

def new_child(state, pop_size):
    """
    Takes in a state and returns a string in ('ww', 'wg', 'gg') that
    represents a child born to two randomly chosen parents from that population.
    """
    parent1, parent2 = random_moth(state, pop_size), random_moth(state, pop_size)
    child = random.choice(parent1) + random.choice(parent2)
    if child == 'gw':
        child = 'wg' # avoiding KeyErrors
    return child

def kill_moth(state, prob_white):
    """
    Takes in a state and returns a string in ('ww', 'wg', 'gg') that
    represents a moth to be killed. White moths are killed with 
    prob_white, gray moths with 1 - prob_white.
    """
    if state['gg'] == 0 or random.random() < prob_white:
        total_white = state['ww'] + state['wg']
        if random.randint(0, total_white - 1) < state['ww']:
            return 'ww'
        return 'wg'
    return 'gg'

def transition(curr_state, pop_size, p_w):
    """
    Takes in a current state and returns a new state 
    after one moth has been born and one has died.
    """
    new_state = dict(curr_state)
    child = new_child(curr_state, pop_size)
    new_state[child] += 1

    dead_moth = kill_moth(new_state, p_w)
    new_state[dead_moth] -= 1

    return new_state 