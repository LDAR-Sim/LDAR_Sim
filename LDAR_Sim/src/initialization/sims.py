# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.sims
# Purpose:     Create and package simulations
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


import os
import pickle
from copy import deepcopy

from initialization.preseed import gen_seed_timeseries
from initialization.sites import generate_sites, regenerate_sites


def create_sims(sim_params, programs, virtual_world, generator_dir, in_dir, out_dir):
    # Store params used to generate the pickle files for change detection
    n_simulations = sim_params['n_simulations']
    pregen_leaks = sim_params['pregenerate_leaks']
    preseed_random = sim_params['preseed_random']
    base_prog = sim_params['baseline_program']
    simulations = []
    for i in range(n_simulations):
        if pregen_leaks:
            file_loc = generator_dir / "pregen_{}_{}.p".format(i, base_prog)
            # If there is no pregenerated file for the virtual world
            if not os.path.isfile(file_loc):
                sites, leak_timeseries, initial_leaks = generate_sites(
                    virtual_world,
                    in_dir,
                    pregen_leaks,
                    sim_params['start_date'],
                    sim_params['end_date']
                )
        else:
            sites, leak_timeseries, initial_leaks = [], [], []
        if preseed_random:
            seed_timeseries = gen_seed_timeseries(sim_params)
        else:
            seed_timeseries = None
        for pidx, p in programs.items():
            if pregen_leaks:
                file_loc = generator_dir / "pregen_{}_{}.p".format(i, pidx)
                if os.path.isfile(file_loc):
                    # If there is a pregenerated file for the virtual world
                    generated_data = pickle.load(open(file_loc, "rb"))
                    sites = generated_data['sites']
                    leak_timeseries = generated_data['leak_timeseries']
                    initial_leaks = generated_data['initial_leaks']
                    seed_timeseries = generated_data['seed_timeseries']
                else:
                    sites = regenerate_sites(virtual_world, sites, in_dir)
                    pickle.dump({
                        'sites': sites, 'leak_timeseries': leak_timeseries,
                        'initial_leaks': initial_leaks, 'seed_timeseries': seed_timeseries},
                        open(file_loc, "wb"))
            else:
                sites = []

            opening_message = "Simulating program: {} ; simulation {} of {}".format(
                pidx, i + 1, n_simulations
            )
            closing_message = "Finished simulating program {} ; simulation {} of {} ".format(
                pidx, i + 1, n_simulations)
            simulations.append(
                [{'i': i, 'program': deepcopy(programs[pidx]),
                  'simulation_settings':sim_params,
                  'virtual_world': virtual_world,
                  'input_directory': in_dir,
                  'output_directory':out_dir,
                  'opening_message': opening_message,
                  'closing_message': closing_message,
                  'pregenerate_leaks': pregen_leaks,
                  'print_from_simulation': sim_params['print_from_simulations'],
                  'sites': sites,
                  'leak_timeseries': leak_timeseries,
                  'initial_leaks': initial_leaks,
                  'seed_timeseries': seed_timeseries,
                  }])
    return simulations
