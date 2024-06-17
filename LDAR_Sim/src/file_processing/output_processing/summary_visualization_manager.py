"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        summary_visualization_manager.py
Purpose:  Contains the SummaryVisualizationManager class, which is responsible
for generating summary visualizations.

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
from constants import output_file_constants, output_messages
from file_processing.output_processing import summary_visualizations
from matplotlib import pyplot as plt
from file_processing.output_processing.summary_visualization_mapper import (
    SummaryVisualizationMapper,
)


class SummaryVisualizationManager:
    OUTPUT_VISUALIZATION_FUNCTIONS_MAP = {
        output_file_constants.SummaryOutputVizFileNames.TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT: (
            summary_visualizations.gen_estimated_vs_true_emissions_percent_difference_plot
        ),
        output_file_constants.SummaryOutputVizFileNames.TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT: (
            summary_visualizations.gen_estimated_vs_true_emissions_relative_difference_plot
        ),
        (
            output_file_constants.SummaryOutputVizFileNames
        ).TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT: (
            summary_visualizations.gen_true_and_estimated_paired_emissions_distribution_plot
        ),
        output_file_constants.SummaryOutputVizFileNames.TRUE_AND_ESTIMATED_PAIRED_PROBIT_PLOT: (
            summary_visualizations.gen_true_and_estimated_paired_probit_plot
        ),
        output_file_constants.SummaryOutputVizFileNames.PROGRAM_MITIGATION_BAR_PLOT: (
            summary_visualizations.gen_program_mitigation_bars
        ),
        output_file_constants.SummaryOutputVizFileNames.STACKED_COST_BAR_PLOT: (
            summary_visualizations.gen_program_stacked_cost_bars
        ),
        output_file_constants.SummaryOutputVizFileNames.COST_TO_MIT_BOX_PLOT: (
            summary_visualizations.gen_cost_to_mit_boxplot
        ),
    }

    def __init__(
        self,
        output_config: dict,
        output_dir: Path,
        baseline_program: str,
        site_count: int,
    ):
        self.summary_visualizations_to_make: list[str] = self.parse_visualization_functions(
            output_config[output_file_constants.OutputConfigCategories.SUMMARY_VISUALIZATIONS]
        )
        self.baseline_program: str = baseline_program
        self.output_dir: Path = output_dir
        self.summary_visualizations_dir: Path = (
            output_dir / output_file_constants.FileDirectory.SUMMARY_PROGRAM_PLOTS_DIRECTORY
        )
        self._visualization_mapper: SummaryVisualizationMapper = SummaryVisualizationMapper(
            site_count
        )

        self._visualization_mapper.update_with_user_defined_summary_settings(
            output_config[
                output_file_constants.OutputConfigCategories.SUMMARY_VISUALIZATION_SETTINGS
            ]
        )

    def gen_visualizations(self):
        # Print a message to the console indicating that
        # the summary visualizations are being generated
        print(output_messages.SUMMARY_PLOT_GENERATION_MESSAGE)
        # Create a directory to store the summary visualizations
        os.makedirs(self.summary_visualizations_dir)
        # Call the visualization functions for each summary visualization
        for summary_visualization in self.summary_visualizations_to_make:
            visualization_function = self.OUTPUT_VISUALIZATION_FUNCTIONS_MAP.get(
                summary_visualization
            )
            if visualization_function:
                visualization_function(
                    self.output_dir,
                    self.summary_visualizations_dir,
                    self.baseline_program,
                    False,
                    self._visualization_mapper,
                )
        plt.close("all")

    def parse_visualization_functions(self, output_config: dict) -> list[str]:
        return [output for output, wanted in output_config.items() if wanted]
