# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        sensitivity_visualization_helpers.py
# Purpose:     Logic to help with preprocessing, calculations and filtering
#             of sensitivity analysis data for visualization
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

from typing import Tuple, Union

import matplotlib.patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from constants import sensitivity_analysis_constants
from file_processing.output_processing import summary_visualization_helpers
from file_processing.output_processing.summary_visualization_helpers import (
    format_tick_labels_with_metric_prefix,
)
from matplotlib import lines, ticker


def extract_sensitivity_data(data_source: pd.DataFrame, metrics: list[str]):
    """
    Extracts sensitivity data from the given data source for the specified metrics.
    The sensitivity data is extracted for each unique sensitivity set.

    Args:
        data_source (pd.DataFrame): The data source containing the sensitivity data.
        metrics (list[str]): The list of metrics to extract sensitivity data for.
        A metric is a string that corresponds to a column in the data source.

    Returns:
        dict[str, dict[str, list[float]]]: A dictionary containing the extracted sensitivity data.
            The keys of the outer dictionary are the unique sensitivity sets.
            The keys of the inner dictionary are the metrics.
            The values of the inner dictionary are lists of sensitivity data for each metric.
    """

    sens_data_for_plotting: dict[str, dict[str, list[float]]] = {}

    unique_sens_sets: np.ndarray = data_source[
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).TrueEstimatedEmisionsSens.SENSITIVITY_SET
    ].unique()

    unique_sens_years: np.ndarray = data_source[
        (sensitivity_analysis_constants.SensitivityAnalysisOutputs).TrueEstimatedEmisionsSens.YEAR
    ].unique()

    for sensitivity_set in unique_sens_sets:
        sens_data_for_plotting[sensitivity_set] = {}
        for metric in metrics:
            sens_data_for_plotting[sensitivity_set][metric] = []

        for year in unique_sens_years:
            # Get the true emissions for the sensitivity set and year
            percent_diff_series: pd.Series = data_source.loc[
                (
                    data_source[
                        (
                            sensitivity_analysis_constants.SensitivityAnalysisOutputs
                        ).TrueEstimatedEmisionsSens.SENSITIVITY_SET
                    ]
                    == sensitivity_set
                )
                & (
                    data_source[
                        (
                            sensitivity_analysis_constants.SensitivityAnalysisOutputs
                        ).TrueEstimatedEmisionsSens.YEAR
                    ]
                    == year
                ),
                metrics,
            ]

            for metric in metrics:
                sens_data_for_plotting[sensitivity_set][metric].extend(
                    list(percent_diff_series[metric].values)
                )

    return sens_data_for_plotting


def plot_violin(
    ax: plt.Axes,
    color: Tuple[float, float, float, float],
    data: np.ndarray,
    index: int,
):
    data_median: float = np.median(data)
    data_quartiles: Tuple[float, float] = np.percentile(data, [25, 75], method="median_unbiased")
    data_interquartile_range: float = data_quartiles[1] - data_quartiles[0]
    data_whiskers: Tuple[float, float] = (
        max(data_quartiles[0] - 1.5 * data_interquartile_range, np.min(data)),
        min(data_quartiles[1] + 1.5 * data_interquartile_range, np.max(data)),
    )
    violin_plot_data: np.ndarray = data[data < data_quartiles[1]]
    scatter_plot_data: np.ndarray = data[data >= data_quartiles[1]]

    violin_parts: dict = ax.violinplot(
        dataset=violin_plot_data,
        positions=[index],
        widths=0.5,
        showmeans=False,
        showmedians=False,
        showextrema=False,
    )

    plt.scatter([index] * len(scatter_plot_data), scatter_plot_data, color="black", s=5)

    plt.scatter([index], [data_median], color="white", marker="o", s=15, zorder=3)

    plt.vlines(
        [index],
        data_quartiles[0],
        data_quartiles[1],
        color="black",
        linestyle="-",
        linewidth=5,
    )

    plt.vlines(
        [index],
        data_whiskers[0],
        data_whiskers[1],
        color="black",
        linestyle="-",
        linewidth=1,
    )

    for part in violin_parts["bodies"]:
        part.set_facecolor(color)
        part.set_edgecolor("black")
        part.set_alpha(1)


def format_paired_violin_plot(
    ax: plt.Axes,
    num_unique_sens_sets: int,
    colors: list[Tuple[float, float, float, float]],
    y_max: float,
):
    ax.set_xticks(np.arange(0.5, num_unique_sens_sets * 2, 2))
    ax.set_xticklabels(
        np.arange(0, num_unique_sens_sets, 1),
    )
    ax.set_xlabel(
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).TrueEstimatedEmissionsViolinSensPlot.X_LABEL
    )
    ax.set_ylabel(
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).TrueEstimatedEmissionsViolinSensPlot.Y_LABEL
    )
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(summary_visualization_helpers.format_tick_labels_with_metric_prefix)
    )
    ax.set_ylim(
        0,
        1.1 * y_max,
    )

    plt.legend(
        handles=[
            matplotlib.patches.Patch(
                color=colors[0],
                label=(
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmissionsViolinSensPlot.TRUE_EMIS_LABEL,
            ),
            matplotlib.patches.Patch(
                color=colors[1],
                label=(
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmissionsViolinSensPlot.ESTIMATED_EMIS_LABEL,
            ),
        ],
        loc="upper right",
    )
    plt.tight_layout()


def plot_density_kde(
    legend_elements: list,
    ax: plt.Axes,
    x_values: list,
    sensitivity_set: str,
    color: Tuple[float, float, float],
    bin_range: Tuple[float, float],
    x_label: str,
    y_label: str,
    legend_label: str = None,
    bin_width: float = 0,
    bins: Union[int, str] = "auto",
    x_locator: ticker.Locator = ticker.AutoLocator(),
    y_locator: ticker.Locator = ticker.MaxNLocator(nbins="auto", integer=True, prune=None),
):
    if bin_width == 0:
        sns.histplot(
            x_values,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binrange=bin_range,
            bins=bins,
            stat="percent",
            fill=False,
            alpha=0.0,
            multiple="layer",
        )
    else:
        sns.histplot(
            x_values,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binwidth=bin_width,
            binrange=bin_range,
            stat="percent",
            fill=False,
            alpha=0.0,
            multiple="layer",
        )

    legend_elements.append(
        lines.Line2D(
            [0],
            [0],
            color=color,
            label=legend_label if legend_label else sensitivity_set,
            markerfacecolor=color,
            markersize=15,
        )
    )
    if x_label and y_label:
        ax.set(
            xlabel=x_label,
            ylabel=y_label,
        )

    ax.xaxis.set_major_locator(locator=x_locator)
    ax.yaxis.set_major_locator(locator=y_locator)

    # Set custom formatter for x-axis
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_tick_labels_with_metric_prefix))
