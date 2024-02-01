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
from typing import Any
import pandas as pd
import numpy as np
from virtual_world.infrastructure import Infrastructure
from time_counter import TimeCounter
from programs.program import Program
from file_processing.output_processing.output_utils import (
    EMIS_SUMMARY_FINAL_COL_ORDER,
    TIMESERIES_COLUMNS,
    TIMESERIES_COL_ACCESSORS as tca,
    TsEmisData,
)


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
        preseed_timeseries,
    ):
        """
        Construct the simulation.
        """
        self._tc: TimeCounter = TimeCounter(virtual_world["start_date"], virtual_world["end_date"])
        self._sim_number: int = sim_number
        self._infrastructure: Infrastructure = infrastructure
        # TODO remove if unused
        self.simulation_settings = simulation_settings
        self._program: Program = program

        self._input_dir: WindowsPath = input_dir
        self._output_dir: WindowsPath = output_dir / program.name
        self.name_str: str = self.SIMULATION_NAME_STR.format(
            program=program.name, sim_number=sim_number
        )
        if preseed_timeseries is not None:
            self._preseed = True
            self._preseed_ts = preseed_timeseries
        else:
            self._preseed = False
        return

    def run_simulation(self):
        timeseries = pd.DataFrame(columns=TIMESERIES_COLUMNS)
        while not self._tc.at_simulation_end():
            if self._preseed:
                np.random.seed(self._preseed_ts[self._tc.current_date])
            new_row: dict[str, Any] = self._init_ts_row()
            new_row[tca.NEW_LEAKS] = self._infrastructure.activate_emissions(
                self._tc.current_date, self._sim_number
            )
            ts_method_info: list[TsMethodData] = self._program.do_daily_program_deployment()
            ts_emis_info: TsEmisData = self._infrastructure.update_emissions_state()
            self._update_ts_row_w_emis_info(new_row=new_row, ts_emis_info=ts_emis_info)
            timeseries.loc[len(timeseries)] = new_row
            self._program.update_date()
            self._tc.next_day()

        overall_emission_data: pd.DataFrame = self._infrastructure.gen_summary_emis_data()

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
        self.format_timeseries(timeseries)
        timeseries_filename = "_".join([self.name_str, "timeseries.csv"])
        self.save_results(timeseries, timeseries_filename)

    def _init_ts_row(self):
        new_ts_row: dict[str, Any] = {
            tca.DATE: self._tc.current_date,
            tca.EMIS: 0,
            tca.COST: 0,
            tca.ACT_LEAKS: 0,
            tca.NEW_LEAKS: 0,
            tca.REP_LEAKS: 0,
            tca.NAT_REP_LEAKS: 0,
            tca.TAGGED_LEAKS: 0,
            tca.REP_COST: 0,
            tca.NAT_REP_COST: 0,
            tca.VERF_COST: 0,
        }
        return new_ts_row

    def _update_ts_row_w_emis_info(self, new_row: dict[str, Any], ts_emis_info: TsEmisData):
        new_row[tca.EMIS] = ts_emis_info.daily_emis
        new_row[tca.ACT_LEAKS] = ts_emis_info.active_leaks
        new_row[tca.REP_LEAKS] = ts_emis_info.repaired_leaks

    def format_timeseries(self, timeseries: pd.DataFrame) -> None:
        return None

    def gen_sim_directory(self) -> None:
        if not os.path.exists(self._output_dir):
            os.mkdir(self._output_dir)

    def save_results(self, data: pd.DataFrame, filename: str) -> None:
        if data is None:
            return
        filepath: Path = self._output_dir / filename
        data.to_csv(filepath, index=False)
