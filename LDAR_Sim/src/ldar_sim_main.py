# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim main
# Purpose:     Interface for parameterizing and running LDAR-Sim.
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


import datetime
import multiprocessing as mp
import os
import sys
import shutil
from pathlib import Path

from config.output_flag_mapping import OUTPUTS, TIMESERIES, SITES, LEAKS, BATCH_REPORTING
from economics.cost_mitigation import cost_mitigation
from initialization.args import files_from_args, get_abs_path
from initialization.input_manager import InputManager
from initialization.sims import create_sims
from initialization.sites import init_generator_files
from ldar_sim_run import ldar_sim_run
from out_processing.batch_reporting import BatchReporting
from utils.generic_functions import check_ERA5_file

opening_msg = """
You are running LDAR-Sim version 3.0.0 an open sourced software (MIT) license.
Provide any issues, comments, questions, or recommendations by
adding an issue to https://github.com/LDAR-Sim/LDAR_Sim.git.

"""

if __name__ == '__main__':
    print(opening_msg)

    # Get route directory, which is parent folder of ldar_sim_main file
    # Set current working directory directory to root directory
    root_dir = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    src_dir = root_dir / 'src'
    sys.path.insert(1, str(src_dir))
    ext_sens_dir = root_dir / 'external_sensors'
    sys.path.append(str(ext_sens_dir))

    # --- Retrieve input parameters and parse ---
    parameter_filenames = files_from_args(root_dir)
    input_manager = InputManager()
    if 'out_dir' in parameter_filenames:
        sim_params = input_manager.read_and_validate_parameters(
            parameter_filenames['parameter_files'])
        out_dir = get_abs_path(parameter_filenames['out_dir'])
    else:
        sim_params = input_manager.read_and_validate_parameters(
            parameter_filenames)
        out_dir = get_abs_path(sim_params['output_directory'])

    # --- Assign local variabls
    ref_program = sim_params['reference_program']
    base_program = sim_params['baseline_program']
    in_dir = get_abs_path(sim_params['input_directory'])
    programs = sim_params.pop('programs')
    virtual_world = sim_params.pop('virtual_world')

    # --- Run Checks ----
    check_ERA5_file(in_dir, virtual_world)
    has_ref = ref_program in programs
    has_base = base_program in programs

    # --- Setup Output folder
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    input_manager.write_parameters(out_dir / 'parameters.yaml')

    # If leak generator is used and there are generated files, user is prompted
    # to use files, If they say no, the files will be removed
    if sim_params['pregenerate_leaks']:
        generator_dir = in_dir / "generator"
        init_generator_files(
            generator_dir, input_manager.simulation_parameters, in_dir, virtual_world)
    else:
        generator_dir = None
    # --- Create simulations ---
    simulations = create_sims(sim_params, programs, virtual_world,
                              generator_dir, in_dir, out_dir)

    # --- Run simulations (in parallel) --
    with mp.Pool(processes=sim_params['n_processes']) as p:
        sim_outputs = p.starmap(ldar_sim_run, simulations)

    # ---- Generate Outputs ----

    # Do batch reporting
    print("....Generating output data")
    if (sim_params[OUTPUTS][BATCH_REPORTING] and
        (sim_params[OUTPUTS][SITES] and
            sim_params[OUTPUTS][LEAKS] and
            sim_params[OUTPUTS][TIMESERIES])):
        # Create a data object...
        if has_ref & has_base:
            print("....Generating cost mitigation outputs")
            cost_mitigation = cost_mitigation(
                sim_outputs, ref_program, base_program, out_dir)
            reporting_data = BatchReporting(
                out_dir, sim_params['start_date'], ref_program, base_program)
            if sim_params['n_simulations'] > 1:
                reporting_data.program_report()
                if len(programs) > 1:
                    print("....Generating program comparison plots")
                    reporting_data.batch_report()
                    reporting_data.batch_plots()
        else:
            print(
                'No reference or base program input...skipping batch reporting and economics.')

    # Write program metadata
    metadata = open(out_dir / '_metadata.txt', 'w')
    metadata.write(str(programs) + '\n' +
                   str(datetime.datetime.now()))

    metadata.close()
