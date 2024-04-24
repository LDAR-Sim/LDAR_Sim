"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        summary_outputs.py
Purpose: Contains functions to summarize the outputs of the LDAR-Sim program.

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

import os
import re
from typing import Any
import pandas as pd
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper
from constants import output_file_constants, file_processing_const, file_name_constants


def summarize_program_outputs(
    output_path: str,
    summary_output: pd.DataFrame,
    summary_mappings: dict[str, callable],
    source_regex: re.Pattern[str],
) -> None:
    with os.scandir(output_path) as entries:
        for entry in entries:
            if (
                entry.is_file()
                and source_regex.match(entry.name)
                and not re.search(
                    file_processing_const.Multi_Sim_Output_Const.OUTPUT_KEEP_REGEX, entry.name
                )
            ):
                new_summary_row: dict[str, Any] = {}
                data = pd.read_csv(entry.path)
                new_summary_row[
                    output_file_constants.SummaryFileColumns.CommonColumns.PROGRAM_NAME
                ] = (
                    (file_processing_const.Multi_Sim_Output_Const.OUTPUTS_NAME_SIM_EXTRACTION_REGEX)
                    .match(entry.name)
                    .group(1)
                )
                new_summary_row[
                    output_file_constants.SummaryFileColumns.CommonColumns.SIMULATION_NUMBER
                ] = (
                    (file_processing_const.Multi_Sim_Output_Const.OUTPUTS_NAME_SIM_EXTRACTION_REGEX)
                    .match(entry.name)
                    .group(2)
                )
                for summary_stat, calc_func in summary_mappings.items():
                    new_summary_row[summary_stat] = calc_func(data)
                summary_output.loc[len(summary_output)] = new_summary_row


def generate_timeseries_summary(directory: str, outputs_mapper: SummaryOutputMapper):
    summary_columns: list[str] = outputs_mapper.get_summary_columns(
        file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY
    )
    summary_columns.insert(
        0, output_file_constants.SummaryFileColumns.CommonColumns.SIMULATION_NUMBER
    )
    summary_columns.insert(0, output_file_constants.SummaryFileColumns.CommonColumns.PROGRAM_NAME)
    timeseries_summary_df = pd.DataFrame(columns=summary_columns)
    summarize_program_outputs(
        directory,
        timeseries_summary_df,
        outputs_mapper.get_summary_mappings(
            file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY
        ),
        file_processing_const.Multi_Sim_Output_Const.TS_PATTERN,
    )
    return timeseries_summary_df


def generate_emissions_summary(directory: str, outputs_mapper: SummaryOutputMapper):
    summary_columns: list[str] = outputs_mapper.get_summary_columns(
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    )
    summary_columns.insert(
        0, output_file_constants.SummaryFileColumns.CommonColumns.SIMULATION_NUMBER
    )
    summary_columns.insert(0, output_file_constants.SummaryFileColumns.CommonColumns.PROGRAM_NAME)
    emissions_summary_df = pd.DataFrame(columns=summary_columns)
    summarize_program_outputs(
        directory,
        emissions_summary_df,
        outputs_mapper.get_summary_mappings(
            file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
        ),
        file_processing_const.Multi_Sim_Output_Const.EMIS_PATTERN,
    )
    estimated_df: pd.DataFrame = generate_emissions_estimation_summary(directory, outputs_mapper)
    merged = pd.merge(
        emissions_summary_df,
        estimated_df,
        on=[
            output_file_constants.SummaryFileColumns.CommonColumns.PROGRAM_NAME,
            output_file_constants.SummaryFileColumns.CommonColumns.SIMULATION_NUMBER,
        ],
        how="outer",
    )
    # Fill NaN values with zeros
    merged.fillna(0, inplace=True)
    return merged


def generate_emissions_estimation_summary(directory: str, outputs_mapper: SummaryOutputMapper):
    summary_columns: list[str] = outputs_mapper.get_summary_columns(
        file_name_constants.Output_Files.SummaryFileNames.EMIS_EST_SUMMARY
    )
    summary_columns.insert(
        0, output_file_constants.SummaryFileColumns.CommonColumns.SIMULATION_NUMBER
    )
    summary_columns.insert(0, output_file_constants.SummaryFileColumns.CommonColumns.PROGRAM_NAME)
    est_emissions_summary_df = pd.DataFrame(columns=summary_columns)
    est_rep_emissions_summary_df = pd.DataFrame(columns=summary_columns)
    summarize_program_outputs(
        directory,
        est_emissions_summary_df,
        outputs_mapper.get_summary_mappings(
            file_name_constants.Output_Files.SummaryFileNames.EMIS_EST_SUMMARY
        ),
        file_processing_const.Multi_Sim_Output_Const.EST_PATTERN,
    )
    summarize_program_outputs(
        directory,
        est_rep_emissions_summary_df,
        outputs_mapper.get_summary_mappings(
            file_name_constants.Output_Files.SummaryFileNames.EMIS_FUG_EST_SUMMARY
        ),
        file_processing_const.Multi_Sim_Output_Const.EST_REP_PATTERN,
    )
    columns_to_subtract = [
        col
        for col in summary_columns
        if col
        not in [
            output_file_constants.SummaryFileColumns.CommonColumns.PROGRAM_NAME,
            output_file_constants.SummaryFileColumns.CommonColumns.SIMULATION_NUMBER,
        ]
    ]

    subtracted_df = est_emissions_summary_df[columns_to_subtract].sub(
        est_rep_emissions_summary_df[columns_to_subtract]
    )

    # Combine the result with columns not involved in subtraction
    result = pd.concat(
        [est_emissions_summary_df.drop(columns=columns_to_subtract), subtracted_df], axis=1
    )
    return result
