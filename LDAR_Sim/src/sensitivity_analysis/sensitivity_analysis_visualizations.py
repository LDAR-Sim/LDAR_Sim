# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        sensitivity_analysis_visualizations.py
# Purpose:     Core logic for generating sensitivity analysis visualizations
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
from typing import Tuple

import matplotlib.colors
import matplotlib.patches
import numpy as np
import pandas as pd
import seaborn as sns
from constants import sensitivity_analysis_constants
from file_processing.output_processing import output_utils
from matplotlib import pyplot as plt
from matplotlib import ticker
from sensitivity_analysis import sensitivity_visualization_helpers


def gen_true_vs_est_emissions_percent_difference_sens_viz(
    out_dir: str,
):
    data_source: pd.DataFrame = pd.read_csv(
        os.path.join(
            out_dir,
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).SENSITIVITY_TRUE_VS_ESTIMATED
            + ".csv",
        )
    )

    sens_data_for_plotting: dict[str, dict[str, list[float]]] = (
        sensitivity_visualization_helpers.extract_sensitivity_data(
            data_source=data_source,
            metrics=[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.PERCENT_DIFFERENCE
            ],
        )
    )

    len_unique_sens_sets = len(sens_data_for_plotting.keys())

    plot: plt.Figure = plt.figure()
    plot_ax: plt.Axes = plt.gca()
    legend_elements: list = []
    colors = sns.color_palette("husl", n_colors=len_unique_sens_sets)
    # Plot the density KDE for each sensitivity set
    for index, (sensitivity_set, data) in enumerate(sens_data_for_plotting.items()):
        sensitivity_visualization_helpers.plot_density_kde(
            legend_elements,
            plot_ax,
            data[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.PERCENT_DIFFERENCE
            ],
            sensitivity_set,
            colors[index],
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmissionsPercentDiffSensPlot.BIN_RANGE,
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmissionsPercentDiffSensPlot.X_LABEL,
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmissionsPercentDiffSensPlot.Y_LABEL,
            bin_width=(
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmissionsPercentDiffSensPlot.BIN_WIDTH,
        )
    plot_ax.xaxis.set_major_formatter(ticker.FuncFormatter(output_utils.percentage_formatter))
    plt.legend(handles=legend_elements)
    save_path: str = os.path.join(
        out_dir,
        sensitivity_analysis_constants.SensitivityAnalysisOutputs.SENSITIVITY_TRUE_VS_ESTIMATED_PD,
    )
    plt.savefig(save_path)
    plt.close(plot)


def gen_true_vs_est_emissions_violin_sens_viz(out_dir: str):
    data_source: pd.DataFrame = pd.read_csv(
        os.path.join(
            out_dir,
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).SENSITIVITY_TRUE_VS_ESTIMATED
            + ".csv",
        )
    )

    sens_data_for_plotting: dict = sensitivity_visualization_helpers.extract_sensitivity_data(
        data_source=data_source,
        metrics=[
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmisionsSens.TRUE_EMISSIONS,
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS,
        ],
    )
    # Get the number of unique sensitivity sets
    num_unique_sens_sets: int = len(sens_data_for_plotting.keys())

    # Create the plot
    plot: plt.Figure = plt.figure(figsize=(11, 7))
    plot_ax: plt.Axes = plt.gca()

    # Define the colors for the paired violin graphs
    colors: list[Tuple[float, float, float, float]] = [
        matplotlib.colors.to_rgba("blue", alpha=1),
        matplotlib.colors.to_rgba("orange", alpha=1),
    ]

    # Plot paired violin graphs for each sensitivity set
    for sensitivity_set, data in sens_data_for_plotting.items():
        # Get the "True" Emissions data for the sensitivity set
        true_emis_data: np.ndarray = np.array(
            data[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.TRUE_EMISSIONS
            ]
        )

        # Plot the "True" Emissions data violin for the sensitivity set
        sensitivity_visualization_helpers.plot_violin(
            plot_ax,
            colors[0],
            true_emis_data,
            sensitivity_set * 2,
        )

        # Get the "Estimated" Emissions data for the sensitivity set
        est_emis_data: np.ndarray = np.array(
            data[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS
            ]
        )

        # Plot the "Estimated" Emissions data violin for the sensitivity set
        sensitivity_visualization_helpers.plot_violin(
            plot_ax,
            colors[1],
            est_emis_data,
            sensitivity_set * 2 + 1,
        )

    # Calculate the maximum y value for the plot
    y_max: float = max(
        data_source[
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmisionsSens.TRUE_EMISSIONS
        ].max(),
        data_source[
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS
        ].max(),
    )

    # Format the paired violin plot
    sensitivity_visualization_helpers.format_paired_violin_plot(
        ax=plot_ax, num_unique_sens_sets=num_unique_sens_sets, colors=colors, y_max=y_max
    )

    # Save and close the plot
    save_path: str = os.path.join(
        out_dir,
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).SENSITIVITY_TRUE_VS_ESTIMATED_VIOLIN,
    )
    plt.savefig(save_path)
    plt.close(plot)
