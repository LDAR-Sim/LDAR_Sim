# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim run
# Purpose:     Main simulation sequence
#
# Copyright (C) 2018-2021  Intelligent Methane Monitoring and Management System (IM3S) Group
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
import copy

from numpy import random as np_rand
import random as rand
from weather.weather_lookup import WeatherLookup as WL
from weather.weather_lookup_hourly import WeatherLookup as WL_h
from ldar_sim import LdarSim
from time_counter import TimeCounter
from stdout_redirect import stdout_redirect
from utils.distributions import unpackage_dist as unpack_leak_dist


def ldar_sim_run(simulation):
    """
    The ldar sim run function takes a simulation dictionary
    simulation = a dictionary of simulation parameters necessary to run LDAR-Sim
    """
    # i = simulation['i']
    simulation = copy.deepcopy(simulation)
    parameters = simulation['program']
    parameters['input_directory'] = simulation['input_directory']
    parameters['output_directory'] = simulation['output_directory'] / parameters['program_name']
    parameters['pregenerate_leaks'] = simulation['pregenerate_leaks']
    parameters['leak_timeseries'] = simulation['leak_timeseries']
    parameters['initial_leaks'] = simulation['initial_leaks']
    parameters['seed_timeseries'] = simulation['seed_timeseries']
    parameters['sites'] = simulation['sites']
    global_params = simulation['globals']

    if not os.path.exists(parameters['output_directory']):
        try:
            os.makedirs(parameters['output_directory'])
        except Exception:
            pass

    logfile = open(parameters['output_directory'] / 'logfile.txt', 'w')
    if 'print_from_simulation' not in simulation or simulation['print_from_simulation']:
        sys.stdout = stdout_redirect([sys.stdout, logfile])
    else:
        sys.stdout = stdout_redirect([logfile])

    gc.collect()
    print(simulation['opening_message'])
    parameters['simulation'] = str(simulation['i'])

    # --------- Leak distributions -------------
    if len(parameters['leak_timeseries']) < 1:
        unpack_leak_dist(parameters, parameters['input_directory'])

        # ------------------------------------------------------------------------------
        # -----------------------Initialize dynamic model state-------------------------

    state = {
        't': None,
        'operator': None,  # operator gets assigned during initialization
        'methods': [],  # list of methods in action
        'sites': parameters['sites'],   # sites in the simulation
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
    if 'weather_is_hourly' in parameters and parameters['weather_is_hourly']:
        state['weather'] = WL_h(state, parameters)
    else:
        state['weather'] = WL(state, parameters)
    state['t'] = TimeCounter(parameters)
    parameters.update({'timesteps': state['t'].timesteps})
    sim = LdarSim(global_params, state, parameters, timeseries)

    # Loop through timeseries
    while state['t'].current_date <= state['t'].end_date:
        np_rand.seed(parameters['seed_timeseries'][state['t'].current_timestep])
        rand.seed(parameters['seed_timeseries'][state['t'].current_timestep])
        sim.update()
        state['t'].next_day()

    # Clean up and write files
    sim_summary = sim.finalize()
    logfile.close()
    return (sim_summary)
