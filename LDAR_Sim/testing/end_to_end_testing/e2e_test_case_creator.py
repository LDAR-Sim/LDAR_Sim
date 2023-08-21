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
import pickle
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml

GLOBAL_PARAMS_TO_REP: 'dict[str, Any]' = {
    'n_simulations': 1,
    'pregenerate_leaks': True,
    'preseed_random': True,
    'input_directory': './inputs',
    'output_directory': './outputs',
}

# Get directories and set up root
e2e_test_dir: Path = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir: Path = e2e_test_dir.parent.parent
src_dir: Path = root_dir / 'src'
test_creator_dir: Path = e2e_test_dir / "test_case_creator"
tests_dir: Path = e2e_test_dir / 'test_suite'
os.chdir(root_dir)
# Add the source directory to the import file path to import all LDAR-Sim modules
sys.path.insert(1, str(src_dir))

# Add the external sensors to the root directory
ext_sens_dir = root_dir / 'external_sensors'
sys.path.append(str(ext_sens_dir))

if __name__ == '__main__':
    from economics.cost_mitigation import cost_mitigation
    from initialization.args import files_from_path, get_abs_path
    from initialization.input_manager import InputManager
    from initialization.sims import create_sims
    from initialization.sites import init_generator_files
    from ldar_sim_run import ldar_sim_run
    from out_processing.batch_reporting import BatchReporting
    from out_processing.prog_table import generate as gen_prog_table
    from utils.generic_functions import check_ERA5_file
    from config.output_flag_mapping import OUTPUTS, SITES, LEAKS, TIMESERIES, BATCH_REPORTING

    # --- Clean out the test creator directory
    for item in os.listdir(test_creator_dir):
        item_path = os.path.join(test_creator_dir, item)

        if item != ".gitignore":
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    # --- Retrieve parameters and inputs ---
    original_inputs_dir: Path = root_dir / sys.argv[1]
    original_params_dir: Path = root_dir / sys.argv[2]
    params_dir: Path = test_creator_dir / "params"
    if original_params_dir != params_dir:
        shutil.copytree(original_params_dir, params_dir)
    test_case_dir: Path = test_creator_dir / sys.argv[3]
    if os.path.exists(test_case_dir):
        shutil.rmtree(test_case_dir)
    os.mkdir(test_case_dir)

    # --- Fix certain global parameters for end-to-end testing
    sim_settings_file: Path = params_dir / sys.argv[4]
    with open(sim_settings_file, 'r') as file:
        sim_settings = yaml.safe_load(file)

    for key, value in GLOBAL_PARAMS_TO_REP.items():
        sim_settings[key] = value

    with open(sim_settings_file, 'w') as file:
        yaml.safe_dump(sim_settings, file)

    # Parse Parameters
    parameter_filenames = files_from_path(params_dir)
    input_manager = InputManager()
    sim_params = input_manager.read_and_validate_parameters(parameter_filenames)
    out_dir = get_abs_path("./expected_outputs", test_case_dir)

    # --- Assign local variabls
    ref_program = sim_params['reference_program']
    base_program = sim_params['baseline_program']
    in_dir = get_abs_path('./inputs', test_creator_dir)
    shutil.copytree(original_inputs_dir, in_dir)
    if os.path.exists(in_dir / 'generator'):
        shutil.rmtree(in_dir / 'generator')
    programs = sim_params.pop('programs')
    virtual_world = sim_params.pop('virtual_world')

    # --- Run Checks ----
    check_ERA5_file(in_dir, virtual_world)
    has_ref: bool = ref_program in programs
    has_base: bool = base_program in programs

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
    simulations = create_sims(
        sim_params,
        programs,
        virtual_world,
        generator_dir,
        in_dir,
        out_dir
    )

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
            cost_mitigation = cost_mitigation(sim_outputs, ref_program, base_program, out_dir)
            reporting_data = BatchReporting(
                out_dir, sim_params['start_date'], ref_program, base_program)
            if sim_params['n_simulations'] > 1:
                reporting_data.program_report()
                if len(programs) > 1:
                    print("....Generating program comparison plots")
                    reporting_data.batch_report()
                    reporting_data.batch_plots()
        else:
            print('No reference or base program input...skipping batch reporting and economics.')

    # Generate output table
    print("....Exporting summary statistic tables")
    out_prog_table = gen_prog_table(sim_outputs, base_program, programs)

    with open(out_dir / 'prog_table.json', 'w') as fp:
        json.dump(out_prog_table, fp)

    # Write program metadata
    metadata = open(out_dir / '_metadata.txt', 'w')
    metadata.write(str(programs) + '\n' +
                   str(datetime.datetime.now()))

    metadata.close()

    # Write simulation outputs
    with open(out_dir / 'sim_outputs.pickle', 'wb') as sim_res:
        pickle.dump(sim_outputs, sim_res)

    os.chdir(root_dir)
    shutil.move(params_dir, test_case_dir)
    shutil.move(in_dir, test_case_dir)
    shutil.move(test_case_dir, tests_dir)
