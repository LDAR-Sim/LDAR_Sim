# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim run
# Purpose:     Main simulation sequence
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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
# ------------------------------------------------------------------------------

from weather_lookup import *
from ldar_sim import *
from time_counter import *
from batch_reporting import *
import gc

def ldar_sim_run (simulation):
    """
    The ldar sim run function takes a simulation dictionary
    simulation = a dictionary of simulation parameters necessary to run LDAR-Sim
    """
    i = simulation['i']
    parameters = simulation['program']
    parameters['working_directory'] = simulation['wd']

    gc.collect ()
    print (simulation['opening_message'])

    parameters['simulation'] = str (simulation['i'])

    # ------------------------------------------------------------------------------
    # -----------------------Initialize dynamic model state-------------------------

    state = {
        't': None,
        'operator': None,  # operator gets assigned during initialization
        'methods': [],  # list of methods in action
        'sites': [],  # sites in the simulation
        'flags': [],  # list of sites flagged for follow-up
        'leaks': [],  # list of all current leaks
        'tags': [],  # leaks that have been tagged for repair
        'weather': None,  # weather gets assigned during initialization
        'daylight': None,  # daylight hours calculated during initialization
        'init_leaks': [],  # the initial leaks generated at timestep 1
        'empirical_vents': [0],  # vent distribution created during initialization
        'max_rate': None  # the largest leak in the input file
    }

    # ------------------------Initialize timeseries data----------------------------

    timeseries = {
        'datetime': [],
        'active_leaks': [],
        'new_leaks': [],
        'n_tags': [],
        'cum_repaired_leaks': [],
        'daily_emissions_kg': []
    }

    # -----------------------------Run simulations----------------------------------

    # Initialize objects
    state['weather'] = WeatherLookup (state, parameters)
    state['t'] = TimeCounter (parameters)
    sim = LdarSim (state, parameters, timeseries)

    # Loop through timeseries
    while state['t'].current_date <= state['t'].end_date:
        sim.update ()
        state['t'].next_day ()

    # Clean up and write files
    sim.finalize ()
    return
