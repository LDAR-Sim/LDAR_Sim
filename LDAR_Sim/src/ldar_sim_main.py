# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim main
# Purpose:     Interface for parameterizing and running LDAR-Sim.
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

import fnmatch
import pickle
import argparse
import os
import shutil
import datetime
import multiprocessing as mp

from initialization.sites import generate_sites, regenerate_sites
from initialization.preseed import gen_seed_timeseries
from generic_functions import check_ERA5_file
from input_manager import InputManager
from pathlib import Path
from batch_reporting import BatchReporting
from ldar_sim_run import ldar_sim_run
from copy import deepcopy
from argparse import RawTextHelpFormatter


if __name__ == '__main__':
    # Get route directory , which is parent folder of ldar_sim_main file
    # Set current working directory directory to root directory
    root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
    # ------------------------------------------------------------------------------
    # Look for parameter files supplied as arguments - if parameter files are supplied as
    # arguments, proceed to parse and type check input parameter type with the input manager
    # will also accept flagged input directory , (-P or --in_dir)
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    # ---Declare input arguments---
    parser.add_argument(
        'in_files', type=str, nargs='*',
        help='Input files, seperate with space, can be absolute path or relative to' +
        'root directory (LDAR_Sim). All files should have yaml, yml, or json extensions \n' +
        'ie. python ldar_sim_main.py ./file1.json c:/path/to/file/file2.json')
    parser.add_argument(
        "-P", "--in_dir",
        help='Input Directory, folder containing input files, will input all files within' +
        'folder that have yaml, yml or json extensions \n' +
        'ie. python ldar_sim_main.py --in_dir ./folder_with_infiles')
    args = parser.parse_args()

    if args.in_dir is not None:
        # if an input directory is specified, get all files within that are in the directory
        in_dir = root_dir / args.in_dir
        # Get all yaml or json files in specified folder
        parameter_filenames = [
            "{}/{}".format(args.in_dir, f) for f in os.listdir(in_dir)
            if ".yaml" in f or ".yml" in f or ".json" in f]
    else:
        parameter_filenames = args.in_files

    if len(parameter_filenames) > 0:
        print('LDAR-Sim using parameters supplied as arguments')
        input_manager = InputManager(root_dir)
        simulation_parameters = input_manager.read_and_validate_parameters(parameter_filenames)
        # Assign appropriate local variables to match older way of inputting parameters
        input_directory = simulation_parameters['input_directory']
        output_directory = simulation_parameters['output_directory']
        programs = simulation_parameters.pop('programs')
        n_processes = simulation_parameters['n_processes']
        print_from_simulations = simulation_parameters['print_from_simulations']
        n_simulations = simulation_parameters['n_simulations']
        ref_program = simulation_parameters['reference_program']
        write_data = simulation_parameters['write_data']
        start_date = simulation_parameters['start_date']
        pregen_leaks = simulation_parameters['pregenerate_leaks']
        preseed_random = simulation_parameters['preseed_random']

    else:
        print('LDAR-Sim using parameters coded into ldar_sim_main.py')
        print('Warning: this method of supplying parameters will be depreciated in the future')
        # ------------------------------------------------------------------------------
        # -----------------------------Global parameters--------------------------------

        input_directory = root_dir / "inputs"
        output_directory = root_dir / "outputs"
        # Programs to compare; Position one should be the reference program (P_ref)
        program_list = ['P_ref', 'P_base']

        # -----------------------------Set up programs----------------------------------
        programs = []

        for p in range(len(program_list)):
            file = input_directory / '{}.txt'.format(program_list[p])
            exec(open(file).read())
            programs.append(eval(program_list[p]))

        n_processes = programs[0]['n_processes']
        print_from_simulations = programs[0]['print_from_simulations']
        n_simulations = programs[0]['n_simulations']
        ref_program = program_list[0]
        write_data = programs[0]['write_data']
        start_date = programs[0]['start_date']

    # -----------------------------Prepare model run----------------------------------
    # Check whether ERA5 data is already in the input directory and download data if not
    for p in programs:
        check_ERA5_file(input_directory, p['weather_file'])

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)
    if 'input_manager' in locals():
        input_manager.write_parameters(output_directory / 'parameters.yaml')

    # If leak generator is used and there are generated files, user is prompted
    # to use files, If they say no, the files will be removed
    if pregen_leaks:
        generator_folder = input_directory / "./generator"
        if not os.path.exists(generator_folder):
            os.mkdir(generator_folder)
        gen_files = fnmatch.filter(os.listdir(generator_folder), '*.p')
        if len(gen_files) > 0:
            print('\n --- \n pregenerated data exists, do you want to use (y/n)?' +
                  ' "n" will remove contents of generated data folder.')
            gen_prompt = input()
            if gen_prompt.lower() == 'n':
                for file in gen_files:
                    os.remove(generator_folder / file)
    simulations = []

    for i in range(n_simulations):
        if pregen_leaks:
            file_loc = generator_folder / "pregen_{}_{}.p".format(i, 0)
            # If there is no pregenerated file for the program
            if not os.path.isfile(file_loc):
                sites, leak_timeseries, initial_leaks = generate_sites(programs[0], input_directory)
        else:
            sites, leak_timeseries, initial_leaks = [], [], []
        if preseed_random:
            seed_timeseries = gen_seed_timeseries(simulation_parameters)
        else:
            seed_timeseries = None

        for j in range(len(programs)):
            if pregen_leaks:
                file_loc = generator_folder / "pregen_{}_{}.p".format(i, j)
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
                    sites = regenerate_sites(programs[j], sites, input_directory)
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
                  'globals':simulation_parameters,
                  'input_directory': input_directory,
                  'output_directory':output_directory,
                  'opening_message': opening_message,
                  'pregenerate_leaks': pregen_leaks,
                  'print_from_simulation': print_from_simulations,
                  'sites': sites,
                  'leak_timeseries': leak_timeseries,
                  'initial_leaks': initial_leaks,
                  'seed_timeseries': seed_timeseries,
                  }])

    # The following can be used for debugging outside of the starmap
    # ldar_sim_run(simulations[0][0])
    trg_sim_idx = next((index for (index, d) in enumerate(simulations)
                       if d[0]['program']['program_name'] == "P_air_dev"), None)

    # ldar_sim_run(simulations[trg_sim_idx][0])
    # Perform simulations in parallel
    with mp.Pool(processes=n_processes) as p:
        res = p.starmap(ldar_sim_run, simulations)

    # Do batch reporting
    if write_data:
        # Create a data object...
        reporting_data = BatchReporting(
            output_directory, start_date, ref_program)
        if n_simulations > 1:
            reporting_data.program_report()
            if len(programs) > 1:
                reporting_data.batch_report()
                reporting_data.batch_plots()

    # Write metadata
    metadata = open(output_directory / '_metadata.txt', 'w')
    metadata.write(str(programs) + '\n' +
                   str(datetime.datetime.now()))

    metadata.close()
