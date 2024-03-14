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


import multiprocessing as mp
import os
import shutil
import sys
from pathlib import Path
from typing import Any
from datetime import date
import yaml
import gc

GLOBAL_PARAMS_TO_REP: "dict[str, Any]" = {
    "n_simulations": 1,
    "pregenerate_leaks": True,
    "preseed_random": True,
    "input_directory": "./inputs",
    "output_directory": "./outputs",
}

# Get directories and set up root
e2e_test_dir: Path = Path(os.path.dirname(os.path.realpath(__file__)))
root_dir: Path = e2e_test_dir.parent.parent
src_dir: Path = root_dir / "src"
test_creator_dir: Path = e2e_test_dir / "test_case_creator"
tests_dir: Path = e2e_test_dir / "test_suite"
os.chdir(root_dir)
# Add the source directory to the import file path to import all LDAR-Sim modules
sys.path.insert(1, str(src_dir))

# Add the external sensors to the root directory
ext_sens_dir = root_dir / "external_sensors"
sys.path.append(str(ext_sens_dir))

if __name__ == "__main__":
    from initialization.initialize_infrastructure import initialize_infrastructure
    from initialization.preseed import gen_seed_emis
    from virtual_world.infrastructure import Infrastructure
    from weather.daylight_calculator import DaylightCalculatorAve
    from weather.weather_lookup import WeatherLookup as WL
    from utils.file_name_constants import PARAMETER_FILE, GENERATOR_FOLDER
    from utils.generic_functions import check_ERA5_file
    from file_processing.input_processing.input_manager import InputManager
    from initialization.args import (
        files_from_path,
        get_abs_path,
    )  # TODO: move this over to input_processing?
    from initialization.initialize_emissions import initialize_emissions, read_in_emissions
    from ldar_sim_run import simulate
    from file_processing.output_processing.multi_simulation_visualizations import (
        gen_cross_program_summary_plots,
    )
    from file_processing.output_processing.multi_simulation_outputs import (
        concat_output_data,
    )

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
    with open(sim_settings_file, "r") as file:
        sim_settings = yaml.safe_load(file)

    for key, value in GLOBAL_PARAMS_TO_REP.items():
        sim_settings[key] = value

    with open(sim_settings_file, "w") as file:
        yaml.safe_dump(sim_settings, file)

    # Parse Parameters
    parameter_filenames = files_from_path(params_dir)
    input_manager = InputManager()
    sim_params = input_manager.read_and_validate_parameters(parameter_filenames)

    # --- Assign local variabls
    ref_program = sim_params["reference_program"]
    base_program = sim_params["baseline_program"]
    in_dir = get_abs_path("./inputs", test_creator_dir)
    out_dir = get_abs_path("./expected_outputs", test_case_dir)
    shutil.copytree(original_inputs_dir, in_dir)
    if os.path.exists(in_dir / "generator"):
        shutil.rmtree(in_dir / "generator")
    programs = sim_params.pop("programs")
    virtual_world = sim_params.pop("virtual_world")
    generator_dir = in_dir / "generator"
    preseed_random = sim_params["preseed_random"]

    METHODS_ACCESSOR = "methods"
    METHOD_LABELS_ACCESSOR = "method_labels"
    methods = {
        method: programs[program][METHODS_ACCESSOR][method]
        for program in programs
        for method in programs[program][METHOD_LABELS_ACCESSOR]
    }

    # --- Run Checks ----
    check_ERA5_file(in_dir, virtual_world)
    has_ref: bool = ref_program in programs
    has_base: bool = base_program in programs

    if not (has_ref and has_base):
        print("No reference or base program input...Exiting sim")
        sys.exit()

    # -- Setup Output folder --
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    input_manager.write_parameters(out_dir / PARAMETER_FILE)

    generator_dir = in_dir / GENERATOR_FOLDER
    print("...Initializing infrastructure")
    simulation_count: int = sim_params["n_simulations"]
    emis_preseed_val: list[int] = None
    if preseed_random:
        emis_preseed_val = gen_seed_emis(simulation_count, generator_dir)
    infrastructure, hash_file_exist = initialize_infrastructure(
        methods, virtual_world, generator_dir, in_dir, preseed_random, emis_preseed_val
    )
    infrastructure: Infrastructure
    hash_file_exist: bool
    print("...Initializing emissions")
    # Pregenerate emissions
    seed_timeseries = initialize_emissions(
        simulation_count,
        preseed_random,
        emis_preseed_val,
        hash_file_exist,
        infrastructure,
        date(*virtual_world["start_date"]),
        date(*virtual_world["end_date"]),
        generator_dir,
    )
    # Initialize objects
    print("...Initializing weather")
    weather = WL(virtual_world, in_dir)
    print("...Initializing daylight")
    daylight = DaylightCalculatorAve(
        infrastructure.get_site_avrg_lat_lon(),
        date(*virtual_world["start_date"]),
        date(*virtual_world["end_date"]),
    )

    n_process = sim_params["n_processes"]
    if len(programs) < sim_params["n_processes"]:
        n_process = len(programs)
    with mp.Manager() as manager:
        lock = manager.Lock()
        simulation_number: int = 0
        print(f"......Simulating set {simulation_number}")
        # read in pregen emissions
        infra = read_in_emissions(infrastructure, generator_dir, simulation_number)
        # -- Run simulations --
        prog_data = []
        for program in programs:
            meth_params = {}
            for meth in programs[program]["method_labels"]:
                meth_params[meth] = methods[meth]
            prog_data.append(
                (
                    daylight,
                    weather,
                    simulation_number,
                    program,
                    meth_params,
                    sim_params,
                    virtual_world,
                    infra,
                    in_dir,
                    out_dir,
                    seed_timeseries,
                    lock,
                )
            )

        with mp.Pool(processes=n_process) as p:
            sim_outputs = p.starmap(
                simulate,
                prog_data,
            )
        concat_output_data(out_dir, False)
        gc.collect()
        print(f"... Finished simulating set {simulation_number}")
    # -- Batch Report --
    gen_cross_program_summary_plots(out_dir, base_program)

    os.chdir(root_dir)
    shutil.move(params_dir, test_case_dir)
    shutil.move(in_dir, test_case_dir)
    shutil.move(test_case_dir, tests_dir)
