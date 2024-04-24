"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        summary_output_mapper.py
Purpose: Contains the mapping for summary outputs

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

from constants import output_file_constants, file_processing_const, file_name_constants
from file_processing.output_processing import summary_output_helpers


class SummaryOutputMapper:

    SUMMARY_MAPPINGS = {
        file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY: {
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_DAILY_EMIS: lambda df: (
                summary_output_helpers.get_mean_val(
                    df, output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_MIT_DAILY_EMIS: lambda df: (
                summary_output_helpers.get_mean_val(
                    df, output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS_MIT
                )
            ),
            (
                output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_NON_MIT_DAILY_EMIS
            ): lambda df: (
                summary_output_helpers.get_mean_val(
                    df, output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS_NON_MIT
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_95: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_95,
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_MIT_DAILY_EMIS_95: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS_MIT,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_95,
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_NON_MIT_DAILY_EMIS_95: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS_NON_MIT,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_95,
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_5: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_5,
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_MIT_DAILT_EMIS_5: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS_MIT,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_5,
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_NON_MIT_DAILY_EMIS_5: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.TIMESERIES_COL_ACCESSORS.EMIS_NON_MIT,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_5,
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.AVG_DAILY_COST: lambda df: (
                summary_output_helpers.get_mean_val(
                    df, output_file_constants.TIMESERIES_COL_ACCESSORS.COST
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_95: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.TIMESERIES_COL_ACCESSORS.COST,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_95,
                )
            ),
            output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_5: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.TIMESERIES_COL_ACCESSORS.COST,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_5,
                )
            ),
        },
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY: {
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS: lambda df: (
                summary_output_helpers.get_sum(
                    df, output_file_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_TOTAL_EMIS: lambda df: (
                summary_output_helpers.get_sum(
                    df, output_file_constants.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_MIT_EMIS: lambda df: (
                summary_output_helpers.get_sum(
                    df.loc[df[output_file_constants.EMIS_DATA_COL_ACCESSORS.REPAIRABLE]],
                    output_file_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_NON_MIT_EMIS: lambda df: (
                summary_output_helpers.get_sum(
                    df.loc[~df[output_file_constants.EMIS_DATA_COL_ACCESSORS.REPAIRABLE]],
                    output_file_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_EMIS_RATE: lambda df: (
                summary_output_helpers.get_mean_val(
                    df, output_file_constants.EMIS_DATA_COL_ACCESSORS.T_RATE
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_95: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.EMIS_DATA_COL_ACCESSORS.T_RATE,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_95,
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_5: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.EMIS_DATA_COL_ACCESSORS.T_RATE,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_5,
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_AVG_EMIS_AMOUNT: lambda df: (
                summary_output_helpers.get_mean_val(
                    df, output_file_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_95: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_95,
                )
            ),
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_5: lambda df: (
                summary_output_helpers.get_nth_percentile(
                    df,
                    output_file_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
                    file_processing_const.Multi_Sim_Output_Const.PERCENTILE_5,
                )
            ),
        },
        file_name_constants.Output_Files.SummaryFileNames.EMIS_EST_SUMMARY: {},
        file_name_constants.Output_Files.SummaryFileNames.EMIS_FUG_EST_SUMMARY: {},
    }

    YEARLY_MAPPINGS = {
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY: {
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS: lambda year: (
                lambda df: (
                    summary_output_helpers.get_yearly_value_for_multi_day_stat(
                        df,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
                        year,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.DATE_BEG,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.DATE_REP_EXP,
                    )
                )
            ),
        },
        file_name_constants.Output_Files.SummaryFileNames.EMIS_EST_SUMMARY: {
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS: lambda year: (
                lambda df: (
                    summary_output_helpers.get_yearly_value_for_multi_day_stat(
                        df,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT,
                        year,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.START_DATE,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.END_DATE,
                    )
                )
            )
        },
        file_name_constants.Output_Files.SummaryFileNames.EMIS_FUG_EST_SUMMARY: {
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS: lambda year: (
                lambda df: (
                    summary_output_helpers.get_yearly_value_for_multi_day_stat(
                        df,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT,
                        year,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.START_DATE,
                        output_file_constants.EMIS_DATA_COL_ACCESSORS.END_DATE,
                    )
                )
            )
        },
    }

    def __init__(self, summary_config: dict[str, dict[str, bool]] = {}, sim_years: list[int] = []):
        self.summary_mapping: dict[str, dict[str, callable]] = {}
        summary_files: file_name_constants.Output_Files.SummaryFileNames = (
            file_name_constants.Output_Files.SummaryFileNames()
        )
        if summary_config:
            for summary_file in summary_files:
                self.set_summary_mapping(summary_file, summary_config.get(summary_file, {}))
                self.add_yearly_mappings(
                    summary_file,
                    sim_years,
                )

    def set_summary_mapping(self, summary_file: str, config: dict[str, bool]):
        wanted_summary_vals: list[str] = [
            summary_val for summary_val, wanted in config.items() if wanted
        ]
        self.summary_mapping[summary_file] = {
            mapping_key: mapping_function
            for mapping_key, mapping_function in self.SUMMARY_MAPPINGS[summary_file].items()
            if mapping_key in wanted_summary_vals
        }

    def add_yearly_mappings(self, summary_file: str, sim_years: list[int]):
        if summary_file not in self.YEARLY_MAPPINGS:
            return
        for mapping_key, mapping_function in self.YEARLY_MAPPINGS[summary_file].items():
            for year in sim_years:
                self.add_summary_mapping(
                    summary_file,
                    mapping_key.format(year),
                    mapping_function(year),
                )

    def add_summary_mapping(self, summary_file: str, map_key: str, map_function: callable):
        if summary_file not in self.summary_mapping:
            self.summary_mapping[summary_file] = {}
        self.summary_mapping[summary_file][map_key] = map_function

    def get_summary_mapping(self, summary_file: str, map_key: str) -> callable:
        if summary_file not in self.summary_mapping:
            self.summary_mapping[summary_file] = {}
        return self.summary_mapping[summary_file].get(map_key)

    def get_summary_columns(self, summary_file: str) -> list[str]:
        return list(self.summary_mapping[summary_file].keys())

    def get_summary_mappings(self, summary_file: str) -> dict[str, callable]:
        return self.summary_mapping[summary_file]
