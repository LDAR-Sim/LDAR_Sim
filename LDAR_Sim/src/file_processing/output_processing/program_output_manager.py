"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        program_output_manager.py
Purpose: Contains the class definition for the ProgramOutputManager class.

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

from datetime import date
import os
import numpy as np
import pandas as pd
from pathlib import Path, WindowsPath
from typing import Any

from file_processing.output_processing.program_specific_visualizations import (
    gen_prog_timeseries_plot,
)
from file_processing.output_processing.output_utils import (
    EmisInfo,
    TsEmisData,
    TsMethodData,
)
from constants.file_name_constants import Output_Files
from constants.output_file_constants import (
    TIMESERIES_COL_ACCESSORS as tca,
    TIMESERIES_COLUMNS,
    EMIS_DATA_COL_ACCESSORS as eca,
    EMIS_INFO_COLUMNS_TO_KEEP_FOR_DURATION_ESTIMATION,
)
from programs.program import Program
from constants.param_default_const import Duration_Method as dm
import file_processing.output_processing.program_output as prog_output


class ProgramOutputManager:
    PROGRAM_FUNCTIONS_MAPPING = {
        dm.COMPONENT: prog_output.gen_estimated_comp_emissions_report,
        dm.MEASUREMENT_CONSERVATIVE: prog_output.gen_estimated_emissions_report,
    }

    def __init__(self, path: WindowsPath, name_str: str, method_names: list[str]) -> None:
        self._output_dir: Path = path
        self.name_str: str = name_str
        self._method_names: list[str] = method_names

    def summarize_program_outputs(
        self,
        overall_emission_data: pd.DataFrame,
        timeseries: pd.DataFrame,
        start_date: date,
        end_date: date,
        program: Program,
    ) -> None:
        self.gen_sim_directory()
        summary_filename = self.generate_file_names(Output_Files.EMISSIONS_SUMMARY_FILE)
        self.save_results(overall_emission_data, summary_filename)
        self.gen_prog_spec_visualizations(timeseries=timeseries)
        timeseries_filename = self.generate_file_names(Output_Files.TIMESERIES_FILE)
        self.save_results(timeseries, timeseries_filename)

        # 1. Trim Emissions data to only include necessary columns
        emis_info_for_duration_estimation = overall_emission_data.loc[
            overall_emission_data[eca.REPAIRABLE],
            EMIS_INFO_COLUMNS_TO_KEEP_FOR_DURATION_ESTIMATION,
        ]
        function_to_call = self.PROGRAM_FUNCTIONS_MAPPING.get(program.duration_method)
        if function_to_call:
            result = function_to_call(
                program.aggregate_method_survey_reports(),
                emis_info_for_duration_estimation,
                start_date,
                end_date,
            )
            if result:
                emis_estimation: pd.DataFrame
                fug_to_remove: pd.DataFrame
                emis_estimation, fug_to_remove = result
                emis_file_name = self.generate_file_names(Output_Files.EST_EMISSIONS_FILE)
                fug_file_name = self.generate_file_names(Output_Files.EST_REP_EMISSIONS_FILE)

                emis_estimation.to_csv(self._output_dir / emis_file_name, index=False)
                fug_to_remove.to_csv(self._output_dir / fug_file_name, index=False)
        else:
            raise KeyError(f"No function found for program: {program}")

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

    def _init_ts_row(self, current_date: date):
        new_ts_row: dict[str, Any] = {
            tca.DATE: current_date,
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

    def _init_ts_columns(self) -> list[str]:
        ts_columns = TIMESERIES_COLUMNS
        for method in self._method_names:
            ts_columns.append(tca.METH_DAILY_DEPLOY_COST.format(method=method))
            ts_columns.append(tca.METH_DAILY_FLAGS.format(method=method))
            ts_columns.append(tca.METH_DAILY_TAGS.format(method=method))
            ts_columns.append(tca.METH_DAILY_SITES_VIS.format(method=method))
            ts_columns.append(tca.METH_DAILY_TRAVEL_TIME.format(method=method))
            ts_columns.append(tca.METH_DAILY_SURVEY_TIME.format(method=method))
        return ts_columns

    def generate_file_names(self, concat_string: str) -> str:
        return "_".join([self.name_str, concat_string])
