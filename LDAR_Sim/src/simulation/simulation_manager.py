# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        simulation_manager.py
# Purpose:     Class to manage the simulation process and state
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

import gc
import logging
import multiprocessing as mp
import os
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Tuple

import pandas as pd
from constants import param_default_const as pdc
from constants.error_messages import Runtime_Error_Messages as rem
from constants.file_name_constants import Generator_Files, Output_Files
from constants.output_messages import RuntimeMessages as rm
from file_processing.input_processing.input_manager import InputManager
from file_processing.output_processing.summary_output_helpers import get_non_baseline_prog_names
from file_processing.output_processing.summary_output_manager import SummaryOutputManager
from file_processing.output_processing.summary_visualization_manager import (
    SummaryVisualizationManager,
)
from initialization.args import get_abs_path
from initialization.initialize_emissions import initialize_emissions, read_in_emissions
from initialization.initialize_infrastructure import initialize_infrastructure
from initialization.preseed import gen_seed_emis
from log_utils.logging_config import setup_logging_to_output
from simulation.simulation_helpers import batch_simulations, simulate
from utils.generic_functions import check_ERA5_file
from utils.prog_method_measured_func import (
    filter_deployment_tf_by_program_methods,
    set_up_tf_method_deployed_df,
)
from virtual_world.infrastructure import Infrastructure
from weather.daylight_calculator import DaylightCalculatorAve
from weather.weather_lookup import WeatherLookup as WL


class SimulationManager:
    def __init__(
        self,
        input_manager: InputManager,
        parameter_filenames: list[str],
    ) -> None:
        self._read_in_parameters(input_manager, parameter_filenames)
        self.setup_properties()
        self.initialize_summary_managers()

    def _read_in_parameters(
        self,
        input_manager: InputManager,
        parameter_filenames: list[str],
    ) -> None:
        if "out_dir" in parameter_filenames:
            self.sim_params: dict = input_manager.read_and_validate_parameters(
                parameter_filenames["parameter_files"]
            )
            self.out_dir = get_abs_path(parameter_filenames[pdc.Sim_Setting_Params.OUTPUT])
        else:
            self.sim_params: dict = input_manager.read_and_validate_parameters(parameter_filenames)
            self.out_dir = get_abs_path(self.sim_params[pdc.Sim_Setting_Params.OUTPUT])

        self._set_parameters()

    def _set_parameters(self) -> None:
        self.base_program: str = self.sim_params[pdc.Sim_Setting_Params.BASELINE]
        self.in_dir: Path = get_abs_path(self.sim_params[pdc.Sim_Setting_Params.INPUT])
        self.programs: dict = self.sim_params.pop(pdc.Levels.PROGRAM)
        self.virtual_world: dict = self.sim_params.pop(pdc.Levels.VIRTUAL)
        self.output_params: dict = self.sim_params.pop(pdc.Levels.OUTPUTS)
        self.preseed_random: bool = self.sim_params[pdc.Sim_Setting_Params.PRESEED]

        self._set_methods()

    def _set_methods(self) -> None:
        self.methods = {
            method: self.programs[program][pdc.Levels.METHOD][method]
            for program in self.programs
            for method in self.programs[program][pdc.Program_Params.METHODS]
        }

    def setup_properties(self) -> None:
        self.emis_preseed_val: list[int] = None
        self.generator_dir = self.in_dir / Generator_Files.GENERATOR_FOLDER
        self.force_remake_gen: bool = False
        self.infrastructure: Infrastructure = None
        self.hash_file_exists: bool = False
        self.site_measurement_matrix: pd.DataFrame = None
        self.simulation_count: int = self.sim_params[pdc.Sim_Setting_Params.SIMS]
        self.sim_start_date: date = date(*self.virtual_world[pdc.Virtual_World_Params.START_DATE])
        self.sim_end_date: date = date(*self.virtual_world[pdc.Virtual_World_Params.END_DATE])
        self.seed_timeseries: dict[date, int] = None
        self.weather: WL = None
        self.calc_simulation_years()

    def initialize_summary_managers(self) -> None:
        self.summary_stats_manager: SummaryOutputManager = SummaryOutputManager(
            output_path=self.out_dir,
            output_config=self.output_params,
            sim_years=self.simulation_years,
            programs=self.programs,
        )

        self.summary_visualization_manager: SummaryVisualizationManager = (
            SummaryVisualizationManager(
                output_config=self.output_params,
                output_dir=self.out_dir,
                baseline_program=self.base_program,
                site_count=self.virtual_world[pdc.Virtual_World_Params.N_SITES],
            )
        )

    def check_inputs(self) -> None:
        check_ERA5_file(self.in_dir, self.virtual_world)
        has_base: bool = self.base_program in self.programs

        if not (has_base):
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(rem.NO_BASE_PROG_ERROR)
            sys.exit()

    def initialize_outputs(
        self,
        input_manager: InputManager,
        write_parameters: bool = True,
    ) -> None:
        if os.path.exists(self.out_dir):
            shutil.rmtree(self.out_dir)
        os.makedirs(self.out_dir)
        setup_logging_to_output(self.out_dir)
        if write_parameters:
            input_manager.write_parameters(self.out_dir / Output_Files.PARAMETER_FILE)

    def check_generator_files(self) -> bool:

        if os.path.exists(self.generator_dir):
            print(rm.GEN_WARNING_MSG)

        if self.preseed_random:
            self.emis_preseed_val, self.force_remake_gen = gen_seed_emis(
                self.simulation_count, self.generator_dir
            )

    def setup_infrastructure(self) -> None:

        self.site_measurement_matrix = set_up_tf_method_deployed_df(
            self.methods, self.virtual_world[pdc.Virtual_World_Params.N_SITES]
        )

        print(rm.INIT_INFRA)

        self.infrastructure, self.hash_file_exists = initialize_infrastructure(
            self.methods,
            self.programs,
            self.virtual_world,
            self.generator_dir,
            self.in_dir,
            self.preseed_random,
            self.emis_preseed_val,
            self.force_remake_gen,
        )

        self.infrastructure.gen_site_measured_tf_data(self.methods, self.site_measurement_matrix)

    def setup_emissions(self) -> None:
        print(rm.INIT_EMISS)
        self.seed_timeseries = initialize_emissions(
            self.simulation_count,
            self.preseed_random,
            self.emis_preseed_val,
            self.hash_file_exists,
            self.infrastructure,
            self.sim_start_date,
            self.sim_end_date,
            self.generator_dir,
        )

    def setup_weather(self) -> None:
        print(rm.INIT_WEATHER)
        self.weather = WL(self.virtual_world, self.in_dir)
        self.infrastructure.set_weather_index(self.weather)

    def setup_daylight(self) -> None:
        print(rm.INIT_DAYLIGHT)
        self.daylight = DaylightCalculatorAve(
            self.infrastructure.get_site_avrg_lat_lon(),
            self.sim_start_date,
            self.sim_end_date,
        )

    def calc_simulation_years(self) -> None:
        self.simulation_years = [
            year for year in range(self.sim_start_date.year, self.sim_end_date.year + 1)
        ]

    def run_simulations(self, DEBUG: bool) -> None:
        sim_counts: list[int] = batch_simulations(self.simulation_count)
        if DEBUG:
            self._run_simulations_debug(sim_counts=sim_counts)
        else:
            self._run_simulation_multiprocessing(sim_counts=sim_counts)

    def _run_simulations_debug(self, sim_counts: list[int]) -> None:
        for batch_count, sim_count in enumerate(sim_counts):
            for simulation in range(sim_count):
                simulation_number: int = batch_count * 5 + simulation
                print(rm.SIM_SET.format(simulation_number=simulation_number))
                program_data: list[Tuple] = self._setup_programs(
                    simulation_number=simulation_number
                )
                for program in program_data:
                    simulate(*program)
                print(rm.FIN_SIM_SET.format(simulation_number=simulation_number))
            print(rm.BATCH_CLEAN.format(batch_count=batch_count))
            self.summary_stats_manager.gen_summary_outputs(batch_count != 0)

    def _run_simulation_multiprocessing(self, sim_counts: list[int]) -> None:
        n_processes: int = self.sim_params[pdc.Sim_Setting_Params.PROCESS]
        if len(self.programs) < n_processes:
            n_processes = len(self.programs)
        with mp.Manager() as manager:
            lock = manager.Lock()
            for batch_count, sim_count in enumerate(sim_counts):
                for simulation in range(sim_count):
                    simulation_number: int = batch_count * 5 + simulation
                    print(rm.SIM_SET.format(simulation_number=simulation_number))
                    program_data: list[Tuple] = self._setup_programs(
                        simulation_number=simulation_number, lock=lock
                    )
                    with mp.Pool(processes=n_processes) as p:
                        _ = p.starmap(
                            simulate,
                            program_data,
                        )
                    gc.collect()
                    print(rm.FIN_SIM_SET.format(simulation_number=simulation_number))
                print(rm.BATCH_CLEAN.format(batch_count=batch_count))
            self.summary_stats_manager.gen_summary_outputs(batch_count != 0)

    def _setup_programs(
        self,
        simulation_number: int,
        lock=None,
    ) -> None:
        # read in pregen emissions
        infra: Infrastructure = read_in_emissions(
            self.infrastructure, self.generator_dir, simulation_number
        )
        prog_data: list = []
        for program in self.programs:
            meth_params = {}
            prog_measured_df = filter_deployment_tf_by_program_methods(
                self.site_measurement_matrix, self.programs[program][pdc.Program_Params.METHODS]
            )
            for meth in self.programs[program][pdc.Program_Params.METHODS]:
                meth_params[meth] = self.methods[meth]
            prog_data.append(
                (
                    self.daylight,
                    self.weather,
                    simulation_number,
                    program,
                    meth_params,
                    self.programs[program],
                    self.sim_params,
                    self.virtual_world,
                    self.output_params,
                    infra,
                    self.in_dir,
                    self.out_dir,
                    self.seed_timeseries,
                    lock,
                    prog_measured_df,
                )
            )
        return prog_data

    def generate_summary_results(self) -> None:

        if self.summary_stats_manager.make_cost_summary():
            non_baseline_progs = get_non_baseline_prog_names(self.programs, self.base_program)
            self.summary_stats_manager.gen_cost_summary_outputs(non_baseline_progs)
        self.summary_visualization_manager.gen_visualizations()
