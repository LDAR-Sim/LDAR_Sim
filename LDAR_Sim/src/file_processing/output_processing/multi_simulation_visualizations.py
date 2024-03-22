"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        multi_simulation_visualizations.py
Purpose: Functionality for visualizations across multiple simulations.

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
from typing import Tuple, Union
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker, lines

from file_processing.output_processing import output_constants, output_utils


def gen_cross_program_summary_plots(out_dir: Path, baseline_program: str):

    print(output_constants.SUMMARRY_PLOT_GENERATION_MESSAGE)

    summary_program_plots_directory = out_dir / output_constants.SUMMARY_PROGRAM_PLOTS_DIRECTORY

    os.makedirs(summary_program_plots_directory)

    emis_summary_info: pd.DataFrame = pd.read_csv(out_dir / output_constants.EMIS_SUMMARY_FILENAME)

    estimate_vs_true_constants = output_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
    gen_estimated_vs_true_emissions_percent_difference_plot(
        emis_summary_info,
        summary_program_plots_directory,
        estimate_vs_true_constants,
        baseline_program,
    )
    gen_estimated_vs_true_emissions_relative_difference_plot(
        emis_summary_info,
        summary_program_plots_directory,
        estimate_vs_true_constants,
        baseline_program,
    )
    gen_paired_estimate_and_true_emission_distributions(
        emis_summary_info,
        summary_program_plots_directory,
        estimate_vs_true_constants,
        baseline_program,
    )
    # Close all plots
    plt.close("all")


def plot_hist(
    legend_elements: list,
    ax: plt.Axes,
    x_values: list,
    program_name: str,
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
    if bin_width != 0:
        sns.histplot(
            x_values,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binwidth=bin_width,
            binrange=bin_range,
        )
    else:
        sns.histplot(
            x_values,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binrange=bin_range,
            bins=bins,
        )

    legend_elements.append(
        lines.Line2D(
            [0],
            [0],
            color=color,
            label=legend_label if legend_label else program_name,
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


def gen_estimated_vs_true_emissions_percent_difference_plot(
    emis_summary_info: pd.DataFrame,
    out_dir: Path,
    estimate_vs_true_constants: output_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS,
    baseline_program: str,
    combine_plots: bool = False,
    save_separate_plots: bool = True,
):

    emis_summary_info["percent_diff"] = emis_summary_info.apply(
        lambda row: output_utils.percent_difference(
            row[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_TOTAL_EMIS],
            row[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS],
        ),
        axis=1,
    )

    program_names = [
        program_name
        for program_name in emis_summary_info[
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
        ].unique()
        if program_name != baseline_program
    ]
    percent_diff_lists = {}

    for program_name in program_names:
        percent_diff_list = emis_summary_info.loc[
            emis_summary_info[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
            == program_name,
            "percent_diff",
        ].tolist()
        percent_diff_lists[program_name] = percent_diff_list

    if combine_plots:
        comb_fig: plt.Figure = plt.figure()
        comb_ax: plt.Axes = plt.gca()

    # TODO for all plots - account for colorblind palette
    colors = sns.color_palette("husl", n_colors=len(program_names))

    legend_elements = []

    for i, (program_name, percent_diff_list) in enumerate(percent_diff_lists.items()):
        if save_separate_plots:
            fig_sep: plt.Figure = plt.figure()  # noqa: 481
            ax_sep: plt.Axes = plt.gca()

            plot_hist(
                legend_elements=legend_elements,
                ax=ax_sep,
                x_values=percent_diff_list,
                program_name=program_name,
                color=colors[i],
                bin_width=estimate_vs_true_constants.HISTOGRAM_BIN_WIDTH,
                bin_range=(0, 200),
                x_label='Percent Difference between "Estimated" and "True" Emissions',
                y_label="Number of Occurrences",
            )

            ax_sep.xaxis.set_major_formatter(
                ticker.FuncFormatter(output_utils.percentage_formatter)
            )
            plt.legend(handles=[legend_elements[i]])
            save_path = out_dir / " ".join(
                [program_name, output_constants.TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT]
            )
            plt.savefig(save_path)
            plt.close(fig_sep)

        if combine_plots:
            plt.figure(comb_fig.number)
            plot_hist(
                legend_elements=legend_elements,
                ax=comb_ax,
                x_values=percent_diff_list,
                program_name=program_name,
                color=colors[i],
                bin_width=estimate_vs_true_constants.HISTOGRAM_BIN_WIDTH,
                bin_range=(0, 200),
            )

    if combine_plots:
        comb_ax.set(
            xlabel='Percent Difference between "Estimated" and "True" Emissions',
            ylabel="Number of Occurrences",
        )
        comb_ax.xaxis.set_major_formatter(ticker.FuncFormatter(output_utils.percentage_formatter))
        plt.legend(handles=legend_elements)
        save_path = out_dir / output_constants.TRUE_VS_ESTIMATED_PERCENT_DIFF_PLOT
        plt.savefig(save_path)
        plt.close(comb_fig)


def gen_estimated_vs_true_emissions_relative_difference_plot(
    emis_summary_info: pd.DataFrame,
    out_dir: Path,
    estimate_vs_true_constants: output_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS,
    baseline_program: str,
    combine_plots: bool = False,
    save_separate_plots: bool = True,
):

    emis_summary_info["relative_diff"] = emis_summary_info.apply(
        lambda row: output_utils.relative_difference(
            row[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_TOTAL_EMIS],
            row[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS],
        ),
        axis=1,
    )

    program_names = [
        program_name
        for program_name in emis_summary_info[
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
        ].unique()
        if program_name != baseline_program
    ]
    relative_diff_lists = {}

    for program_name in program_names:
        relative_diff_list = emis_summary_info.loc[
            emis_summary_info[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
            == program_name,
            "relative_diff",
        ].tolist()
        relative_diff_lists[program_name] = relative_diff_list

    if combine_plots:
        comb_fig: plt.Figure = plt.figure()
        comb_ax: plt.Axes = plt.gca()

    colors = sns.color_palette("husl", n_colors=len(program_names))
    plot_bin_range: Tuple[float, float] = (
        -100,
        max(emis_summary_info["relative_diff"].max() + 10, 100),
    )

    legend_elements = []

    for i, (program_name, relative_diff_list) in enumerate(relative_diff_lists.items()):
        if save_separate_plots:
            fig_sep: plt.Figure = plt.figure()  # noqa: 481
            ax_sep: plt.Axes = plt.gca()

            plot_hist(
                legend_elements=legend_elements,
                ax=ax_sep,
                x_values=relative_diff_list,
                program_name=program_name,
                color=colors[i],
                bin_width=estimate_vs_true_constants.HISTOGRAM_BIN_WIDTH,
                bin_range=plot_bin_range,
                x_label="Relative Difference between Estimated and True Emissions",
                y_label="Number of Occurrences",
                x_locator=ticker.MaxNLocator(nbins="auto", prune=None),
            )

            ax_sep.xaxis.set_major_formatter(
                ticker.FuncFormatter(output_utils.percentage_formatter)
            )
            plt.axvline(0, color="black", linestyle="--")
            plt.legend(handles=[legend_elements[i]])
            save_path = out_dir / " ".join(
                [program_name, output_constants.TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT]
            )
            plt.savefig(save_path)
            plt.close(fig_sep)

        if combine_plots:
            plt.figure(comb_fig.number)
            plot_hist(
                legend_elements=legend_elements,
                ax=comb_ax,
                x_values=relative_diff_list,
                program_name=program_name,
                color=colors[i],
                bin_width=estimate_vs_true_constants.HISTOGRAM_BIN_WIDTH,
                bin_range=plot_bin_range,
                x_locator=ticker.MaxNLocator(nbins="auto", prune=None),
            )

    if combine_plots:
        comb_ax.set(
            xlabel="Relative Difference between Estimated and True Emissions",
            ylabel="Number of Occurrences",
        )
        comb_ax.xaxis.set_major_formatter(ticker.FuncFormatter(output_utils.percentage_formatter))
        plt.axvline(0, color="black", linestyle="--")
        plt.legend(handles=legend_elements)
        save_path = out_dir / output_constants.TRUE_VS_ESTIMATED_RELATIVE_DIFF_PLOT
        plt.savefig(save_path)
        plt.close(comb_fig)


def gen_paired_estimate_and_true_emission_distributions(
    emis_summary_info: pd.DataFrame,
    out_dir: Path,
    estimate_vs_true_constants: output_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS,
    baseline_program: str,
    combine_plots: bool = False,
    save_separate_plots: bool = True,
):

    program_names = [
        program_name
        for program_name in emis_summary_info[
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
        ].unique()
        if program_name != baseline_program
    ]
    paired_emissions_lists = {}

    for program_name in program_names:
        true_emis_list = emis_summary_info.loc[
            emis_summary_info[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
            == program_name,
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS,
        ].tolist()
        est_emis_list = emis_summary_info.loc[
            emis_summary_info[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
            == program_name,
            output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_TOTAL_EMIS,
        ].tolist()
        paired_emissions_lists[program_name] = (true_emis_list, est_emis_list)

    if combine_plots:
        comb_fig: plt.Figure = plt.figure()
        comb_ax: plt.Axes = plt.gca()

    colors = sns.color_palette("husl", n_colors=len(program_names))
    dark_pallete = [output_utils.luminance_shift(color, lighten=False) for color in colors]
    light_pallete = [output_utils.luminance_shift(color, lighten=True) for color in colors]
    plot_bin_range = (
        0,
        max(
            emis_summary_info[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS].max(),
            emis_summary_info[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_TOTAL_EMIS].max(),
        ),
    )

    legend_elements = []

    for i, (program_name, paired_emis_list) in enumerate(paired_emissions_lists.items()):
        if save_separate_plots:
            fig_sep: plt.Figure = plt.figure()  # noqa: 481
            ax_sep: plt.Axes = plt.gca()

            plot_hist(
                legend_elements=legend_elements,
                ax=ax_sep,
                x_values=paired_emis_list[0],
                program_name=program_name,
                color=dark_pallete[i],
                bin_range=plot_bin_range,
                x_label="emissions (Kg Methane)",
                y_label="Number of Occurrences",
                bins=30,
                legend_label=" ".join(
                    [program_name, estimate_vs_true_constants.TRUE_EMISSIONS_SUFFIX]
                ),
            )

            plot_hist(
                legend_elements=legend_elements,
                ax=ax_sep,
                x_values=paired_emis_list[1],
                program_name=program_name,
                color=light_pallete[i],
                bin_range=plot_bin_range,
                x_label="Emissions (Kg Methane)",
                y_label="Number of Occurrences",
                bins=30,
                legend_label=" ".join(
                    [program_name, estimate_vs_true_constants.ESTIMATED_EMISSIONS_SUFFIX]
                ),
            )

            plt.legend(handles=legend_elements[(i * 2) : (i * 2 + 2)])  # noqa: 481
            save_path = out_dir / " ".join(
                [
                    program_name,
                    output_constants.TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT,
                ]
            )
            plt.savefig(save_path)
            plt.close(fig_sep)

        if combine_plots:
            plt.figure(comb_fig.number)
            plot_hist(
                legend_elements=legend_elements,
                ax=comb_ax,
                x_values=paired_emis_list[0],
                program_name=program_name,
                color=dark_pallete[i],
                bin_range=plot_bin_range,
                bins=30,
                legend_label=" ".join(
                    [program_name, estimate_vs_true_constants.TRUE_EMISSIONS_SUFFIX]
                ),
            )

            plot_hist(
                legend_elements=legend_elements,
                ax=comb_ax,
                x_values=paired_emis_list[1],
                program_name=program_name,
                color=light_pallete[i],
                bin_range=plot_bin_range,
                bins=30,
                legend_label=" ".join(
                    [program_name, estimate_vs_true_constants.ESTIMATED_EMISSIONS_SUFFIX]
                ),
            )

    if combine_plots:
        comb_ax.set(
            xlabel="emissions (Kg Methane)",
            ylabel="Number of Occurrences",
        )
        plt.legend(handles=legend_elements)
        save_path = out_dir / output_constants.TRUE_AND_ESTIMATED_PAIRED_EMISSIONS_DISTRIBUTION_PLOT
        plt.savefig(save_path)
        plt.close(comb_fig)
