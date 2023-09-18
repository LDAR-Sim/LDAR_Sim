# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        methods.init_func.repair_delay
# Purpose:     Generates the repair delays
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------

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
