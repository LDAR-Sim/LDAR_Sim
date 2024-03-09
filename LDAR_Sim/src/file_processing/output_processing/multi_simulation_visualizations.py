from pathlib import Path
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker, lines

from src.file_processing.output_processing import output_constants
from src.file_processing.output_processing import output_utils


def gen_estimated_vs_true_emissions_plot(out_dir: Path):
    emis_summary_info: pd.DataFrame = pd.read_csv(out_dir / output_constants.EMIS_SUMMARY_FILENAME)

    estimated_vs_true_total_emis_percent_diff = output_utils.percent_difference(
        emis_summary_info[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS],
        emis_summary_info[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_TOTAL_EMIS],
    )

    fig, ax = plt.subplots()
    sns.histplot(
        estimated_vs_true_total_emis_percent_diff,
        kde=True,
        color="b",
        element="step",
        ax=ax,
        bins=30,
    )
    fig: plt.Figure
    ax: plt.Axes
    # sns.histplot(normal_dist_samples2, kde=True, color="orange", element="step", ax=ax, bins=30)
    ax.set(xlabel="Difference between Estimated and True Emissions", ylabel="Number of Occurences")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(output_utils.percentage_formatter))
    # ax.set_title("Distribution of Variation between Estimated and True values")
    plt.axvline(0, color="black", linestyle="--")
    plt.ylim(0, 110)
    legend_elements = [
        lines.Line2D(
            [0], [0], color="blue", label="Measured Only", markerfacecolor="blue", markersize=15
        ),
        lines.Line2D(
            [0],
            [0],
            color="orange",
            label="Measured + Calculated",
            markerfacecolor="orange",
            markersize=15,
        ),
    ]
    plt.legend(handles=legend_elements)
    plt.savefig("Sample PD Fig1")
