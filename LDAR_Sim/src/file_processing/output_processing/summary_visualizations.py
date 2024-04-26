"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        summary_visualizations.py
Purpose: Contains functions to generate summary visualizations for the LDAR-Sim output.

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

from pathlib import Path
from typing import Tuple

from matplotlib import lines, pyplot as plt, ticker
import numpy as np
import pandas as pd
import matplotlib.scale as mscale
import scipy.stats

# import scipy.stats
from constants import output_file_constants, file_name_constants
from file_processing.output_processing import output_utils, summary_visualization_helpers
from file_processing.output_processing.scaling import QuantileScale
from file_processing.output_processing.summary_visualization_mapper import (
    SummaryVisualizationMapper,
)
import seaborn as sns


def plot_histograms(
    colors: Tuple[list[Tuple[float, float, float]]],
    program_hist_stats: dict[str, list[float] | Tuple[list[float], list[float]]],
    combine_program_histograms: bool,
    visualization_dir: Path,
    visualization_name: str,
    viz_mapper: SummaryVisualizationMapper,
    save_separate_plots: bool = True,
):
    # Determine the dimensionality of the histogram statistics
    # This is used to determine how many histograms to plot for each program
    hist_stat_dimensionality: int = 1
    for key, value in program_hist_stats.items():
        if not isinstance(value, tuple):
            program_hist_stats[key] = (value,)  # Treat non-tuple values as 1-tuple
            value = program_hist_stats[key]
        hist_stat_dimensionality = len(value)

    # Lookup the histogram properties from the visualization mapper
    histogram_properties: dict = viz_mapper.get_histogram_properties(visualization_name)
    x_axis_formatter: ticker.FuncFormatter | None = viz_mapper.get_x_axis_formatter(
        visualization_name
    )

    for accessor, hist_properties in enumerate(histogram_properties.values()):
        summary_visualization_helpers.calculate_histogram_bin_range(
            program_hist_stats, hist_properties, accessor
        )

    # Setup a figure and axes for a combined histogram plot for all programs
    if combine_program_histograms:
        combined_plot: plt.Figure = plt.figure()
        combined_plot_ax: plt.Axes = plt.gca()

    # Setup list of legend elements
    legend_elements = []

    # Pop the legend label(s) from the histogram properties so it/they can be used dynamically
    if hist_stat_dimensionality > 1:
        legend_labels: tuple = tuple(
            histogram_properties[f"hist{dim}"].pop("legend_label", None)
            for dim in range(hist_stat_dimensionality)
        )
    else:
        legend_labels: tuple = (histogram_properties.pop("legend_label", None),)

    for accessor, (program_name, stat) in enumerate(program_hist_stats.items()):
        if save_separate_plots:
            # Setup a figure and axes for a separated histogram plot for each program
            separated_plot: plt.Figure = plt.figure()
            separated_plot_ax: plt.Axes = plt.gca()

            for val in range(hist_stat_dimensionality):
                if legend_labels[val] is not None:
                    legend_label_to_use = " ".join([program_name, legend_labels[val]])
                else:
                    legend_label_to_use = None
                # Plot the histogram for the program
                summary_visualization_helpers.plot_hist_percent_occurrence_with_smoothed_curved(
                    legend_elements=legend_elements,
                    ax=separated_plot_ax,
                    x_values=stat[val],
                    program_name=program_name,
                    color=colors[val][accessor],
                    legend_label=legend_label_to_use,
                    **histogram_properties[f"hist{val}"],
                )
            # If there is more than 1 histogram to plot, add a legend
            if hist_stat_dimensionality > 1:
                plt.legend(
                    handles=legend_elements[
                        (accessor * hist_stat_dimensionality) : (  # noqa 481
                            accessor * hist_stat_dimensionality
                        )
                        + hist_stat_dimensionality
                    ]
                )
            # Format and save the separated plot
            if x_axis_formatter:
                separated_plot_ax.xaxis.set_major_formatter(x_axis_formatter)
            save_path: Path = visualization_dir / f"{program_name}_{visualization_name}.png"
            plt.savefig(save_path)
            plt.close(separated_plot)

        if combine_program_histograms:
            plt.figure(combined_plot.number)
            for val in range(hist_stat_dimensionality):
                if legend_labels[val] is not None:
                    legend_label_to_use = " ".join([program_name, legend_labels[val]])
                else:
                    legend_label_to_use = None
                # Plot the histogram for the program on the combined plot
                summary_visualization_helpers.plot_hist_percent_occurrence_with_smoothed_curved(
                    legend_elements=legend_elements,
                    ax=combined_plot_ax,
                    x_values=stat[val],
                    program_name=program_name,
                    color=colors[val][accessor],
                    legend_label=legend_label_to_use,
                    **histogram_properties,
                )
    # Format and save the combined plot
    if combine_program_histograms:
        if x_axis_formatter:
            combined_plot_ax.xaxis.set_major_formatter(x_axis_formatter)
        plt.legend(handles=legend_elements)
        save_path: Path = visualization_dir / visualization_name
        plt.savefig(save_path)
        plt.close(combined_plot)


def plot_probit(
    colors: Tuple[list[Tuple[float, float, float]]],
    probit_data: dict[str, list[float] | Tuple[list[float], list[float]]],
    combine_program_plots: bool,
    visualization_dir: Path,
    visualization_name: str,
    viz_mapper: SummaryVisualizationMapper,
    save_separate_plots: bool = True,
):
    probit_stat_dimensionality: int = 1
    for key, value in probit_data.items():
        if not isinstance(value, tuple):
            probit_data[key] = (value,)
            value = probit_data[key]
        probit_stat_dimensionality = len(value)

    probit_properties: dict = viz_mapper.get_probit_properties(visualization_name)

    legend_elements: list = []

    mscale.register_scale(QuantileScale)

    if combine_program_plots:
        combined_plot: plt.Figure = plt.figure()
        combined_plot_ax: plt.Axes = plt.gca()

    if probit_stat_dimensionality > 1:
        legend_labels: tuple = tuple(
            probit_properties[f"probit{dim}"].pop("legend_label", None)
            for dim in range(probit_stat_dimensionality)
        )
    else:
        legend_labels: tuple = (probit_properties.pop("legend_label", None),)

    for accessor, (program_name, stat) in enumerate(probit_data.items()):
        if save_separate_plots:
            separated_plot: plt.Figure = plt.figure()
            separated_plot_ax: plt.Axes = plt.gca()

            for val in range(probit_stat_dimensionality):
                if legend_labels[val] is not None:
                    legend_label_to_use = " ".join([program_name, legend_labels[val]])
                else:
                    legend_label_to_use = None

                x_values: np.ndarray = np.sort(stat[val])
                x_values = x_values[x_values > 0]
                y_values: np.ndarray = scipy.stats.mstats.plotting_positions(
                    x_values, alpha=(1.0 / 3.0), beta=(1.0 / 3.0)
                )

                plt.scatter(
                    x_values,
                    y_values,
                    color=colors[val][accessor],
                    label=legend_label_to_use,
                    marker="d",
                    facecolors="none",
                    edgecolors=colors[val][accessor],
                    s=15,
                )

                separated_plot_ax.set_yscale("quantile")
                separated_plot_ax.set_xscale("log")

                separated_plot_ax.xaxis.set_major_formatter(
                    ticker.FuncFormatter(
                        summary_visualization_helpers.format_tick_labels_with_metric_prefix
                    )
                )
                major_locator, minor_locator = (
                    summary_visualization_helpers.format_major_minor_ticks_log_scale(
                        10, x_values.max(), x_values.min()
                    )
                )
                major_locator: ticker.LogLocator
                minor_locator: ticker.LogLocator
                separated_plot_ax.xaxis.set_major_locator(major_locator)
                separated_plot_ax.xaxis.set_minor_locator(minor_locator)
                separated_plot_ax.xaxis.set_minor_formatter(ticker.NullFormatter())
                separated_plot_ax.tick_params(axis="x", which="major", labelsize=8)

                plt.xticks(rotation=45)

                best_fit_coefficients: np.ndarray = np.polyfit(
                    np.log(x_values), scipy.stats.norm.ppf(y_values), 1
                )

                best_fit_line_y_intermediate: np.ndarray = (
                    best_fit_coefficients[0] * np.log(x_values) + best_fit_coefficients[1]
                )

                best_fit_line_y_values: np.ndarray = scipy.stats.norm.cdf(
                    best_fit_line_y_intermediate
                )

                plt.plot(
                    x_values, best_fit_line_y_values, color=colors[val][accessor], linestyle="--"
                )

                separated_plot_ax.set_xlabel(probit_properties[f"probit{val}"]["x_label"])
                separated_plot_ax.set_ylabel(probit_properties[f"probit{val}"]["y_label"])

                legend_elements.append(
                    lines.Line2D(
                        [0],
                        [0],
                        color=colors[val][accessor],
                        label=legend_label_to_use,
                        markersize=15,
                    )
                )

                plt.tight_layout()
                plt.grid(True)

            if probit_stat_dimensionality > 1:
                plt.legend(
                    handles=legend_elements[
                        (accessor * probit_stat_dimensionality) : (  # noqa 481
                            accessor * probit_stat_dimensionality
                        )
                        + probit_stat_dimensionality
                    ]
                )

            save_path: Path = visualization_dir / f"{program_name}_{visualization_name}.png"
            plt.savefig(save_path)
            plt.close(separated_plot)

        if combine_program_plots:
            plt.figure(combined_plot.number)

            for val in range(probit_stat_dimensionality):
                if legend_labels[val] is not None:
                    legend_label_to_use = " ".join([program_name, legend_labels[val]])
                else:
                    legend_label_to_use = None

                x_values: np.ndarray = np.sort(stat[val])
                y_values: np.ndarray = scipy.stats.mstats.plotting_positions(
                    x_values, alpha=(1.0 / 3.0), beta=(1.0 / 3.0)
                )

                plt.scatter(
                    x_values,
                    y_values,
                    color=colors[val][accessor],
                    label=legend_label_to_use,
                    marker="d",
                    facecolors="none",
                    edgecolors=colors[val][accessor],
                    s=15,
                )

                combined_plot_ax.set_yscale("quantile")
                combined_plot_ax.set_xscale("log")

                combined_plot_ax.xaxis.set_major_formatter(
                    ticker.FuncFormatter(
                        summary_visualization_helpers.format_tick_labels_with_metric_prefix
                    )
                )
                combined_plot_ax.xaxis.set_major_locator(
                    ticker.LogLocator(base=10, subs=np.arange(0, 20))
                )
                combined_plot_ax.xaxis.set_minor_locator(ticker.NullLocator())
                combined_plot_ax.xaxis.set_minor_formatter(ticker.NullFormatter())

                plt.xticks(rotation=-60)

                best_fit_coefficients: np.ndarray = np.polyfit(
                    np.log(x_values), scipy.stats.norm.ppf(y_values), 1
                )

                best_fit_line_y_intermediate: np.ndarray = (
                    best_fit_coefficients[0] * np.log(x_values) + best_fit_coefficients[1]
                )

                best_fit_line_y_values: np.ndarray = scipy.stats.norm.cdf(
                    best_fit_line_y_intermediate
                )

                plt.plot(
                    x_values, best_fit_line_y_values, color=colors[val][accessor], linestyle="--"
                )

                plt.tight_layout()
                plt.grid(True)

    if combine_program_plots:
        save_path: Path = visualization_dir / visualization_name
        plt.savefig(save_path)
        plt.close(combined_plot)


def gen_estimated_vs_true_emissions_percent_difference_plot(
    out_dir: Path,
    visualization_dir: Path,
    baseline_program: str,
    combine_program_histograms: bool,
    viz_mapper: SummaryVisualizationMapper,
):
    data_source: Path = out_dir / file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    data: pd.DataFrame = pd.read_csv(data_source.with_suffix(".csv"))
    visualization_name: str = output_file_constants.FileNames.TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT

    program_names: list[str] = summary_visualization_helpers.get_non_baseline_prog_names(
        data, baseline_program
    )
    annualized_emissions_data: dict[Tuple[list[float], list[float]]] = (
        summary_visualization_helpers.gen_annual_emissions_summary_list(data, program_names)
    )
    true_and_estimated_percent_differences: dict = (
        summary_visualization_helpers.gen_true_estimated_annualized_statistics(
            output_file_constants.SummaryVisualizationStatistics.PERCENT_DIFFERENCE,
            annualized_emissions_data,
            viz_mapper,
        )
    )

    colors = sns.color_palette("husl", n_colors=len(program_names))

    plot_histograms(
        (colors,),
        true_and_estimated_percent_differences,
        combine_program_histograms,
        visualization_dir,
        visualization_name,
        viz_mapper,
    )


def gen_estimated_vs_true_emissions_relative_difference_plot(
    out_dir: Path,
    visualization_dir: Path,
    baseline_program: str,
    combine_program_histograms: bool,
    viz_mapper: SummaryVisualizationMapper,
):
    data_source: Path = out_dir / file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    data: pd.DataFrame = pd.read_csv(data_source.with_suffix(".csv"))
    visualization_name: str = output_file_constants.FileNames.TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT

    program_names: list[str] = summary_visualization_helpers.get_non_baseline_prog_names(
        data, baseline_program
    )
    annualized_emissions_data: dict[Tuple[list[float], list[float]]] = (
        summary_visualization_helpers.gen_annual_emissions_summary_list(data, program_names)
    )
    true_and_estimated_relative_differences: dict = (
        summary_visualization_helpers.gen_true_estimated_annualized_statistics(
            output_file_constants.SummaryVisualizationStatistics.RELATIVE_DIFFERENCE,
            annualized_emissions_data,
            viz_mapper,
        )
    )

    colors = sns.color_palette("husl", n_colors=len(program_names))

    plot_histograms(
        (colors,),
        true_and_estimated_relative_differences,
        combine_program_histograms,
        visualization_dir,
        visualization_name,
        viz_mapper,
    )


def gen_true_and_estimated_paired_emissions_distribution_plot(
    out_dir: Path,
    visualization_dir: Path,
    baseline_program: str,
    combine_program_histograms: bool,
    viz_mapper: SummaryVisualizationMapper,
):
    data_source: Path = out_dir / file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    data: pd.DataFrame = pd.read_csv(data_source.with_suffix(".csv"))
    visualization_name: str = (
        output_file_constants.FileNames.TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT
    )

    program_names: list[str] = summary_visualization_helpers.get_non_baseline_prog_names(
        data, baseline_program
    )
    annualized_emissions_data: dict[Tuple[list[float], list[float]]] = (
        summary_visualization_helpers.gen_annual_emissions_summary_list(data, program_names)
    )

    colors = sns.color_palette("husl", n_colors=len(program_names))

    colors_paired = (
        [output_utils.luminance_shift(color, lighten=False) for color in colors],
        [output_utils.luminance_shift(color, lighten=True) for color in colors],
    )

    plot_histograms(
        colors_paired,
        annualized_emissions_data,
        combine_program_histograms,
        visualization_dir,
        visualization_name,
        viz_mapper,
    )


def gen_true_and_estimated_paired_probit_plot(
    out_dir: Path,
    visualization_dir: Path,
    baseline_program: str,
    combine_program_plots: bool,
    viz_mapper: SummaryVisualizationMapper,
):
    data_source: Path = out_dir / file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    data: pd.DataFrame = pd.read_csv(data_source.with_suffix(".csv"))
    visualization_name: str = output_file_constants.FileNames.TRUE_AND_ESTIMATED_PAIRED_PROBIT_PLOT

    program_names: list[str] = summary_visualization_helpers.get_non_baseline_prog_names(
        data, baseline_program
    )
    annualized_emissions_data: dict[Tuple[list[float], list[float]]] = (
        summary_visualization_helpers.gen_annual_emissions_summary_list(data, program_names)
    )

    colors = sns.color_palette("husl", n_colors=len(program_names))

    colors_paired = (
        [output_utils.luminance_shift(color, lighten=False) for color in colors],
        [output_utils.luminance_shift(color, lighten=True) for color in colors],
    )

    plot_probit(
        colors_paired,
        annualized_emissions_data,
        combine_program_plots,
        visualization_dir,
        visualization_name,
        viz_mapper,
    )
