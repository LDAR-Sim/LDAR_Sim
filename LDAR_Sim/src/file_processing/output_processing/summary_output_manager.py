"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        summary_output_manager.py
Purpose: Contains the SummaryOutputManager module for LDAR-Sim.

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
from pathlib import Path

import pandas as pd
from constants.file_name_constants import Output_Files
from constants import output_file_constants
from constants.general_const import Conversion_Constants as cc
from file_processing.output_processing import summary_outputs, summary_output_helpers
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper
from constants.param_default_const import Program_Params as pp


class SummaryOutputManager:

    OUTPUT_FUNCTIONS_MAP = {
        Output_Files.SummaryFileNames.TS_SUMMARY: (summary_outputs.generate_timeseries_summary),
        Output_Files.SummaryFileNames.EMIS_SUMMARY: (summary_outputs.generate_emissions_summary),
    }

    def __init__(
        self, output_path: Path, output_config: dict, sim_years: list[int], programs: dict
    ):
        self._output_path: Path = output_path
        self._summary_outputs_to_make: list[str] = self.parse_output_functions(
            output_config[output_file_constants.OutputConfigCategories.SUMMARY_OUTPUTS][
                output_file_constants.OutputConfigCategories.SummaryOutputCatageories.SUMMARY_FILES
            ]
        )
        self._outputs_mapper: SummaryOutputMapper = SummaryOutputMapper(
            output_config[output_file_constants.OutputConfigCategories.SUMMARY_OUTPUTS][
                output_file_constants.OutputConfigCategories.SummaryOutputCatageories.SUMMARY_STATS
            ],
            sim_years,
        )

        self.parse_program_cost_info(programs)

    def parse_program_cost_info(self, programs: dict) -> None:
        program_cost_info = {}
        for program_name, program in programs.items():
            program_cost_info[program_name] = program.get(pp.ECONOMICS)

        self._program_cost_info = program_cost_info

    def gen_summary_outputs(self, clear_outputs: bool = False):
        program_directories: list[str] = [
            f.path for f in os.scandir(self._output_path) if f.is_dir()
        ]
        legacy_outputs: dict[str, pd.DataFrame] = self.get_legacy_outputs()
        new_outputs: dict[str, list[pd.DataFrame]] = {}
        for program_directory in program_directories:
            for summary_output in self._summary_outputs_to_make:
                output_function = self.OUTPUT_FUNCTIONS_MAP.get(summary_output)
                if output_function:
                    new_summary_output = new_outputs.get(summary_output, [])
                    new_summary_output.append(
                        output_function(program_directory, self._outputs_mapper)
                    )
                    new_outputs[summary_output] = new_summary_output
            if clear_outputs:
                summary_output_helpers.clear_directory(program_directory)
            else:
                summary_output_helpers.mark_outputs_to_keep(program_directory)
        combined_outputs: dict[str, pd.DataFrame] = self.combine_outputs(
            legacy_outputs, new_outputs
        )
        self.save_summary_files(combined_outputs)

    def parse_output_functions(self, output_config: dict) -> list[str]:
        return [output for output, wanted in output_config.items() if wanted]

    def get_legacy_outputs(self) -> dict[str, pd.DataFrame]:
        legacy_outputs: dict[str, pd.DataFrame] = {}
        for summary_output in self._summary_outputs_to_make:
            legacy_outputs[summary_output] = summary_output_helpers.get_summary_file(
                self._output_path, summary_output + ".csv"
            )
        return legacy_outputs

    def combine_outputs(
        self, old_outputs: dict[str, pd.DataFrame], new_outputs: dict[str, list[pd.DataFrame]]
    ) -> dict[str, pd.DataFrame]:
        combined_outputs: dict[str, pd.DataFrame] = {}
        for output_name, output in new_outputs.items():
            if old_outputs[output_name].empty:
                combined_outputs[output_name] = pd.concat(output, ignore_index=True)
            else:
                output.insert(0, old_outputs[output_name])
                combined_outputs[output_name] = pd.concat(output, ignore_index=True)

        return combined_outputs

    def save_summary_files(self, combined_outputs: dict[str, pd.DataFrame]):
        for name, summary_output in combined_outputs.items():
            summary_output_helpers.save_summary_file(summary_output, self._output_path, name)

    def gen_cost_summary_outputs(self, non_baseline_prog):
        data_source_emis: Path = self._output_path / Output_Files.SummaryFileNames.EMIS_SUMMARY
        data_source_ts: Path = self._output_path / Output_Files.SummaryFileNames.TS_SUMMARY
        data_emis: pd.DataFrame = pd.read_csv(data_source_emis.with_suffix(".csv"))
        data_ts: pd.DataFrame = pd.read_csv(data_source_ts.with_suffix(".csv"))

        mitigation_data: pd.DataFrame = self.filter_program_mitigation(data_emis, non_baseline_prog)

        cost_data: pd.DataFrame = self.filter_program_costs(data_ts, non_baseline_prog)

        combined_df: pd.DataFrame = pd.merge(
            mitigation_data,
            cost_data,
            on=[
                output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
                output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.SIM,
            ],
        )

        self.gen_cost_to_mitigation_ratio(combined_df, non_baseline_prog)
        self.gen_cost_of_mitigated_emissions(combined_df, non_baseline_prog)

        name = Output_Files.SummaryFileNames.COST_SUMMARY + ".csv"

        summary_output_helpers.save_summary_file(combined_df, self._output_path, name)

    def gen_cost_of_mitigated_emissions(self, cost_df, program_names) -> None:
        """Generate a DataFrame with the cost of mitigated emissions for each program"""

        # Initialize the column for the cost of mitigated emissions
        cost_df[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.COST_OF_MITIGATED_EMIS] = 0.0

        # Iterate over each program name
        for program_name in program_names:
            # Calculate the cost of mitigated emissions for each row
            mask = (
                cost_df[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
                == program_name
            )
            cost_df.loc[
                mask, output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.COST_OF_MITIGATED_EMIS
            ] = (
                cost_df.loc[mask, output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION]
                * cc.KG_TO_MMBTU
                * self._program_cost_info[program_name][pp.NATGAS]
            )
        return

    def gen_cost_to_mitigation_ratio(self, cost_mit_df, program_names) -> None:
        """Generate a DataFrame with cost to mitigation ratios for each program"""

        # Initialize the column for cost-to-mitigation ratios
        cost_mit_df[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION_RATIO] = 0.0

        # Iterate over each program name
        for program_name in program_names:
            # Calculate the cost-to-mitigation ratio for each row
            mask = (
                cost_mit_df[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
                == program_name
            )
            cost_mit_df.loc[
                mask, output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION_RATIO
            ] = (
                cost_mit_df.loc[
                    mask, output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.TOTAL_COST
                ]
                / (
                    cost_mit_df.loc[
                        mask, output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION
                    ]
                    / 1000
                )
                * self._program_cost_info[program_name][pp.GWP]
            )

        return

    def filter_program_costs(self, ts_summary_info, program_names) -> pd.DataFrame:
        """Filter DataFrame to return cost columns and rows with program names in program_names"""
        filtered_df = ts_summary_info.loc[
            ts_summary_info[output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME].isin(
                program_names
            ),
            [
                output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
                output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.SIM,
                output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.TOT_COST,
            ],
        ]
        filtered_df.rename(
            columns={
                output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.TOT_COST: output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.TOTAL_COST
            },
            inplace=True,
        )
        return filtered_df

    def filter_program_mitigation(self, emis_summary_info, program_names) -> pd.DataFrame:
        """Filter dataframe to return mitigation columns and rows with program names in program_names"""
        filtered_df = emis_summary_info.loc[
            emis_summary_info[output_file_constants.TS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME].isin(
                program_names
            ),
            [
                output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
                output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.SIM,
                output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOT_MIT,
            ],
        ]
        filtered_df.rename(
            columns={
                output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOT_MIT: output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION,
            },
            inplace=True,
        )
        return filtered_df
