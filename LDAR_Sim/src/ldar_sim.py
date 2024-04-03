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
from file_processing.output_processing.program_specific_visualizations import (
    gen_prog_timeseries_plot,
)
from virtual_world.infrastructure import Infrastructure
from time_counter import TimeCounter
from programs.program import Program
from file_processing.output_processing.output_utils import (
    EMIS_DATA_FINAL_COL_ORDER,
    TIMESERIES_COLUMNS,
    TIMESERIES_COL_ACCESSORS as tca,
    EmisInfo,
    TsEmisData,
    TsMethodData,
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
        ts_columns = self._init_ts_columns()
        timeseries = pd.DataFrame(columns=ts_columns)
        total_emissions_count: int = 0
        while not self._tc.at_simulation_end():
            if self._preseed:
                np.random.seed(self._preseed_ts[self._tc.current_date])
            new_row: dict[str, Any] = self._init_ts_row()
            new_row[tca.NEW_LEAKS] = self._infrastructure.activate_emissions(
                self._tc.current_date, self._sim_number
            )
            total_emissions_count += new_row[tca.NEW_LEAKS]
            ts_methods_info: list[TsMethodData] = self._program.do_daily_program_deployment()
            ts_emis_rep_info: EmisInfo = EmisInfo()
            ts_emis_info: TsEmisData = self._infrastructure.update_emissions_state(ts_emis_rep_info)
            self._update_ts_row_w_emis_info(
                new_row=new_row, ts_emis_info=ts_emis_info, ts_emis_rep_info=ts_emis_rep_info
            )
            self._update_ts_row_w_methods_info(new_row=new_row, ts_methods_info=ts_methods_info)
            timeseries.loc[len(timeseries)] = new_row
            self._program.update_date()
            self._tc.next_day()

        overall_emission_data: pd.DataFrame = pd.DataFrame(
            columns=EMIS_DATA_FINAL_COL_ORDER, index=range(total_emissions_count)
        )
        self._infrastructure.gen_summary_emis_data(overall_emission_data, self._tc._end_date)

        self.gen_sim_directory()
        summary_filename = "_".join([self.name_str, "emissions_summary.csv"])
        self.save_results(overall_emission_data, summary_filename)
        self.gen_prog_spec_visualizations(timeseries=timeseries)
        timeseries_filename = "_".join([self.name_str, "timeseries.csv"])
        self.save_results(timeseries, timeseries_filename)

    def _init_ts_columns(self) -> list[str]:
        ts_columns = TIMESERIES_COLUMNS
        for method in self._program.method_names:
            ts_columns.append(tca.METH_DAILY_DEPLOY_COST.format(method=method))
            ts_columns.append(tca.METH_DAILY_FLAGS.format(method=method))
            ts_columns.append(tca.METH_DAILY_TAGS.format(method=method))
            ts_columns.append(tca.METH_DAILY_SITES_VIS.format(method=method))
            ts_columns.append(tca.METH_DAILY_TRAVEL_TIME.format(method=method))
            ts_columns.append(tca.METH_DAILY_SURVEY_TIME.format(method=method))
        return ts_columns

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
        }
        return new_ts_row

    def _update_ts_row_w_emis_info(
        self, new_row: dict[str, Any], ts_emis_info: TsEmisData, ts_emis_rep_info: EmisInfo
    ):
        new_row[tca.EMIS] = ts_emis_info.daily_emis
        new_row[tca.EMIS_MIT] = ts_emis_info.daily_emis_mit
        new_row[tca.EMIS_NON_MIT] = ts_emis_info.daily_emis_non_mit
        new_row[tca.ACT_LEAKS] = ts_emis_info.active_leaks
        new_row[tca.REP_COST] = ts_emis_rep_info.repair_cost
        new_row[tca.REP_LEAKS] = ts_emis_rep_info.leaks_repaired
        new_row[tca.NAT_REP_COST] = ts_emis_rep_info.nat_repair_cost
        new_row[tca.NAT_REP_LEAKS] = ts_emis_rep_info.leaks_nat_repaired

    def _update_ts_row_w_methods_info(
        self, new_row: dict[str, Any], ts_methods_info: list[TsMethodData]
    ) -> None:
        total_daily_cost: float = 0.0
        total_leaks_tagged: int = 0
        for method_info in ts_methods_info:
            total_daily_cost += method_info.daily_deployment_cost
            total_leaks_tagged += np.nan_to_num(method_info.daily_tags)
            new_row[tca.METH_DAILY_DEPLOY_COST.format(method=method_info.method_name)] = (
                method_info.daily_deployment_cost
            )
            new_row[tca.METH_DAILY_TAGS.format(method=method_info.method_name)] = (
                method_info.daily_tags
            )
            new_row[tca.METH_DAILY_FLAGS.format(method=method_info.method_name)] = (
                method_info.daily_flags
            )
            new_row[tca.METH_DAILY_SITES_VIS.format(method=method_info.method_name)] = (
                method_info.sites_visited
            )
            new_row[tca.METH_DAILY_TRAVEL_TIME.format(method=method_info.method_name)] = (
                method_info.travel_time
            )
            new_row[tca.METH_DAILY_SURVEY_TIME.format(method=method_info.method_name)] = (
                method_info.survey_time
            )
        new_row[tca.COST] = total_daily_cost + new_row[tca.REP_COST]
        new_row[tca.TAGGED_LEAKS] = total_leaks_tagged

    def format_timeseries(self, timeseries: pd.DataFrame) -> None:
        return None

    def gen_sim_directory(self) -> None:
        if not os.path.exists(self._output_dir):
            os.mkdir(self._output_dir)

    def save_results(self, data: pd.DataFrame, filename: str) -> None:
        if data is None:
            return
        filepath: Path = self._output_dir / filename
        with open(filepath, "w", newline="") as f:
            data.to_csv(f, index=False, float_format="%.5f")

    def gen_prog_spec_visualizations(self, timeseries: pd.DataFrame):
        gen_prog_timeseries_plot(timeseries, self._output_dir, self.name_str)
        return
