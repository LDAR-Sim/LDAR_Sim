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


import datetime
import json
import multiprocessing as mp
import os
import shutil
from pathlib import Path

from economics.cost_mitigation import cost_mitigation
from initialization.args import files_from_args, get_abs_path
from initialization.checks import for_program as check_for_prog
from initialization.input_manager import InputManager
from initialization.sims import create_sims
from initialization.sites import init_generator_files
from ldar_sim_run import ldar_sim_run
from out_processing.batch_reporting import BatchReporting
from out_processing.prog_table import generate as gen_prog_table
from utils.generic_functions import check_ERA5_file

opening_msg = """
You are running LDAR-Sim version 2.0 an open sourced software (MIT) license.
It is continually being developed by the University of Calgary's Intelligent
Methane Monitoring and Management System (IM3S) Group.
Provide any issues, comments, questions, or recommendations to the IM3S by
adding an issue to https://github.com/LDAR-Sim/LDAR_Sim.git.

"""

if __name__ == '__main__':
    print(opening_msg)

    # Get route directory , which is parent folder of ldar_sim_main file
    # Set current working directory directory to root directory
    root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
    os.chdir(root_dir)

    # --- Retrieve input parameters and parse ---
    parameter_filenames = files_from_args(root_dir)
    input_manager = InputManager()
    sim_params = input_manager.read_and_validate_parameters(parameter_filenames)

    # --- Assign local variabls
    ref_program = sim_params['reference_program']
    base_program = sim_params['baseline_program']
    in_dir = get_abs_path(sim_params['input_directory'])
    out_dir = get_abs_path(sim_params['output_directory'])
    programs = sim_params.pop('programs')

    # --- Run Checks ----
    check_ERA5_file(in_dir, programs)
    has_ref = check_for_prog(ref_program, programs)
    has_base = check_for_prog(base_program, programs)

    # --- Setup Output folder
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    input_manager.write_parameters(out_dir / 'parameters.yaml')

    # If leak generator is used and there are generated files, user is prompted
    # to use files, If they say no, the files will be removed
    if sim_params['pregenerate_leaks']:
        generator_dir = in_dir / "generator"
        init_generator_files(generator_dir, input_manager.simulation_parameters, in_dir)
    else:
        generator_dir = None
    # --- Create simulations ---
    simulations = create_sims(sim_params, programs, generator_dir, in_dir, out_dir, input_manager)

    # --- Run simulations (in parallel) --
    with mp.Pool(processes=sim_params['n_processes']) as p:
        sim_outputs = p.starmap(ldar_sim_run, simulations)

    # ---- Generate Outputs ----

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

    # Generate output table
    out_prog_table = gen_prog_table(sim_outputs, base_program, programs)

    with open(out_dir / 'prog_table.json', 'w') as fp:
        json.dump(out_prog_table, fp)

    # Write program metadata
    metadata = open(out_dir / '_metadata.txt', 'w')
    metadata.write(str(programs) + '\n' +
                   str(datetime.datetime.now()))

    metadata.close()
