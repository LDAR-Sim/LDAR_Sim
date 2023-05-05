# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        End-to-End Test Suite Runner
# Purpose:     Interface for running LDAR-Sim End-to-End test.
#
# Copyright (C) 2018-2023  Intelligent Methane Monitoring and Management System (IM3S) Group
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
import pickle
import shutil
import sys
import yaml
from pathlib import Path
from pandas import read_csv
# Get directories and set up root
e2e_test_dir: Path = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir: Path = e2e_test_dir.parent.parent
src_dir: Path = root_dir / 'src'
tests_dir: Path = e2e_test_dir / 'test_suite'
os.chdir(root_dir)
# Add the source directory to the import file path to import all LDAR-Sim modules
sys.path.insert(1, str(src_dir))

if __name__ == '__main__':
    from initialization.args import files_from_path, get_abs_path
    from initialization.input_manager import InputManager, NoAliasDumper
    from initialization.sims import create_sims
    from initialization.sites import init_generator_files
    from ldar_sim_run import ldar_sim_run
    from utils.generic_functions import check_ERA5_file
    from out_processing.batch_reporting import BatchReporting
    from out_processing.prog_table import generate as gen_prog_table
    # Get root directory , which is parent folder of ldar_sim_main file
    # Set current working directory directory to root directory

    # --- Retrieve input parameters and parse ---
    for test in os.scandir(tests_dir):
        print(test)
        test_dir: Path = Path(os.path.normpath(test) + '/params')
        parameter_filenames = files_from_path(test_dir)
        input_manager = InputManager()
        sim_params = input_manager.read_and_validate_parameters(
            parameter_filenames)

        # --- Assign local variabls
        ref_program = sim_params['reference_program']
        base_program = sim_params['baseline_program']
        in_dir = get_abs_path(sim_params['input_directory'], test_dir)
        out_dir = get_abs_path(sim_params['output_directory'], test_dir)
        programs = sim_params.pop('programs')
        generator_dir = in_dir / "generator"

        # --- Run Checks ----
        check_ERA5_file(in_dir, programs)
        has_ref: bool = ref_program in programs
        has_base: bool = base_program in programs

        # --- Setup Output folder
        # //TODO remove test dir at end of loop
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)

        # merging all parameter files
        if programs[sim_params['baseline_program']]['subtype_file']:
            param_dict_w_subtype = {**{'globals': sim_params}, ** {'subtype': read_csv(
                in_dir/programs[sim_params['baseline_program']]['subtype_file']).to_dict()}}
        else:
            param_dict_w_subtype = {
                **{'globals': sim_params}, ** {'subtype': None}}
        param_dict_all = {**param_dict_w_subtype, **{'programs': programs}}

        # Save parameters for comparison
        input_manager.write_parameters(out_dir / 'parameters.yaml')

        # --- Create simulations ---
        simulations = create_sims(sim_params, programs,
                                  generator_dir, in_dir, out_dir, input_manager)

        # --- Run simulations (in parallel) --
        n_processes = sim_params['n_processes']
        if n_processes > 1:
            with mp.Pool(processes=n_processes) as p:
                sim_outputs = p.starmap(ldar_sim_run, simulations)
        else:
            sim_outputs = [ldar_sim_run(simulation[0]) for simulation in simulations]
        print("Done runing simulations...")
        print("Processing outputs...")
        # --- Process Outputs ---
        prog_leaks = leaks_process(
            sim_outputs, cache_dir, sim_params['baseline_program'])
        prog_ts = ts_process(sim_outputs, sim_params, cache_dir)
        prog_sites = sites_process(sim_outputs, cache_dir)
        pickle.dump(prog_sites, open(cache_dir / "sites.p", "wb"))

        # # Do batch reporting
        # print("....Generating output data")
        # if sim_params['write_data']:
        #     # Create a data object...
        #     if has_ref & has_base:
        #         # print("....Generating cost mitigation outputs")
        #         # cost_mitigation = cost_mitigation(sim_outputs, ref_program, base_program, out_dir)
        #         reporting_data = BatchReporting(
        #             out_dir, sim_params['start_date'], ref_program, base_program)
        #         if sim_params['n_simulations'] > 1:
        #             reporting_data.program_report()
        #             if len(programs) > 1:
        #                 print("....Generating program comparison plots")
        #                 reporting_data.batch_report()
        #                 reporting_data.batch_plots()
        #     else:
        #         print(
        #             'No reference or base program input...skipping batch reporting and economics.')

        # meta = {
        #     'n_sites': len(sim_outputs[0]['sites']),
        #     'n_days': len(sim_outputs[0]['timeseries']),
        #     'n_leaks': len(sim_outputs[0]['leaks']),
        #     'pregen_leaks': sim_params['pregenerate_leaks'],
        #     'reference_program': sim_params['reference_program'],
        #     'baseline_program': sim_params['baseline_program']}
        # pickle.dump(meta, open(cache_dir / "meta.p", "wb"))

        # # Write program metadata
        # metadata = open(out_dir / '_metadata.txt', 'w')
        # metadata.write(str(programs) + '\n' +
        #                str(datetime.datetime.now()))

        # metadata.close()
