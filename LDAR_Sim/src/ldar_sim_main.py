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


import os
import shutil
import datetime
import multiprocessing as mp
from pathlib import Path
from initialization.sims import create_sims
from initialization.sites import init_generator_files
from initialization.input_manager import InputManager
from initialization.args import files_from_args, get_abs_path
from utils.generic_functions import check_ERA5_file
from batch_reporting import BatchReporting
from ldar_sim_run import ldar_sim_run
from economics.cost_mitigation import cost_mitigation

if __name__ == '__main__':
    # Get route directory , which is parent folder of ldar_sim_main file
    # Set current working directory directory to root directory
    root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
    os.chdir(root_dir)
    parameter_filenames = files_from_args(root_dir)
    input_manager = InputManager()
    sim_params = input_manager.read_and_validate_parameters(parameter_filenames)
    ref_program = sim_params['reference_program']
    base_program = sim_params['baseline_program']
    # Assign appropriate local variables to match older way of inputting parameters
    in_dir = get_abs_path(sim_params['input_directory'])
    out_dir = get_abs_path(sim_params['output_directory'])
    programs = sim_params.pop('programs')

    temp_w_file = ""
    for p in programs:
        if p['weather_file'] != temp_w_file:
            # Check whether ERA5 data is already in the input directory and download data if not
            check_ERA5_file(in_dir, p['weather_file'])
            temp_w_file = p['weather_file']

    has_ref = True
    if len([p['program_name'] for p in programs if p['program_name'] == ref_program]) < 1:
        print('Missing reference program...continuing')
        no_ref = False

    has_base = True
    if len([p['program_name'] for p in programs if p['program_name'] == base_program]) < 1:
        print('Missing baseline program...continuing')
        no_base = False

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    # record input parameters as an output
    input_manager.write_parameters(out_dir / 'parameters.yaml')
    # If leak generator is used and there are generated files, user is prompted
    # to use files, If they say no, the files will be removed
    if sim_params['pregenerate_leaks']:
        generator_dir = in_dir / "generator"
        init_generator_files(generator_dir, input_manager.simulation_parameters)
    simulations = create_sims(sim_params, programs, generator_dir, in_dir, out_dir, input_manager)

    # --- Debugging ---
    # The following can be used for debugging outside of the starmap
    # trg_sim_idx = next((index for (index, d) in enumerate(simulations)
    #                     if d[0]['program']['program_name'] == "P_air"), None)
    # ldar_sim_run(simulations[trg_sim_idx][0])

    # --- Run simulations (in parallel) --
    with mp.Pool(processes=sim_params['n_processes']) as p:
        sim_outputs = p.starmap(ldar_sim_run, simulations)

    # Do batch reporting
    if sim_params['write_data']:
        # Create a data object...
        if has_ref & has_base:
            cost_mitigation = cost_mitigation(sim_outputs, ref_program, base_program, out_dir)
            reporting_data = BatchReporting(
                out_dir, sim_params['start_date'], ref_program, base_program)
            if sim_params['n_simulations'] > 1:
                reporting_data.program_report()
                if len(programs) > 1:
                    reporting_data.batch_report()
                    reporting_data.batch_plots()
        else:
            print('No reference or base program input...skipping batch reporting and economics.')

    # Write program metadata
    metadata = open(out_dir / '_metadata.txt', 'w')
    metadata.write(str(programs) + '\n' +
                   str(datetime.datetime.now()))

    metadata.close()
