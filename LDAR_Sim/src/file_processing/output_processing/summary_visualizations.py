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

import matplotlib.scale as mscale
import numpy as np
import pandas as pd
import seaborn as sns

from constants import file_name_constants, output_file_constants
from file_processing.output_processing import output_utils, summary_visualization_helpers
from file_processing.output_processing.scaling import QuantileScale
from file_processing.output_processing.summary_visualization_mapper import (
    SummaryVisualizationMapper,
)
from matplotlib import pyplot as plt
from matplotlib import ticker


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
    x_axis_formatter: ticker.FuncFormatter | None = viz_mapper.get_axis_formatter(
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

                summary_visualization_helpers.plot_probabilities_lognormal_probit_with_best_fit(
                    x_vals=stat[val],
                    color=colors[val][accessor],
                    legend_label=legend_label_to_use,
                    axis=separated_plot_ax,
                    legend_elements=legend_elements,
                    **probit_properties[f"probit{val}"],
                )

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

                summary_visualization_helpers.plot_probabilities_lognormal_probit_with_best_fit(
                    x_vals=stat[val],
                    color=colors[val][accessor],
                    legend_label=legend_label_to_use,
                    axis=combined_plot_ax,
                    legend_elements=legend_elements,
                    **probit_properties[f"probit{val}"],
                )

    if combine_program_plots:
        save_path: Path = visualization_dir / visualization_name
        plt.savefig(save_path)
        plt.close(combined_plot)


def plot_box_whisker(
    cost_mit_ratio_data: pd.DataFrame,
    visualization_dir: Path,
    visualization_name: str,
    viz_mapper: SummaryVisualizationMapper,
):
    box_plot_properties: dict = viz_mapper.get_boxplot_properties(visualization_name)

    x_label: str = box_plot_properties.pop("x_label")
    y_label: str = box_plot_properties.pop("y_label")
    # Group by 'program name' and collect 'mitigation_ratio' values into lists
    grouped_data = (
        cost_mit_ratio_data.groupby(output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME)[
            output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION_RATIO
        ]
        .apply(list)
        .reset_index(name=output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION_RATIO)
    )
    labels = grouped_data[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME].tolist()
    data_to_plot = grouped_data[
        output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION_RATIO
    ].tolist()

    figure: plt.Figure = plt.figure(figsize=(11, 7))  # noqa 841
    ax: plt.Axes = plt.gca()
    ax.boxplot(data_to_plot, labels=labels, **box_plot_properties)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.tight_layout()

    save_path: Path = visualization_dir / visualization_name
    plt.savefig(save_path)
    plt.close(figure)


def plot_stack_bar_chart(
    cost_data: pd.DataFrame,
    visualization_dir: Path,
    visualization_name: str,
    viz_mapper: SummaryVisualizationMapper,
):
    bar_chart_properties: dict = viz_mapper.get_bar_chart_properties(visualization_name)
    y_axis_formatter: ticker.FuncFormatter | None = viz_mapper.get_axis_formatter(
        visualization_name
    )
    # Extract NET_COST and remove it from cost_data
    net_cost = cost_data.pop(output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.NET_COST)

    x_label: str = bar_chart_properties.pop("x_label")
    y_label: str = bar_chart_properties.pop("y_label")

    figure: plt.Figure = plt.figure(figsize=(11, 7))  # noqa 841
    ax: plt.Axes = plt.gca()
    cost_data.plot(
        x=output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
        kind="bar",
        stacked=True,
        ax=ax,
    )
    # Plot NET_COST as dots on top of the stacked bar chart
    program_names = cost_data[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
    x_positions = range(len(program_names))  # Assuming program names are on the x-axis
    ax.scatter(
        x_positions,
        net_cost,
        color="black",
        zorder=5,
        label=output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.NET_COST,
    )  # zorder=5 to plot dots above bars

    # Add text labels for each dot to display the actual Net Cost value
    for x_pos, net_cost_value in zip(x_positions, net_cost):
        ax.text(
            x_pos + 0.02,
            net_cost_value,
            f"${net_cost_value:.2f}",  # Format the net cost value to two decimal places
            ha="left",
            va="bottom",
        )
    ax.legend()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.yaxis.set_major_formatter(y_axis_formatter)

    # Add a horizontal line at y=0.0
    ax.axhline(0, color="black")

    plt.tight_layout()

    save_path: Path = visualization_dir / visualization_name
    plt.savefig(save_path)
    plt.close(figure)


def plot_bar_chart(
    mitigation_data: dict[str, list[float]],
    visualization_dir: Path,
    visualization_name: str,
    viz_mapper: SummaryVisualizationMapper,
):
    x_axis_formatter: ticker.FuncFormatter | None = viz_mapper.get_axis_formatter(
        visualization_name
    )

    bar_chart_properties: dict = viz_mapper.get_bar_chart_properties(visualization_name)

    x_label: str = bar_chart_properties.pop("x_label")
    y_label: str = bar_chart_properties.pop("y_label")

    figure: plt.Figure = plt.figure(figsize=(11, 7))  # noqa 841
    ax: plt.Axes = plt.gca()
    for index, (program_name, mitigation_values) in enumerate(mitigation_data.items()):
        ax.barh(
            y=index,
            width=np.mean(mitigation_values),
            label=program_name,
            **bar_chart_properties,
        )

    ax.set_yticks(range(len(mitigation_data.keys())))
    ax.set_yticklabels(mitigation_data.keys())
    ax.xaxis.set_major_formatter(x_axis_formatter)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    plt.tight_layout()

    save_path: Path = visualization_dir / visualization_name
    plt.savefig(save_path)
    plt.close(figure)


def gen_estimated_vs_true_emissions_percent_difference_plot(
    out_dir: Path,
    visualization_dir: Path,
    baseline_program: str,
    combine_program_histograms: bool,
    viz_mapper: SummaryVisualizationMapper,
):
    data_source: Path = out_dir / file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    data: pd.DataFrame = pd.read_csv(data_source.with_suffix(".csv"))
    visualization_name: str = (
        output_file_constants.SummaryOutputVizFileNames.TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT
    )

    program_names: list[str] = summary_visualization_helpers.get_non_baseline_prog_names(
        data, baseline_program
    )
    annualized_emissions_data: dict[Tuple[list[float], list[float]]] = (
        summary_visualization_helpers.gen_annual_emissions_summary_list(data, program_names)
    )

    stat_function: callable = viz_mapper.get_summary_stat_function(
        output_file_constants.SummaryVisualizationStatistics.PERCENT_DIFFERENCE
    )
    true_and_estimated_percent_differences: dict = (
        summary_visualization_helpers.gen_true_estimated_annualized_statistics(
            stat_function,
            annualized_emissions_data,
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
    visualization_name: str = (
        output_file_constants.SummaryOutputVizFileNames.TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT
    )

    program_names: list[str] = summary_visualization_helpers.get_non_baseline_prog_names(
        data, baseline_program
    )
    annualized_emissions_data: dict[Tuple[list[float], list[float]]] = (
        summary_visualization_helpers.gen_annual_emissions_summary_list(data, program_names)
    )

    stat_function: callable = viz_mapper.get_summary_stat_function(
        output_file_constants.SummaryVisualizationStatistics.RELATIVE_DIFFERENCE
    )
    true_and_estimated_relative_differences: dict = (
        summary_visualization_helpers.gen_true_estimated_annualized_statistics(
            stat_function,
            annualized_emissions_data,
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
        output_file_constants.SummaryOutputVizFileNames
    ).TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT

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
    visualization_name: str = (
        output_file_constants.SummaryOutputVizFileNames.TRUE_AND_ESTIMATED_PAIRED_PROBIT_PLOT
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

    plot_probit(
        colors_paired,
        annualized_emissions_data,
        combine_program_plots,
        visualization_dir,
        visualization_name,
        viz_mapper,
    )


def gen_program_mitigation_bars(
    out_dir: Path,
    visualization_dir: Path,
    baseline_program: str,
    _,
    viz_mapper: SummaryVisualizationMapper,
):
    data_source: Path = out_dir / file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    data: pd.DataFrame = pd.read_csv(data_source.with_suffix(".csv"))
    visualization_name: str = (
        output_file_constants.SummaryOutputVizFileNames.PROGRAM_MITIGATION_BAR_PLOT
    )
    program_names: list[str] = summary_visualization_helpers.get_non_baseline_prog_names(
        data, baseline_program
    )
    annual_mitigation_data: dict[str, list[float]] = (
        summary_visualization_helpers.gen_annual_mitigation_summary_list(data, program_names)
    )
    # if no mitigation data was found, return
    if annual_mitigation_data is None:
        return
    plot_bar_chart(
        annual_mitigation_data,
        visualization_dir,
        visualization_name,
        viz_mapper,
    )


def gen_cost_to_mit_boxplot(
    out_dir: Path,
    visualization_dir: Path,
    baseline_program: str,
    _,
    viz_mapper: SummaryVisualizationMapper,
):
    data_source: Path = out_dir / file_name_constants.Output_Files.SummaryFileNames.COST_SUMMARY
    data: pd.DataFrame = pd.read_csv(data_source.with_suffix(".csv"))

    visualization_name: str = output_file_constants.SummaryOutputVizFileNames.COST_TO_MIT_BOX_PLOT

    filtered_data = data[
        [
            output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
            output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION_RATIO,
        ]
    ]
    # Mitigation ratio will be infinite if there is no mitigation.
    # if all mitigation ratios are infinite, do not plot.
    if np.isinf(
        filtered_data[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.MITIGATION_RATIO]
    ).all():
        return

    plot_box_whisker(
        filtered_data,
        visualization_dir,
        visualization_name,
        viz_mapper,
    )


def gen_program_stacked_cost_value_bars(
    out_dir: Path,
    visualization_dir: Path,
    baseline_program: str,
    _,
    viz_mapper: SummaryVisualizationMapper,
):
    data_source: Path = out_dir / file_name_constants.Output_Files.SummaryFileNames.COST_SUMMARY
    data: pd.DataFrame = pd.read_csv(data_source.with_suffix(".csv"))

    visualization_name: str = (
        output_file_constants.SummaryOutputVizFileNames.PROGRAM_COST_VALUE_BAR_PLOT
    )

    data = data[
        [
            output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
            output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.COST_OF_MITIGATED_EMIS,
            output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.TOTAL_COST,
        ]
    ]

    data = (
        data.groupby(output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME)
        .median()
        .reset_index()
    )

    data[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.TOTAL_COST] = -data[
        output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.TOTAL_COST
    ]

    data[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.NET_COST] = (
        data[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.TOTAL_COST]
        + data[output_file_constants.COST_SUMMARY_COLUMNS_ACCESSORS.COST_OF_MITIGATED_EMIS]
    )

    plot_stack_bar_chart(
        data,
        visualization_dir,
        visualization_name,
        viz_mapper,
    )
