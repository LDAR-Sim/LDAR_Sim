# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim run
# Purpose:     Main simulation sequence
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

import copy
import gc
from math import floor

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------
import os
import multiprocessing as mp
import sys
import shutil
from pathlib import Path
from datetime import date
from file_processing.output_processing.multi_simulation_outputs import (
    concat_output_data,
)


from initialization.initialize_infrastructure import initialize_infrastructure
from virtual_world.infrastructure import Infrastructure
from stdout_redirect import stdout_redirect
from virtual_world.sites import Site
from weather.daylight_calculator import DaylightCalculatorAve
from weather.weather_lookup import WeatherLookup as WL

from utils.generic_functions import check_ERA5_file
from file_processing.input_processing.input_manager import InputManager
from initialization.args import (
    files_from_args,
    get_abs_path,
)  # TODO: move this over to input_processing?
from initialization.initialize_emissions import initialize_emissions, read_in_emissions
from ldar_sim import LdarSim
from programs.program import Program

opening_msg = """
You are running LDAR-Sim version 4.0.0 an open sourced software (MIT) license.
Provide any issues, comments, questions, or recommendations by
adding an issue to https://github.com/LDAR-Sim/LDAR_Sim.git
"""


# def ldar_sim_run(simulation, weather, daylight):
#     """
#     The ldar sim run function takes a simulation dictionary
#     simulation = a dictionary of simulation parameters necessary to run LDAR-Sim
#     """

#     simulation = copy.deepcopy(simulation)
#     virtual_world = simulation["virtual_world"]
#     program_parameters = simulation["program"]
#     input_directory = simulation["input_directory"]
#     output_directory = simulation["output_directory"] / program_parameters["program_name"]
#     virtual_world["pregenerate_leaks"] = simulation["pregenerate_leaks"]
#     infrastructure: Infrastructure = simulation["Infrastructure"]
#     simulation_settings = simulation["simulation_settings"]

#     if not os.path.exists(output_directory):
#         try:
#             os.makedirs(output_directory)
#         except Exception:
#             pass

#     logfile = open(output_directory / "logfile.txt", "w")
#     if "print_from_simulation" not in simulation or simulation["print_from_simulation"]:
#         sys.stdout = stdout_redirect([sys.stdout, logfile])
#     else:
#         sys.stdout = stdout_redirect([logfile])
#     gc.collect()

#     sim = LdarSim(
#         simulation_settings,
#         weather,
#         daylight,
#         program_parameters,
#         virtual_world,
#         infrastructure,
#         input_directory,
#         output_directory,
#     )

#     # Clean up and write files
#     sim_summary = sim.finalize()
#     print(simulation["closing_message"])
#     logfile.close()
#     return sim_summary


def simulate(
    daylight,
    weather,
    sim_num: int,
    prog_name: str,
    meth_params,
    sim_settings,
    virtual_world,
    infrastructure,
    input_dir,
    output_dir,
    preseed_timeseries,
    lock,
):
    with lock:
        infra = copy.deepcopy(infrastructure)
    gc.collect()
    program: Program = Program(
        prog_name,
        weather,
        daylight,
        meth_params,
        infra._sites,
        date(*virtual_world["start_date"]),
        date(*virtual_world["end_date"]),
        virtual_world["consider_weather"],
    )
    print(f"......... Simulating program: {prog_name}")
    simulation: LdarSim = LdarSim(
        sim_num,
        sim_settings,
        virtual_world,
        program,
        infra,
        input_dir,
        output_dir,
        preseed_timeseries,
    )
    simulation.run_simulation()
    print(f"......... Finished simulating program: {prog_name}")
    gc.collect()
    return


if __name__ == "__main__":
    print(opening_msg)

    root_dir: Path = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    src_dir: Path = root_dir / "src"
    sys.path.insert(1, str(src_dir))

    # Add the external sensors directory
    # TODO update external sensors
    # ext_sens_dir: Path = root_dir / "external_sensors"
    # sys.path.append(str(ext_sens_dir))

    # -- Retrieve input parameters from commandline argument and parse --
    parameter_filenames = files_from_args(root_dir)

    input_manager = InputManager()

    if "out_dir" in parameter_filenames:
        sim_params = input_manager.read_and_validate_parameters(
            parameter_filenames["parameter_files"]
        )
        out_dir = get_abs_path(parameter_filenames["out_dir"])
    else:
        sim_params = input_manager.read_and_validate_parameters(parameter_filenames)
        out_dir = get_abs_path(sim_params["output_directory"])

    # --- Assign local variables
    ref_program = sim_params["reference_program"]
    base_program = sim_params["baseline_program"]
    in_dir = get_abs_path(sim_params["input_directory"])
    programs = sim_params.pop("programs")
    virtual_world = sim_params.pop("virtual_world")
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
    input_manager.write_parameters(out_dir / "parameters.yaml")

    generator_dir = in_dir / "generator"
    if os.path.exists(generator_dir):
        print(
            "\n".join(
                [
                    "!!!Pre-generated initialization files exist!!!",
                    "LDAR-Sim may not create new emissions to model with",
                ]
            )
        )
    print("...Initializing infrastructure")

    simulation_count: int = sim_params["n_simulations"]
    infrastructure, hash_file_exist = initialize_infrastructure(
        methods,
        virtual_world,
        generator_dir,
        in_dir,
    )
    infrastructure: Infrastructure
    hash_file_exist: bool
    print("...Initializing emissions")
    # Pregenerate emissions
    seed_timeseries = initialize_emissions(
        simulation_count,
        preseed_random,
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
    # IF the are more than 5 simulations, divide the simulations into batches
    if simulation_count > 5:
        simulation_batches = floor(simulation_count / 5.0)
        sim_counts = [5] * simulation_batches
        sim_counts.append(simulation_count % 5)
    else:
        sim_counts = [simulation_count]
    n_process = sim_params["n_processes"]
    if len(programs) < sim_params["n_processes"]:
        n_process = len(programs)
    with mp.Manager() as manager:
        lock = manager.Lock()
        for batch_count, sim_count in enumerate(sim_counts):
            for simulation in range(sim_count):
                simulation_number: int = batch_count * 5 + simulation
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
                gc.collect()
                print(f"Finished simulating set {simulation_number}")

            # -- Batch Report --
            print("...Cleaning up output data")
            concat_output_data(out_dir, batch_count != 0)
