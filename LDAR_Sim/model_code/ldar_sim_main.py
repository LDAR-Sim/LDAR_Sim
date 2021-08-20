# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim main
# Purpose:     Interface for parameterizing and running LDAR-Sim.
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

import multiprocessing as mp
import warnings
import datetime
import shutil
import os
import pandas as pd
import argparse
from argparse import RawTextHelpFormatter

from ldar_sim_run import ldar_sim_run
from batch_reporting import BatchReporting
from pathlib import Path
from input_manager import InputManager
from generic_functions import check_ERA5_file

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
        programs = simulation_parameters['programs']
        n_processes = simulation_parameters['n_processes']
        print_from_simulations = simulation_parameters['print_from_simulations']
        n_simulations = simulation_parameters['n_simulations']
        spin_up = simulation_parameters['spin_up']
        ref_program = simulation_parameters['reference_program']
        write_data = simulation_parameters['write_data']
        weather_file = simulation_parameters['weather_file']
        start_year = simulation_parameters['start_year']

    else:
        print('LDAR-Sim using parameters coded into ldar_sim_main.py')
        print('Warning: this method of supplying parameters will be depreciated in the future')
        # ------------------------------------------------------------------------------
        # -----------------------------Global parameters--------------------------------

        input_directory = root_dir / "inputs_template"
        output_directory = root_dir / "outputs"
        # Programs to compare; Position one should be the reference program (P_ref)
        program_list = ['P_ref', 'P_base']

        # -----------------------------Set up programs----------------------------------
        programs = []

        warnings.filterwarnings('ignore')    # Temporarily mute warnings

        for p in range(len(program_list)):
            file = input_directory / '{}.txt'.format(program_list[p])
            exec(open(file).read())
            programs.append(eval(program_list[p]))

        n_processes = programs[0]['n_processes']
        print_from_simulations = programs[0]['print_from_simulations']
        n_simulations = programs[0]['n_simulations']
        spin_up = programs[0]['spin_up']
        ref_program = program_list[0]
        write_data = programs[0]['write_data']
        weather_file = programs[0]['weather_file']
        start_year = programs[0]['start_year']

    # -----------------------------Prepare model run----------------------------------
    # Check whether ERA5 data is already in the input directory and download data if not
    check_ERA5_file(input_directory, weather_file)

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory)
    if 'input_manager' in locals():
        input_manager.write_parameters(output_directory / 'parameters.yaml')

    # Set up simulation parameter files
    simulations = []
    for i in range(n_simulations):
        for j in range(len(programs)):
            opening_message = "Simulating program {} of {} ; simulation {} of {}".format(
                j + 1, len(programs), i + 1, n_simulations
            )
            simulations.append(
                [{'i': i, 'program': programs[j],
                  'input_directory': input_directory,
                  'output_directory':output_directory,
                  'opening_message': opening_message,
                  'print_from_simulation': print_from_simulations}])

    # ldar_sim_run(simulations[4][0])
    # Perform simulations in parallel
    with mp.Pool(processes=n_processes) as p:
        res = p.starmap(ldar_sim_run, simulations)

    # Do batch reporting
    if write_data:
        # Create a data object...
        reporting_data = BatchReporting(
            output_directory, start_year,
            spin_up, ref_program)
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

