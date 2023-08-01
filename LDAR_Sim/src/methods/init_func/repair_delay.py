import numpy as np
import random


def determine_delay(virtual_world):
    """
        Generates the repair delay
            default: Expects a single value
            list: grabs a random value from a list of possibilities
            distribution: generates a value from a distribution
        Arg: virtual_world parameter dictionary
        Returns:
            Static Repair delay value based on different functions
    """
    # add in compatibility with previous versions
    if type(virtual_world['repair_delay']) == int:
        delay = virtual_world['repair_delay']
    elif virtual_world['repair_delay']['type'] == 'default':
        delay = virtual_world['repair_delay']['val'][0]
    elif virtual_world['repair_delay']['type'] == 'list':
        list_len = len(virtual_world['repair_delay']['val'])
        delay_ind = random.randint(0, list_len-1)
        delay = virtual_world['repair_delay']['val'][delay_ind]
    elif virtual_world['repair_delay']['type'] == 'distribution':
        delay = np.random.lognormal(
            virtual_world['repair_delay']['val'][0], virtual_world['repair_delay']['val'][1])

    return delay
