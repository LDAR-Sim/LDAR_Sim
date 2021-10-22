# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim initialization.sims
# Purpose:     Create and package simulations
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
import pickle
from copy import deepcopy
from initialization.preseed import gen_seed_timeseries
from initialization.sites import generate_sites, regenerate_sites


def create_sims(sim_params, programs, generator_dir, in_dir, out_dir, input_manager):
    # Store params used to generate the pickle files for change detection
    input_manager.write_parameters(generator_dir / 'parameters.yaml')
    n_simulations = sim_params['n_simulations']
    pregen_leaks = sim_params['pregenerate_leaks']
    preseed_random = sim_params['preseed_random']
    simulations = []
    for i in range(n_simulations):
        if pregen_leaks:
            file_loc = generator_dir / "pregen_{}_{}.p".format(i, 0)
            # If there is no pregenerated file for the program
            if not os.path.isfile(file_loc):
                sites, leak_timeseries, initial_leaks = generate_sites(programs[0], in_dir)
        else:
            sites, leak_timeseries, initial_leaks = [], [], []
        if preseed_random:
            seed_timeseries = gen_seed_timeseries(sim_params)
        else:
            seed_timeseries = None

        for j in range(len(programs)):
            if pregen_leaks:
                file_loc = generator_dir / "pregen_{}_{}.p".format(i, j)
                if os.path.isfile(file_loc):
                    # If there is a  pregenerated file for the program
                    generated_data = pickle.load(open(file_loc, "rb"))
                    sites = generated_data['sites']
                    leak_timeseries = generated_data['leak_timeseries']
                    initial_leaks = generated_data['initial_leaks']
                    seed_timeseries = generated_data['seed_timeseries']
                else:
                    # Different programs can have different site level parameters ie survey
                    # frequency,so re-evaluate selected sites with new parameters
                    sites = regenerate_sites(programs[j], sites, in_dir)
                    pickle.dump({
                        'sites': sites, 'leak_timeseries': leak_timeseries,
                        'initial_leaks': initial_leaks, 'seed_timeseries': seed_timeseries},
                        open(file_loc, "wb"))
            else:
                sites = []

            opening_message = "Simulating program {} of {} ; simulation {} of {}".format(
                j + 1, len(programs), i + 1, n_simulations
            )
            simulations.append(
                [{'i': i, 'program': deepcopy(programs[j]),
                  'globals':sim_params,
                  'input_directory': in_dir,
                  'output_directory':out_dir,
                  'opening_message': opening_message,
                  'pregenerate_leaks': pregen_leaks,
                  'print_from_simulation': sim_params['print_from_simulations'],
                  'sites': sites,
                  'leak_timeseries': leak_timeseries,
                  'initial_leaks': initial_leaks,
                  'seed_timeseries': seed_timeseries,
                  }])
    return simulations
