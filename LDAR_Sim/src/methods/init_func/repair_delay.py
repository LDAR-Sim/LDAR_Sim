import numpy as np
import random


def determine_delay(program):
    """
        Generates the repair delay
            default: Expects a single value
            list: grabs a random value from a list of possiblities
            distribution: generates a value from a distribution
        Arg: program parameter dictionary
        Returns:
            Static Repair delay value based on different functions
    """
    if program['repair_delay']['type'] == 'default':
        delay = program['repair_delay']['val'][0]
    elif program['repair_delay']['type'] == 'list':
        list_len = len(program['repair_delay']['val'])
        delay_ind = random.randint(0, list_len-1)
        delay = program['repair_delay']['val'][delay_ind]
    elif program['repair_delay']['type'] == 'distribution':
        delay = np.random.lognormal(
            program['repair_delay']['val'][0], program['repair_delay']['val'][1])

    return delay
