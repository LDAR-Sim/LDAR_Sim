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


from pathlib import WindowsPath
from typing import Any
import pandas as pd
import numpy as np

from file_processing.output_processing.program_output_manager import ProgramOutputManager
from virtual_world.infrastructure import Infrastructure
from time_counter import TimeCounter
from programs.program import Program
from file_processing.output_processing.output_utils import (
    EmisInfo,
    TsEmisData,
    TsMethodData,
)
from constants.output_file_constants import (
    EMIS_DATA_FINAL_COL_ORDER,
    TIMESERIES_COL_ACCESSORS as tca,
)
from constants.param_default_const import Virtual_World_Params as vp


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
        self._tc: TimeCounter = TimeCounter(
            virtual_world[vp.START_DATE], virtual_world[vp.END_DATE]
        )
        self._sim_number: int = sim_number
        self._infrastructure: Infrastructure = infrastructure
        # TODO remove if unused
        self.simulation_settings = simulation_settings
        self._program: Program = program

        self._input_dir: WindowsPath = input_dir

        self.name_str: str = self.SIMULATION_NAME_STR.format(
            program=program.name, sim_number=sim_number
        )
        self._output_manager: ProgramOutputManager = ProgramOutputManager(
            path=output_dir / program.name,
            name_str=self.name_str,
            method_names=program.method_names,
        )
        if preseed_timeseries is not None:
            self._preseed = True
            self._preseed_ts = preseed_timeseries
        else:
            self._preseed = False
        return

    def run_simulation(self):
        ts_columns = self._output_manager._init_ts_columns()
        timeseries = pd.DataFrame(columns=ts_columns)
        total_emissions_count: int = 0
        while not self._tc.at_simulation_end():
            if self._preseed:
                np.random.seed(self._preseed_ts[self._tc.current_date])
            new_row: dict[str, Any] = self._output_manager._init_ts_row(self._tc.current_date)
            new_row[tca.NEW_LEAKS] = self._infrastructure.activate_emissions(
                self._tc.current_date, self._sim_number
            )
            total_emissions_count += new_row[tca.NEW_LEAKS]
            ts_methods_info: list[TsMethodData] = self._program.do_daily_program_deployment()
            ts_emis_rep_info: EmisInfo = EmisInfo()
            ts_emis_info: TsEmisData = self._infrastructure.update_emissions_state(ts_emis_rep_info)
            self._output_manager._update_ts_row_w_emis_info(
                new_row=new_row, ts_emis_info=ts_emis_info, ts_emis_rep_info=ts_emis_rep_info
            )
            self._output_manager._update_ts_row_w_methods_info(
                new_row=new_row, ts_methods_info=ts_methods_info
            )
            timeseries.loc[len(timeseries)] = new_row
            self._program.update_date()
            self._tc.next_day()

        overall_emission_data: pd.DataFrame = pd.DataFrame(
            columns=EMIS_DATA_FINAL_COL_ORDER, index=range(total_emissions_count)
        )
        self._infrastructure.gen_summary_emis_data(overall_emission_data, self._tc._end_date)

        self._output_manager.summarize_program_outputs(
            overall_emission_data,
            timeseries,
            self._tc._start_date,
            self._tc._end_date,
            self._program,
        )
