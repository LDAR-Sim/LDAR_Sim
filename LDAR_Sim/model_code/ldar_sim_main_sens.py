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
from pathlib import Path

from ldar_sim_run import ldar_sim_run
# from copy import deepcopy
# import pandas as pd
import os
import copy
import datetime
import multiprocessing as mp
from argparse import ArgumentParser, RawTextHelpFormatter
from input_manager import InputManager
from utils.result_processing import get_emis_ratios
from generic_functions import check_ERA5_file
from initialization.sites import generate_sites, regenerate_sites
from utils.sensitivity import yaml_to_dict, set_from_keylist

if __name__ == '__main__':
    root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
    # ------------------------------------------------------------------------------
    # Look for parameter files supplied as arguments - if parameter files are supplied as
    # arguments, proceed to parse and type check input parameter type with the input manager
    # will also accept flagged input directory , (-P or --in_dir)
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
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

    data = yaml_to_dict(input_directory / 'sens_vars.yaml')

    work_prac_var = data['work_prac_var']
    virt_world_vars = data['virt_world_vars']
    new_progs = []
    prev_progs_names = set()

    if len(work_prac_var) > 0:
        # Go through ensitivity progs
        var_paths = [path.split(".") for path in work_prac_var['paths']]
        # Get program names and the their associated index in programs object
        for val in work_prac_var['vals']:
            for path in var_paths:
                for (pidx, p) in enumerate(programs):
                    if p["program_name"] == path[0] or path[0].lower() == '__all':
                        prev_progs_names.add(path[0])
                        tmp_prog = copy.deepcopy(programs[pidx])
                        set_from_keylist(tmp_prog, path[1:], val)
                new_progs.append(tmp_prog)
        if pregen_leaks:
            sites, leak_timeseries, initial_leaks = generate_sites(programs[0], input_directory)
        for prog in list(prev_progs_names):
            prog_idx = next((idx for (idx, p) in enumerate(
                programs) if p["program_name"] == prog), None)
            programs.pop(prog_idx)
        programs += new_progs
    # Check whether ERA5 data is already in the working directory and download data if not
    for p in programs:
        check_ERA5_file(input_directory, p['weather_file'])

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    def run_programs(programs, n_simulations, output_directory,
                     sites=[], leak_timeseries=[], initial_leaks=[]):
        # Set up simulation parameter files
        simulations = []
        for i in range(n_simulations):
            if pregen_leaks:
                sites, leak_timeseries, initial_leaks = generate_sites(
                    programs[0], input_directory)
            for j in range(len(programs)):
                if pregen_leaks:
                    sites = regenerate_sites(programs[j], sites, input_directory)
                opening_message = "Simulating program {} of {} ; simulation {} of {}".format(
                    j + 1, len(programs), i + 1, n_simulations
                )
                simulations.append(
                    [{'i': i, 'program': copy.deepcopy(programs[j]),
                      'globals':simulation_parameters,
                      'input_directory': input_directory,
                      'output_directory':output_directory,
                      'opening_message': opening_message,
                      'pregenerate_leaks': pregen_leaks,
                      'print_from_simulation': print_from_simulations,
                      'sites': sites,
                      'leak_timeseries': leak_timeseries,
                      'initial_leaks': initial_leaks,
                      }])

        # Perform simulations in parallel
        with mp.Pool(processes=n_processes) as p:
            res = p.starmap(ldar_sim_run, simulations)
        metadata = open(output_directory / 'metadata.txt', 'w')
        metadata.write(str(programs) + '\n' + str(datetime.datetime.now()))
        metadata.close()
        return res

    #  ----------Run Program Routine-------------
    all_progs = []
    if len(virt_world_vars) == 0:
        # If prog_var_manip is unused run program with parameters in Program Files
        programs, n_simulations, output_directory,
        sites = [], leak_timeseries = [], initial_leaks = []

        all_progs['base'] = run_programs(
            programs, ref_program, n_simulations, write_data, output_directory)
    else:
        for virt_world_var in virt_world_vars:
            sim_progs = []
            var_paths = [path.split(".") for path in virt_world_var['paths']]
            # Get program names and the their associated index in programs object
            key = path[0][-1]
            for val in virt_world_var['vals']:
                munip_progs = copy.deepcopy(programs)
                for path in var_paths:
                    for (idx, p) in enumerate(munip_progs):
                        if p["program_name"] == path[0] or path[0].lower() == '__all':
                            set_from_keylist(munip_progs[idx], path[1:], val)
                print('------ running {} : {} --------'.format(path, val))
                prog_outdir = output_directory / '{}/{}/'.format(key, val)
                if not os.path.exists(prog_outdir):
                    os.makedirs(prog_outdir)
                prog_results = run_programs(munip_progs, n_simulations, prog_outdir,
                                            sites, leak_timeseries, initial_leaks)
                for prog in prog_results:
                    prog.update({'key': key, 'value': val})
                sim_progs += prog_results
            alt_ts = get_emis_ratios(sim_progs, ['daily_emissions_kg'])
            xxx = 10
