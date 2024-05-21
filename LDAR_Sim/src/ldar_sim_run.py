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


# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------
import os

import copy
import gc
from math import floor
import cProfile
import multiprocessing as mp
import sys
import shutil
from pathlib import Path
from datetime import date
from file_processing.output_processing.summary_visualization_manager import (
    SummaryVisualizationManager,
)
from file_processing.output_processing.summary_output_manager import SummaryOutputManager


from initialization.initialize_infrastructure import initialize_infrastructure
from initialization.preseed import gen_seed_emis
from virtual_world.infrastructure import Infrastructure
from weather.daylight_calculator import DaylightCalculatorAve
from weather.weather_lookup import WeatherLookup as WL
from constants.file_name_constants import Generator_Files, Output_Files
from utils.generic_functions import check_ERA5_file
from file_processing.input_processing.input_manager import InputManager
from initialization.args import (
    files_from_args,
    get_abs_path,
)  # TODO: move this over to input_processing?
from initialization.initialize_emissions import initialize_emissions, read_in_emissions
from ldar_sim import LdarSim
from programs.program import Program
from constants.output_messages import RuntimeMessages as rm
from constants.error_messages import Runtime_Error_Messages as rem
import constants.param_default_const as pdc


def simulate(
    daylight,
    weather,
    sim_num: int,
    prog_name: str,
    meth_params,
    prog_param,
    sim_settings,
    virtual_world,
    infrastructure: Infrastructure,
    input_dir: Path,
    output_dir: Path,
    preseed_timeseries,
    lock,
):
    if lock is not None:
        with lock:
            infra = copy.deepcopy(infrastructure)
    else:
        infra = copy.deepcopy(infrastructure)
    gc.collect()
    program: Program = Program(
        prog_name,
        weather,
        daylight,
        meth_params,
        infra._sites,
        date(*virtual_world[pdc.Virtual_World_Params.START_DATE]),
        date(*virtual_world[pdc.Virtual_World_Params.END_DATE]),
        virtual_world[pdc.Virtual_World_Params.CONSIDER_WEATHER],
        prog_param,
    )
    infra.setup(program.get_method_names())
    print(rm.SIM_PROG.format(prog_name=prog_name))
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
    print(rm.FIN_PROG.format(prog_name=prog_name))
    gc.collect()
    return


def run_ldar_sim(parameter_filenames, DEBUG=False):

    input_manager = InputManager()

    if "out_dir" in parameter_filenames:
        sim_params = input_manager.read_and_validate_parameters(
            parameter_filenames["parameter_files"]
        )
        out_dir = get_abs_path(parameter_filenames[pdc.Sim_Setting_Params.OUTPUT])
    else:
        sim_params = input_manager.read_and_validate_parameters(parameter_filenames)
        out_dir = get_abs_path(sim_params[pdc.Sim_Setting_Params.OUTPUT])

    # --- Assign local variables
    ref_program = sim_params[pdc.Sim_Setting_Params.REFERENCE]
    base_program = sim_params[pdc.Sim_Setting_Params.BASELINE]
    in_dir = get_abs_path(sim_params[pdc.Sim_Setting_Params.INPUT])
    programs = sim_params.pop(pdc.Levels.PROGRAM)
    virtual_world = sim_params.pop(pdc.Levels.VIRTUAL)
    output_params = sim_params.pop(pdc.Levels.OUTPUTS)
    preseed_random = sim_params[pdc.Sim_Setting_Params.PRESEED]

    methods = {
        method: programs[program][pdc.Levels.METHOD][method]
        for program in programs
        for method in programs[program][pdc.Program_Params.METHODS]
    }

    # --- Run Checks ----
    check_ERA5_file(in_dir, virtual_world)
    has_ref: bool = ref_program in programs
    has_base: bool = base_program in programs

    if not (has_ref and has_base):
        print(rem.NO_REF_BASE_PROG_ERROR)
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
    )
    summary_visualization_manager: SummaryVisualizationManager = SummaryVisualizationManager(
        output_config=output_params,
        output_dir=out_dir,
        baseline_program=base_program,
        site_count=virtual_world[pdc.Virtual_World_Params.N_SITES],
    )
    # IF the are more than 5 simulations, divide the simulations into batches
    if simulation_count > 5:
        simulation_batches = floor(simulation_count / 5.0)
        sim_counts = [5] * simulation_batches
        remainder = simulation_count % 5
        if remainder > 0:
            sim_counts.append(remainder)
    else:
        sim_counts = [simulation_count]
    if _DEBUG:
        for batch_count, sim_count in enumerate(sim_counts):
            for simulation in range(sim_count):
                simulation_number: int = batch_count * 5 + simulation
                print(rm.SIM_SET.format(simulation_number=simulation_number))
                # read in pregen emissions
                infra = read_in_emissions(infrastructure, generator_dir, simulation_number)
                # -- Run simulations --
                for program in programs:
                    meth_params = {}
                    for meth in programs[program][pdc.Program_Params.METHODS]:
                        meth_params[meth] = methods[meth]
                    simulate(
                        daylight,
                        weather,
                        simulation_number,
                        program,
                        meth_params,
                        programs[program],
                        sim_params,
                        virtual_world,
                        infra,
                        in_dir,
                        out_dir,
                        seed_timeseries,
                        None,
                    )
                print(rm.FIN_SIM_SET.format(simulation_number=simulation_number))
            # -- Batch Report --
            print(rm.BATCH_CLEAN.format(batch_count=batch_count))
            summary_stats_manager.gen_summary_outputs(batch_count != 0)
    else:
        n_process = sim_params[pdc.Sim_Setting_Params.PROCESS]
        if len(programs) < sim_params[pdc.Sim_Setting_Params.PROCESS]:
            n_process = len(programs)
        with mp.Manager() as manager:
            lock = manager.Lock()
            for batch_count, sim_count in enumerate(sim_counts):
                for simulation in range(sim_count):
                    simulation_number: int = batch_count * 5 + simulation
                    print(rm.SIM_SET.format(simulation_number=simulation_number))
                    # read in pregen emissions
                    infra = read_in_emissions(infrastructure, generator_dir, simulation_number)
                    # -- Run simulations --
                    prog_data = []
                    for program in programs:
                        meth_params = {}
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
                                infra,
                                in_dir,
                                out_dir,
                                seed_timeseries,
                                lock,
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
                print(rm.BATCH_CLEAN.format(batch_count=batch_count))
                summary_stats_manager.gen_summary_outputs(batch_count != 0)
    summary_visualization_manager.gen_visualizations()


if __name__ == "__main__":
    print(rm.OPENING_MSG)

    root_dir: Path = Path(__file__).resolve().parent.parent
    os.chdir(root_dir)

    src_dir: Path = root_dir / "src"
    sys.path.insert(1, str(src_dir))

    # Add the external sensors directory
    # TODO update external sensors
    # ext_sens_dir: Path = root_dir / "external_sensors"
    # sys.path.append(str(ext_sens_dir))

    # -- Retrieve input parameters from commandline argument and parse --
    parameter_filenames, _DEBUG = files_from_args(root_dir)

    if _DEBUG:
        print(rm.DEBUG_MODE_ON)
        cProfile.run(
            "run_ldar_sim(parameter_filenames, _DEBUG)",
            "../Benchmarking/benchmark1_results",
            "cumulative",
        )
    else:
        run_ldar_sim(parameter_filenames)
