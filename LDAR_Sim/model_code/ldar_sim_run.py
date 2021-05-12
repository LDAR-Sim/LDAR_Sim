# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim run
# Purpose:     Main simulation sequence
#
# Copyright (C) 2018-2020  Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
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
import os
import sys
import gc
import numpy as np

from weather_lookup import WeatherLookup
from ldar_sim import LdarSim
from time_counter import TimeCounter
from stdout_redirect import stdout_redirect
from leak_processing.distributions import fit_dist


def ldar_sim_run(simulation):
    """
    The ldar sim run function takes a simulation dictionary
    simulation = a dictionary of simulation parameters necessary to run LDAR-Sim
    """
    # i = simulation['i']
    parameters = simulation['program']
    parameters['working_directory'] = simulation['wd']
    parameters['output_directory'] = os.path.join(
        simulation['output_directory'],
        parameters['program_name'])
    if not os.path.exists(parameters['output_directory']):
        os.makedirs(parameters['output_directory'])

    logfile = open(os.path.join(parameters['output_directory'], 'logfile.txt'), 'w')
    if 'print_from_simulation' not in simulation or simulation['print_from_simulation']:
        sys.stdout = stdout_redirect([sys.stdout, logfile])
    else:
        sys.stdout = stdout_redirect([logfile])

    gc.collect()
    print(simulation['opening_message'])
    parameters['simulation'] = str(simulation['i'])
    parameters['dist'] = {}
    # if "leak_rate_dist" in parameters and not parameters['use_empirical_rates'].lower():
    if "leak_rate_dist" in parameters:
        parameters['dist_type'] = parameters['leak_rate_dist'][0]
        parameters['dist_scale'] = parameters['leak_rate_dist'][1]
        parameters['dist_shape'] = parameters['leak_rate_dist'][2:-2]
        parameters['leak_rate_units'] = parameters['leak_rate_dist'][-2:]
        # lognorm is a common special case. used often for leaks. Mu is is commonly
        # provided to discribe leak which is ln(dist_scale). For this type the model
        # accepts mu in place of scale.
        if parameters['dist_type'] == 'lognorm':
            parameters['dist_scale'] = np.exp(parameters['dist_scale'])
        parameters['leak_distribution'] = fit_dist(dist_type=parameters['dist_type'],
                                                   shape=parameters['dist_shape'],
                                                   scale=parameters['dist_scale'])
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
        'max_leak_rate': None  # the largest leak in the input file
    }

    # ------------------------Initialize timeseries data----------------------------

    timeseries = {
        'datetime': [],
        'active_leaks': [],
        'new_leaks': [],
        'n_tags': [],
        'rolling_cost_estimate': [],
        'cum_repaired_leaks': [],
        'daily_emissions_kg': []
    }

    # -----------------------------Run simulations----------------------------------

    # Initialize objects
    state['weather'] = WeatherLookup(state, parameters)
    state['t'] = TimeCounter(parameters)
    sim = LdarSim(state, parameters, timeseries)

    # Loop through timeseries
    while state['t'].current_date <= state['t'].end_date:
        sim.update()
        state['t'].next_day()

    # Clean up and write files
    sim_summary = sim.finalize()
    logfile.close()
    return (sim_summary)
