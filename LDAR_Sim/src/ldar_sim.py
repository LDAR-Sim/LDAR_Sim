# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        LDAR-Sim
# Purpose:     Primary module of LDAR-Sim
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
from pathlib import Path, WindowsPath
import pandas as pd
from virtual_world.infrastructure import Infrastructure
from time_counter import TimeCounter
from programs.program import Program
from file_processing.output_processing.output_constants import EMIS_SUMMARY_FINAL_COL_ORDER


class LdarSim:
    SIMULATION_NAME_STR = "{program}_{sim_number}"

    def __init__(
        self,
        sim_number: int,
        simulation_settings,
        virtual_world,
        program: Program,
        infrastructure: Infrastructure,
        input_dir: WindowsPath,
        output_dir: WindowsPath,
    ):
        """
        Construct the simulation.
        """
        self._tc: TimeCounter = TimeCounter(virtual_world["start_date"], virtual_world["end_date"])
        self.sim_number: int = sim_number
        self.infrastructure: Infrastructure = infrastructure
        # TODO remove if unused
        self.simulation_settings = simulation_settings
        self.program: Program = program

        self.input_dir: WindowsPath = input_dir
        self.output_dir: WindowsPath = output_dir / program.name
        self.name_str: str = self.SIMULATION_NAME_STR.format(
            program=program.name, sim_number=sim_number
        )

        return

    def run_simulation(self):
        while not self._tc.at_simulation_end():
            self.infrastructure.activate_emissions(self._tc.current_date, self.sim_number)
            self.program.do_daily_program_deployment()
            self.infrastructure.update_emissions_state()
            self.program.update_date()
            self._tc.next_day()

        overall_emission_data: pd.DataFrame = self.infrastructure.gen_summary_emis_data()

        overall_emission_data = overall_emission_data[
            EMIS_SUMMARY_FINAL_COL_ORDER
            + [
                col
                for col in overall_emission_data.columns
                if col not in EMIS_SUMMARY_FINAL_COL_ORDER
            ]
        ]

        self.gen_sim_directory()
        summary_filename = "_".join([self.name_str, "emissions_summary.csv"])
        self.save_results(overall_emission_data, summary_filename)

    def gen_sim_directory(self) -> None:
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def save_results(self, data: pd.DataFrame, filename: str) -> None:
        if data is None:
            return
        filepath: Path = self.output_dir / filename
        data.to_csv(filepath, index=False)
