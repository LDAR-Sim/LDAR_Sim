#------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim) 
# File:        Generic functions
# Purpose:     Generic functions for running LDAR-Sim.
#
# Copyright (C) 2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#    
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#------------------------------------------------------------------------------

import numpy as np

def gap_calculator (condition_vector):
    """
    This function calculates max gaps between daily activites in a time series.
    Requires only a single binary vector describing whether a condition was met.
    """
    
    # Find the index of all days in which the condition is true
    max_gap = None
    indices = np.where(condition_vector == True)
    
    # If there are no condition days, max_gap equals the vector length
    if len(indices[0]) == 0:
        max_gap = len(condition_vector)

    # If there is only one condition day, get max_gap
    elif len(indices[0]) == 1:
        start_gap = indices[0][0]   
        end_gap = len(condition_vector) - indices[0][0]
        max_gap = max(start_gap, end_gap)
        
    # If there are multiple condition days, calculate longest gap   
    elif len(indices[0] > 1):  
        start_gap = indices[0][0]   
        mid_gap = max(abs(x - y) for (x, y) in zip(indices[0][1:], indices[0][:-1]))
        end_gap = len(condition_vector) - indices[0][-1]
        max_gap = max(start_gap, mid_gap, end_gap)
        
    return (max_gap)

