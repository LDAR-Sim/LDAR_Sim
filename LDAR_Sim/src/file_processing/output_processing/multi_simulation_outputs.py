import os
from pathlib import Path
import numpy as np
import pandas as pd
import re
from file_processing.output_processing.output_utils import (
    TIMESERIES_COL_ACCESSORS as tca,
    EMIS_DATA_COL_ACCESSORS as eca,
)


class TS_SUMMARY_COLUMNS_ACCESSORS:
    PROG_NAME = "Program Name"
    SIM = "Simulation"
    AVG_T_DAILY_EMIS = 'Average "True" Daily Emissions (Kg Methane)'
    T_DAILY_EMIS_95 = '95th Percentile "True" Daily Emissions (Kg Methane)'
    T_DAILY_EMIS_5 = '5th Percentile "True" Daily Emissions (Kg Methane)'
    AVG_DAILY_COST = "Average Daily Cost ($)"
    DAILY_COST_95 = "95th Percentile Daily Cost ($)"
    DAILY_COST_5 = "5th Percentile Daily Cost ($)"


class EMIS_SUMMARY_COLUMNS_ACCESSORS:
    PROG_NAME = "Program Name"
    SIM = "Simulation"
    T_TOTAL_EMIS = 'Total "True" Emissions (Kg Methane)'
    AVG_T_EMIS_RATE = 'Average "True" Emissions Rate (g/s)'
    T_EMIS_RATE_95 = '95th Percentile "True" Emissions Rate (g/s)'
    T_EMIS_RATE_5 = '5th Percentile "True" Emissions Rate (g/s)'
    T_AVG_EMIS_AMOUNT = '"True" Average Emissions Amount (Kg Methane)'
    T_EMIS_AMOUNT_95 = '95th Percentile "True" Emissions Amount (Kg Methane)'
    T_EMIS_AMOUNT_5 = '5th Percentile "True" Emissions Amount (Kg Methane)'


TS_SUMMARY_COLUMNS = [
    TS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
    TS_SUMMARY_COLUMNS_ACCESSORS.SIM,
    TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_DAILY_EMIS,
    TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_95,
    TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_5,
    TS_SUMMARY_COLUMNS_ACCESSORS.AVG_DAILY_COST,
    TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_95,
    TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_5,
]

EMIS_SUMMARY_COLUMNS = [
    EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.SIM,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_EMIS_RATE,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_95,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_5,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_AVG_EMIS_AMOUNT,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_95,
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_5,
]


def get_mean_val(df: pd.DataFrame, column: str) -> float:
    return df[column].mean()


def get_sum(df: pd.DataFrame, column: str) -> float:
    return df[column].sum()


# Currently defined to compute percentiles using a median-unbiased method as described in:
# https://numpy.org/doc/stable/reference/generated/numpy.percentile.html and
# Rob J. Hyndman & Yanan Fan (1996) Sample Quantiles in Statistical
# Packages, The American Statistician, 50:4, 361-365
# As this is described as the suggested method for unknown distributions
def get_nth_percentile(df: pd.DataFrame, column: str, percentile: float) -> float:
    return np.percentile(df[column], percentile, method="median_unbiased")


TS_MAPPING_TO_SUMMARY_COLS = {
    TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_DAILY_EMIS: lambda df: get_mean_val(df, tca.EMIS),
    TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_95: lambda df: get_nth_percentile(df, tca.EMIS, 95),
    TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_5: lambda df: get_nth_percentile(df, tca.EMIS, 5),
    TS_SUMMARY_COLUMNS_ACCESSORS.AVG_DAILY_COST: lambda df: get_mean_val(df, tca.COST),
    TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_95: lambda df: get_nth_percentile(df, tca.COST, 95),
    TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_5: lambda df: get_nth_percentile(df, tca.COST, 5),
}

EMIS_MAPPING_TO_SUMMARY_COLS = {
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS: lambda df: get_sum(df, eca.T_VOL_EMIT),
    EMIS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_EMIS_RATE: lambda df: get_mean_val(df, eca.T_RATE),
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_95: lambda df: get_nth_percentile(
        df, eca.T_RATE, 95
    ),
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_5: lambda df: get_nth_percentile(df, eca.T_RATE, 5),
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_AVG_EMIS_AMOUNT: lambda df: get_mean_val(df, eca.T_VOL_EMIT),
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_95: lambda df: get_nth_percentile(
        df, eca.T_VOL_EMIT, 95
    ),
    EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_5: lambda df: get_nth_percentile(
        df, eca.T_VOL_EMIT, 5
    ),
}

TS_SUMMARY_FILENAME = "daily_summary_stats.csv"
EMIS_SUMMARY_FILENAME = "emissions_summary_stats.csv"

TS_PATTERN = re.compile(r".*timeseries\.csv$")
EMIS_PATTERN = re.compile(r".*emissions_summary\.csv$")

OUTPUTS_NAME_SIM_EXTRACTION_REGEX = re.compile(r"^(.*?)_(\d+)_.+.csv$")

OUTPUT_KEEP_STR = "kept"
OUTPUT_KEEP_REGEX = re.compile(re.escape(OUTPUT_KEEP_STR))


def gen_ts_summary(dir: Path):
    ts_summary_df = pd.DataFrame(columns=TS_SUMMARY_COLUMNS)
    with os.scandir(dir) as entries:
        for entry in entries:
            if (
                entry.is_file()
                and TS_PATTERN.match(entry.name)
                and not re.search(OUTPUT_KEEP_REGEX, entry.name)
            ):
                new_summary_row = {}
                ts_data: pd.DataFrame = pd.read_csv(entry.path)
                new_summary_row[TS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME] = (
                    OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(1)
                )
                new_summary_row[TS_SUMMARY_COLUMNS_ACCESSORS.SIM] = (
                    OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(2)
                )
                for sum_stat, calc in TS_MAPPING_TO_SUMMARY_COLS.items():
                    new_summary_row[sum_stat] = calc(ts_data)
                ts_summary_df.loc[len(ts_summary_df)] = new_summary_row
    return ts_summary_df


def gen_emissions_summary(dir: Path):
    emis_summary_df = pd.DataFrame(columns=EMIS_SUMMARY_COLUMNS)
    with os.scandir(dir) as entries:
        for entry in entries:
            if (
                entry.is_file()
                and EMIS_PATTERN.match(entry.name)
                and not re.search(OUTPUT_KEEP_REGEX, entry.name)
            ):
                new_summary_row = {}
                emis_data: pd.DataFrame = pd.read_csv(entry.path)
                new_summary_row[EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME] = (
                    OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(1)
                )
                new_summary_row[EMIS_SUMMARY_COLUMNS_ACCESSORS.SIM] = (
                    OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(2)
                )
                for sum_stat, calc in EMIS_MAPPING_TO_SUMMARY_COLS.items():
                    new_summary_row[sum_stat] = calc(emis_data)
                emis_summary_df.loc[len(emis_summary_df)] = new_summary_row
    return emis_summary_df


def get_summary_file(out_dir: Path, filename: str):
    filepath: Path = out_dir / filename
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame()


def save_summary_file(summary_file: pd.DataFrame, out_dir: Path, filename: str):
    filepath: Path = out_dir / filename
    summary_file.to_csv(filepath, index=False, mode="w")


def clear_directory(dir: Path):
    with os.scandir(dir) as entries:
        for entry in entries:
            if not re.search(OUTPUT_KEEP_REGEX, entry.name):
                os.remove(entry.path)


def mark_outputs_to_keep(dir: Path):
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file():
                old_file_path = entry.path
                new_name = OUTPUT_KEEP_STR + entry.name
                new_file_path = os.path.join(dir, new_name)
                os.rename(old_file_path, new_file_path)


def concat_output_data(out_dir: Path, clear_outputs: bool):
    leg_ts_sum: pd.DataFrame = get_summary_file(out_dir, TS_SUMMARY_FILENAME)
    leg_emis_sum: pd.DataFrame = get_summary_file(out_dir, EMIS_SUMMARY_FILENAME)
    program_dirs = [f.path for f in os.scandir(out_dir) if f.is_dir()]
    prog_ts_sum_dfs: list[pd.DataFrame] = []
    prog_emis_sum_dfs: list[pd.DataFrame] = []
    for program_dir in program_dirs:
        prog_ts_sum_dfs.append(gen_ts_summary(program_dir))
        prog_emis_sum_dfs.append(gen_emissions_summary(program_dir))
        if clear_outputs:
            clear_directory(program_dir)
        else:
            mark_outputs_to_keep(program_dir)
    if not leg_ts_sum.empty and not leg_emis_sum.empty:
        prog_ts_sum_dfs.insert(0, leg_ts_sum)
        new_ts_sum: pd.DataFrame = pd.concat(prog_ts_sum_dfs, ignore_index=True)
        prog_emis_sum_dfs.insert(0, leg_emis_sum)
        new_emis_sum: pd.DataFrame = pd.concat(prog_emis_sum_dfs, ignore_index=True)
        save_summary_file(new_ts_sum, out_dir, TS_SUMMARY_FILENAME)
        save_summary_file(new_emis_sum, out_dir, EMIS_SUMMARY_FILENAME)
    else:
        new_ts_sum: pd.DataFrame = pd.concat(prog_ts_sum_dfs, ignore_index=True)
        new_emis_sum: pd.DataFrame = pd.concat(prog_emis_sum_dfs, ignore_index=True)
        save_summary_file(new_ts_sum, out_dir, TS_SUMMARY_FILENAME)
        save_summary_file(new_emis_sum, out_dir, EMIS_SUMMARY_FILENAME)
