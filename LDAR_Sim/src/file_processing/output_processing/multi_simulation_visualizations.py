import os
from pathlib import Path
from typing import Tuple
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker, lines

from file_processing.output_processing import output_constants
from file_processing.output_processing import output_utils


def gen_cross_program_summary_plots(out_dir: Path):

    summary_program_plots_directory = out_dir / output_constants.SUMMARY_PROGRAM_PLOTS_DIRECTORY

    os.makedirs(summary_program_plots_directory)

    emis_summary_info: pd.DataFrame = pd.read_csv(out_dir / output_constants.EMIS_SUMMARY_FILENAME)

    estimate_vs_true_constants = output_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS
    gen_estimated_vs_true_emissions_percent_difference_plot(
        emis_summary_info, summary_program_plots_directory, estimate_vs_true_constants
    )
    gen_estimated_vs_true_emissions_relative_difference_plot(
        emis_summary_info, summary_program_plots_directory, estimate_vs_true_constants
    )
    gen_paired_estimate_and_true_emission_distributions(
        emis_summary_info, summary_program_plots_directory, estimate_vs_true_constants
    )


def plot_hist(
    legend_elements: list,
    ax: plt.Axes,
    percent_diff_list,
    program_name: str,
    color: Tuple[float, float, float],
    bin_range: Tuple[int, int],
    x_label: str,
    y_label: str,
    legend_label: str = None,
    bin_width: float = 0,
    bins: int = 0,
):
    if bins != 0:
        sns.histplot(
            percent_diff_list,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binrange=bin_range,
            bins=bins,
        )
    elif bin_width != 0:
        sns.histplot(
            percent_diff_list,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binwidth=bin_width,
            binrange=bin_range,
        )
    else:
        sns.histplot(
            percent_diff_list,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binrange=bin_range,
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


def gen_estimated_vs_true_emissions_percent_difference_plot(
    emis_summary_info: pd.DataFrame,
    out_dir: Path,
    estimate_vs_true_constants: output_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS,
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

    program_names = emis_summary_info[
        output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
    ].unique()
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

    colors = sns.color_palette("husl", n_colors=len(program_names))

    legend_elements = []

    for i, (program_name, percent_diff_list) in enumerate(percent_diff_lists.items()):
        if save_separate_plots:
            fig_sep: plt.Figure = plt.figure()  # noqa: 481
            ax_sep: plt.Axes = plt.gca()

            plot_hist(
                legend_elements=legend_elements,
                ax=ax_sep,
                percent_diff_list=percent_diff_list,
                program_name=program_name,
                color=colors[i],
                bin_width=1.0,
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

        if combine_plots:
            plt.figure(comb_fig.number)
            plot_hist(
                legend_elements=legend_elements,
                ax=comb_ax,
                percent_diff_list=percent_diff_list,
                program_name=program_name,
                color=colors[i],
                bin_width=1.0,
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


def gen_estimated_vs_true_emissions_relative_difference_plot(
    emis_summary_info: pd.DataFrame,
    out_dir: Path,
    estimate_vs_true_constants: output_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS,
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

    program_names = emis_summary_info[
        output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
    ].unique()
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
    plot_bin_range = (-100, max(emis_summary_info["relative_diff"].max() + 10, 100))

    legend_elements = []

    for i, (program_name, relative_diff_list) in enumerate(relative_diff_lists.items()):
        if save_separate_plots:
            fig_sep: plt.Figure = plt.figure()  # noqa: 481
            ax_sep: plt.Axes = plt.gca()

            plot_hist(
                legend_elements=legend_elements,
                ax=ax_sep,
                percent_diff_list=relative_diff_list,
                program_name=program_name,
                color=colors[i],
                bin_width=1.0,
                bin_range=plot_bin_range,
                x_label="Relative Difference between Estimated and True Emissions",
                y_label="Number of Occurrences",
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

        if combine_plots:
            plt.figure(comb_fig.number)
            plot_hist(
                legend_elements=legend_elements,
                ax=comb_ax,
                percent_diff_list=relative_diff_list,
                program_name=program_name,
                color=colors[i],
                bin_width=1.0,
                bin_range=plot_bin_range,
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


def gen_paired_estimate_and_true_emission_distributions(
    emis_summary_info: pd.DataFrame,
    out_dir: Path,
    estimate_vs_true_constants: output_constants.ESTIMATE_VS_TRUE_PLOTTING_CONSTANTS,
    combine_plots: bool = False,
    save_separate_plots: bool = True,
):

    program_names = emis_summary_info[
        output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
    ].unique()
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
                percent_diff_list=paired_emis_list[0],
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
                percent_diff_list=paired_emis_list[1],
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

        if combine_plots:
            plt.figure(comb_fig.number)
            plot_hist(
                legend_elements=legend_elements,
                ax=comb_ax,
                percent_diff_list=paired_emis_list[0],
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
                percent_diff_list=paired_emis_list[1],
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
