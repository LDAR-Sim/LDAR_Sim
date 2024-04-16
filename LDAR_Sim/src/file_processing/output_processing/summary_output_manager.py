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
from file_processing.output_processing import summary_outputs, summary_output_helpers
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper


class SummaryOutputManager:

    OUTPUT_FUNCTIONS_MAP = {
        Output_Files.SummaryFileNames.TS_SUMMARY: (summary_outputs.generate_timeseries_summary),
        Output_Files.SummaryFileNames.EMIS_SUMMARY: (summary_outputs.generate_emissions_summary),
    }

    def __init__(self, output_path: Path, output_config: dict, sim_years: list[int]):
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
                self._output_path, summary_output
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
