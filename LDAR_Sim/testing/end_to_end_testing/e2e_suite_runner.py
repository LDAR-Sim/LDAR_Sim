# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        End-to-End Test Suite Runner
# Purpose:     Interface for running LDAR-Sim End-to-End test.
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

import multiprocessing as mp
import os
import shutil
import sys
import gc
import pandas as pd
from pathlib import Path
from datetime import date
from testing_utils.result_verification import compare_outputs

# Get directories and set up root
e2e_test_dir: Path = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir: Path = e2e_test_dir.parent.parent
src_dir: Path = root_dir / "src"
tests_dir: Path = e2e_test_dir / "test_suite"
os.chdir(root_dir)
# Add the source directory to the import file path to import all LDAR-Sim modules
sys.path.insert(1, str(src_dir))

if __name__ == "__main__":
    from constants.error_messages import Runtime_Error_Messages as rem
    from constants.file_name_constants import Output_Files, Generator_Files
    from constants.output_messages import RuntimeMessages as rm
    import constants.param_default_const as pdc
    from file_processing.input_processing.input_manager import InputManager
    from file_processing.output_processing.summary_output_helpers import get_non_baseline_prog_names
    from file_processing.output_processing.summary_output_manager import SummaryOutputManager
    from file_processing.output_processing.summary_visualization_manager import (
        SummaryVisualizationManager,
    )
    from initialization.args import files_from_path, get_abs_path
    from initialization.initialize_emissions import initialize_emissions, read_in_emissions
    from initialization.initialize_infrastructure import initialize_infrastructure
    from initialization.preseed import gen_seed_emis
    from ldar_sim_run import simulate
    from utils.generic_functions import check_ERA5_file
    from utils.prog_method_measured_func import (
        set_up_tf_method_deployed_df,
        filter_deployment_tf_by_program_methods,
    )
    from virtual_world.infrastructure import Infrastructure
    from weather.daylight_calculator import DaylightCalculatorAve
    from weather.weather_lookup import WeatherLookup as WL

    GLOBAL_PARAMS_TO_REP: "dict[str, Any]" = {
        pdc.Sim_Setting_Params.SIMS: 2,
        pdc.Sim_Setting_Params.PRESEED: True,
        pdc.Sim_Setting_Params.INPUT: "./inputs",
        pdc.Sim_Setting_Params.OUTPUT: "./outputs",
    }

    GLOBAL_OUTPUT_PARAMS: "dict[str, Any]" = {
        pdc.Output_Params.PROGRAM_VISUALIZATIONS: {
            pdc.Output_Params.SINGLE_PROGRAM_TIMESERIES: False
        }
    }

    # Get root directory , which is parent folder of ldar_sim_main file
    # Set current working directory directory to root directory
    # --- Retrieve input parameters and parse ---
    for test in os.scandir(tests_dir):
        if test.is_dir():
            print(f"Running test: {test.name}")
            test_dir: Path = Path(os.path.normpath(test))
            params_dir = test_dir / "params"
            parameter_filenames = files_from_path(params_dir)
            input_manager = InputManager()
            sim_params = input_manager.read_and_validate_parameters(parameter_filenames)
            # --- Overwrite certain parameters for end-to-end testing ---
            for key, value in GLOBAL_PARAMS_TO_REP.items():
                sim_params[key] = value
            # --- Assign local variabls
            in_dir = get_abs_path(sim_params[pdc.Sim_Setting_Params.INPUT], test_dir)
            out_dir = get_abs_path(sim_params[pdc.Sim_Setting_Params.OUTPUT], test_dir)
            base_program = sim_params[pdc.Sim_Setting_Params.BASELINE]
            programs = sim_params.pop(pdc.Levels.PROGRAM)
            virtual_world = sim_params.pop(pdc.Levels.VIRTUAL)
            output_params = sim_params.pop(pdc.Levels.OUTPUTS)
            preseed_random = sim_params[pdc.Sim_Setting_Params.PRESEED]
            expected_results = test_dir / "expected_outputs"

            # -- Overwrite certain output params for end-to-end testing --
            for key, value in GLOBAL_OUTPUT_PARAMS.items():
                output_params[key] = value

            methods = {
                method: programs[program][pdc.Levels.METHOD][method]
                for program in programs
                for method in programs[program][pdc.Program_Params.METHODS]
            }

            # --- Run Checks ----
            check_ERA5_file(in_dir, virtual_world)
            has_base: bool = base_program in programs

            if not (has_base):
                print(rem.NO_BASE_PROG_ERROR)
                sys.exit()

            # -- Setup Output folder --
            if os.path.exists(out_dir):
                shutil.rmtree(out_dir)
            os.makedirs(out_dir)
            input_manager.write_parameters(out_dir / Output_Files.PARAMETER_FILE)

            generator_dir = in_dir / Generator_Files.GENERATOR_FOLDER
            if os.path.exists(generator_dir):
                print(rm.GEN_WARNING_MSG)
            print(rm.INIT_INFRA)
            simulation_count: int = sim_params[pdc.Sim_Setting_Params.SIMS]
            emis_preseed_val: list[int] = None
            force_remake_gen: bool = False
            if preseed_random:
                emis_preseed_val, force_remake_gen = gen_seed_emis(simulation_count, generator_dir)
            infrastructure: Infrastructure
            hash_file_exist: bool
            site_measured: pd.DataFrame = set_up_tf_method_deployed_df(
                methods, virtual_world[pdc.Virtual_World_Params.N_SITES]
            )
            infrastructure, hash_file_exist = initialize_infrastructure(
                methods,
                programs,
                virtual_world,
                generator_dir,
                in_dir,
                preseed_random,
                emis_preseed_val,
                force_remake_gen,
            )
            infrastructure.gen_site_measured_tf_data(
                methods,
                site_measured,
            )
            print(rm.INIT_EMISS)
            # Pregenerate emissions
            seed_timeseries = initialize_emissions(
                simulation_count,
                preseed_random,
                emis_preseed_val,
                hash_file_exist,
                infrastructure,
                date(*virtual_world[pdc.Virtual_World_Params.START_DATE]),
                date(*virtual_world[pdc.Virtual_World_Params.END_DATE]),
                generator_dir,
            )
            # Initialize objects
            print(rm.INIT_WEATHER)
            weather = WL(virtual_world, in_dir)
            infrastructure.set_weather_index(weather)
            print(rm.INIT_DAYLIGHT)
            daylight = DaylightCalculatorAve(
                infrastructure.get_site_avrg_lat_lon(),
                date(*virtual_world[pdc.Virtual_World_Params.START_DATE]),
                date(*virtual_world[pdc.Virtual_World_Params.END_DATE]),
            )
            # Calculate the simulation years
            simulation_years: list[int] = [
                year
                for year in range(
                    virtual_world[pdc.Virtual_World_Params.START_DATE][0],
                    virtual_world[pdc.Virtual_World_Params.END_DATE][0] + 1,
                )
            ]
            # Initialize output managers
            summary_stats_manager: SummaryOutputManager = SummaryOutputManager(
                output_path=out_dir,
                output_config=output_params,
                sim_years=simulation_years,
                programs=programs,
            )
            summary_visualization_manager: SummaryVisualizationManager = (
                SummaryVisualizationManager(
                    output_config=output_params,
                    output_dir=out_dir,
                    baseline_program=base_program,
                    site_count=virtual_world[pdc.Virtual_World_Params.N_SITES],
                )
            )
            n_process = sim_params[pdc.Sim_Setting_Params.PROCESS]
            if len(programs) < sim_params[pdc.Sim_Setting_Params.PROCESS]:
                n_process = len(programs)
            with mp.Manager() as manager:
                lock = manager.Lock()
                for simulation_number in range(simulation_count):
                    print(rm.SIM_SET.format(simulation_number=simulation_number))
                    # read in pregen emissions
                    infra = read_in_emissions(infrastructure, generator_dir, simulation_number)
                    # -- Run simulations --
                    prog_data = []
                    for program in programs:
                        meth_params = {}
                        prog_measured_df = filter_deployment_tf_by_program_methods(
                            site_measured, programs[program][pdc.Program_Params.METHODS]
                        )
                        for meth in programs[program][pdc.Program_Params.METHODS]:
                            meth_params[meth] = methods[meth]
                        prog_data.append(
                            (
                                daylight,
                                weather,
                                simulation_number,
                                program,
                                meth_params,
                                programs[program],
                                sim_params,
                                virtual_world,
                                output_params,
                                infra,
                                in_dir,
                                out_dir,
                                seed_timeseries,
                                lock,
                                prog_measured_df,
                            )
                        )

                    with mp.Pool(processes=n_process) as p:
                        _ = p.starmap(
                            simulate,
                            prog_data,
                        )
                    gc.collect()
                    print(rm.FIN_SIM_SET.format(simulation_number=simulation_number))

                # -- Batch Report --
                print(rm.BATCH_CLEAN.format(batch_count=0))
                summary_stats_manager.gen_summary_outputs(False)
                non_baseline_progs = get_non_baseline_prog_names(programs, base_program)
                summary_stats_manager.gen_cost_summary_outputs(non_baseline_progs)
            # Compare results to expected
            compare_outputs(test.name, out_dir, expected_results)
