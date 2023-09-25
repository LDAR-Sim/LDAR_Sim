# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim run
# Purpose:     Main simulation sequence
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

import copy
import gc
# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------
import os
import random as rand
import sys
from datetime import datetime, timedelta

from initialization.sites import get_subtype_dist
from numpy import random as np_rand
from stdout_redirect import stdout_redirect
from time_counter import TimeCounter
from weather.weather_lookup import WeatherLookup as WL
from weather.weather_lookup_hourly import WeatherLookup as WL_h

from ldar_sim import LdarSim


def ldar_sim_run(simulation):
    """
    The ldar sim run function takes a simulation dictionary
    simulation = a dictionary of simulation parameters necessary to run LDAR-Sim
    """
    # i = simulation['i']
    simulation = copy.deepcopy(simulation)
    virtual_world = simulation['virtual_world']
    program_parameters = simulation['program']
    input_directory = simulation['input_directory']
    output_directory = simulation['output_directory'] / \
        program_parameters['program_name']
    virtual_world['pregenerate_leaks'] = simulation['pregenerate_leaks']
    virtual_world['leak_timeseries'] = simulation['leak_timeseries']
    virtual_world['initial_leaks'] = simulation['initial_leaks']
    virtual_world['seed_timeseries'] = simulation['seed_timeseries']
    virtual_world['sites'] = simulation['sites']
    simulation_settings = simulation['simulation_settings']
    simulation_settings['batch_run'] = simulation['batch_run']

    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)
        except Exception:
            pass

    logfile = open(output_directory / 'logfile.txt', 'w')
    if 'print_from_simulation' not in simulation or simulation['print_from_simulation']:
        sys.stdout = stdout_redirect([sys.stdout, logfile])
    else:
        sys.stdout = stdout_redirect([logfile])
    gc.collect()
    print(simulation['opening_message'])
    virtual_world['simulation'] = str(simulation['i'])

    # --------- Leak distributions -------------
    if len(virtual_world['leak_timeseries']) < 1:
        get_subtype_dist(virtual_world, input_directory)

    # --------------------------------------
    # --- Initialize dynamic model state ---
    state = {
        't': None,
        'operator': None,  # operator gets assigned during initialization
        'methods': [],  # list of methods in action
        'sites': virtual_world['sites'],   # sites in the simulation
        'flags': [],  # list of sites flagged for follow-up
        # 'leaks': [],  # list of all current leaks
        'tags': [],  # leaks that have been tagged for repair
        'weather': None,  # weather gets assigned during initialization
        'daylight': None,  # daylight hours calculated during initialization
        # 'init_leaks': [],  # the initial leaks generated at timestep 1
        'max_leak_rate': None,  # the largest leak in the input file
        'site_visits': {},
    }

    # ------------------------Initialize timeseries data----------------------------

    timeseries = {
        'datetime': [],
        'active_leaks': [],
        'new_leaks': [],
        'n_tags': [],
        'rolling_cost_estimate': [],
        'rolling_cost_estimate_b': [],
        'cum_repaired_leaks': [],
        'daily_emissions_kg': []
    }

    # -----------------------------Run simulations----------------------------------

    # Initialize objects
    if 'weather_is_hourly' in virtual_world and virtual_world['weather_is_hourly']:
        state['weather'] = WL_h(state, virtual_world, input_directory)
    else:
        state['weather'] = WL(state, virtual_world, input_directory)
    state['t'] = TimeCounter(simulation_settings['start_date'], simulation_settings['end_date'])
    virtual_world.update({'timesteps': state['t'].timesteps})
    sim = LdarSim(
        simulation_settings,
        state,
        program_parameters,
        virtual_world,
        timeseries,
        input_directory,
        output_directory
    )
    start_date = datetime(*simulation_settings['start_date'])
    # Loop through timeseries
    for ts in range(state['t'].timesteps):
        state['t'].current_timestep = ts
        state['t'].current_date = start_date + timedelta(days=ts)
        if virtual_world['seed_timeseries']:
            np_rand.seed(virtual_world['seed_timeseries']
                         [state['t'].current_timestep])
            rand.seed(virtual_world['seed_timeseries']
                      [state['t'].current_timestep])
        sim.update()

    # Clean up and write files
    sim_summary = sim.finalize()
    print(simulation['closing_message'])
    logfile.close()
    return (sim_summary)
