"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        multi_simulation_outputs
Purpose: Functionality for outputs across multiple simulations.

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
import numpy as np
import pandas as pd
import re
from file_processing.output_processing import output_constants


def get_mean_val(df: pd.DataFrame, column: str) -> float:
    return df[column].mean()


def get_sum(df: pd.DataFrame, column: str) -> float:
    return df[column].sum()


def assign_part_sum_columns(df: pd.DataFrame, column_name: str, base_column_name: str):
    # Extracting distinct years from the 'Date Began' column
    distinct_years = pd.to_datetime(
        df[output_constants.EMIS_DATA_COL_ACCESSORS.DATE_BEG]
    ).dt.year.unique()
    result = {}
    for year in distinct_years:
        year_df = df[
            pd.to_datetime(df[output_constants.EMIS_DATA_COL_ACCESSORS.DATE_BEG]).dt.year == year
        ]
        ann_sum = get_sum(year_df, column_name)
        year_column_name = base_column_name.format(year)
        result[year_column_name] = ann_sum
    return result


# TODO add this comment to the relevant User Manual Section
# Currently defined to compute percentiles using a median-unbiased method as described in:
# https://numpy.org/doc/stable/reference/generated/numpy.percentile.html and
# Rob J. Hyndman & Yanan Fan (1996) Sample Quantiles in Statistical
# Packages, The American Statistician, 50:4, 361-365
# As this is described as the suggested method for unknown distributions
def get_nth_percentile(df: pd.DataFrame, column: str, percentile: float) -> float:
    return np.percentile(df[column], percentile, method="median_unbiased")


TS_MAPPING_TO_SUMMARY_COLS = {
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_DAILY_EMIS: lambda df: (
        get_mean_val(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_MIT_DAILY_EMIS: lambda df: (
        get_mean_val(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS_MIT)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_NON_MIT_DAILY_EMIS: lambda df: (
        get_mean_val(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS_NON_MIT)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_95: lambda df: (
        get_nth_percentile(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS, 95)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_MIT_DAILY_EMIS_95: lambda df: (
        get_nth_percentile(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS_MIT, 95)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_NON_MIT_DAILY_EMIS_95: lambda df: (
        get_nth_percentile(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS_NON_MIT, 95)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_DAILY_EMIS_5: lambda df: (
        get_nth_percentile(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS, 5)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_MIT_DAILT_EMIS_5: lambda df: (
        get_nth_percentile(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS_MIT, 5)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.T_NON_MIT_DAILY_EMIS_5: lambda df: (
        get_nth_percentile(df, output_constants.TIMESERIES_COL_ACCESSORS.EMIS_NON_MIT, 5)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.AVG_DAILY_COST: lambda df: (
        get_mean_val(df, output_constants.TIMESERIES_COL_ACCESSORS.COST)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_95: lambda df: (
        get_nth_percentile(df, output_constants.TIMESERIES_COL_ACCESSORS.COST, 95)
    ),
    output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.DAILY_COST_5: lambda df: (
        get_nth_percentile(df, output_constants.TIMESERIES_COL_ACCESSORS.COST, 5)
    ),
}

EMIS_MAPPING_TO_SUMMARY_COLS = {
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_EMIS: lambda df: get_sum(
        df, output_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_TOTAL_EMIS: lambda df: get_sum(
        df, output_constants.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_MIT_EMIS: lambda df: get_sum(
        df.loc[df[output_constants.EMIS_DATA_COL_ACCESSORS.REPAIRABLE]],
        output_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_TOTAL_NON_MIT_EMIS: lambda df: get_sum(
        df.loc[~df[output_constants.EMIS_DATA_COL_ACCESSORS.REPAIRABLE]],
        output_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.AVG_T_EMIS_RATE: lambda df: get_mean_val(
        df, output_constants.EMIS_DATA_COL_ACCESSORS.T_RATE
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_95: lambda df: get_nth_percentile(
        df, output_constants.EMIS_DATA_COL_ACCESSORS.T_RATE, 95
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_RATE_5: lambda df: get_nth_percentile(
        df, output_constants.EMIS_DATA_COL_ACCESSORS.T_RATE, 5
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_AVG_EMIS_AMOUNT: lambda df: get_mean_val(
        df, output_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_95: lambda df: get_nth_percentile(
        df, output_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT, 95
    ),
    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_EMIS_AMOUNT_5: lambda df: get_nth_percentile(
        df, output_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT, 5
    ),
}

TS_PATTERN = re.compile(r".*timeseries\.csv$")
EMIS_PATTERN = re.compile(r".*emissions_summary\.csv$")
EST_PATTERN = re.compile(r".*estimated_emissions\.csv$")

OUTPUTS_NAME_SIM_EXTRACTION_REGEX = re.compile(r"^(.*?)_(\d+)_.+.csv$")

OUTPUT_KEEP_STR = "kept"
OUTPUT_KEEP_REGEX = re.compile(re.escape(OUTPUT_KEEP_STR))


def gen_emis_estimate_summary(dir: Path):
    emis_estimate_summary_df = pd.DataFrame(
        columns=output_constants.EMIS_ESTIMATION_SUMMARY_COLUMNS
    )
    emis_summary_df = pd.DataFrame(columns=output_constants.EMIS_SIMPLE_SUMMARY_COLUMNS)
    with os.scandir(dir) as entries:
        for entry in entries:
            if (
                entry.is_file()
                and EST_PATTERN.match(entry.name)
                and not re.search(OUTPUT_KEEP_REGEX, entry.name)
            ):
                est_emis_data: pd.DataFrame = pd.read_csv(entry.path)
                prog_name = OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(1)
                sim = OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(2)

                for year in est_emis_data["year"].unique():
                    new_summary_row = {}

                    new_summary_row[
                        output_constants.EMIS_ESTIMATION_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
                    ] = prog_name
                    new_summary_row[
                        output_constants.EMIS_ESTIMATION_SUMMARY_COLUMNS_ACCESSORS.SIM
                    ] = sim
                    new_summary_row[
                        output_constants.EMIS_ESTIMATION_SUMMARY_COLUMNS_ACCESSORS.YEAR
                    ] = year
                    yearly_emissions = est_emis_data.loc[
                        est_emis_data["year"] == year, "volume_emitted"
                    ].sum()
                    new_summary_row[
                        output_constants.EMIS_ESTIMATION_SUMMARY_COLUMNS_ACCESSORS.ANNUAL_EMISSIONS
                    ] = yearly_emissions
                    emis_estimate_summary_df.loc[len(emis_estimate_summary_df)] = new_summary_row
            elif (
                entry.is_file()
                and EMIS_PATTERN.match(entry.name)
                and not re.search(OUTPUT_KEEP_REGEX, entry.name)
            ):
                emis_data: pd.DataFrame = pd.read_csv(entry.path)
                prog_name = OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(1)
                sim = OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(2)
                distinct_years = pd.to_datetime(
                    emis_data[output_constants.EMIS_DATA_COL_ACCESSORS.DATE_BEG]
                ).dt.year.unique()
                int_data = pd.DataFrame(
                    columns=[
                        "Emissions ID",
                        "Date Began",
                        "Days Active",
                        '"True" Rate (g/s)',
                        "volume emitted",
                        "year",
                    ]
                )
                emis_data["Date Began"] = pd.to_datetime(emis_data["Date Began"])
                for _, row in emis_data.iterrows():
                    new_intermediate_row = {}
                    new_intermediate_row["Emissions ID"] = row["Emissions ID"]
                    new_intermediate_row["Date Began"] = row["Date Began"]
                    new_intermediate_row["Days Active"] = row["Days Active"]
                    new_intermediate_row['"True" Rate (g/s)'] = row['"True" Rate (g/s)']

                    if (
                        (row["Date Began"]) + pd.to_timedelta(row["Days Active"], unit="D")
                    ).year == (row["Date Began"]).year:
                        # If the emission is active for one specific year
                        new_intermediate_row["volume emitted"] = (
                            row['"True" Rate (g/s)'] * row["Days Active"] * 24 * 3600
                        ) / 1000
                        new_intermediate_row["year"] = row["Date Began"].year
                        int_data.loc[len(int_data)] = new_intermediate_row
                    else:
                        # Emission is active for more than 1 year
                        # Calculate the volume emitted for the first year
                        days_in_first_year = (
                            row["Date Began"] + pd.offsets.YearEnd()
                        ).dayofyear - row["Date Began"].dayofyear
                        new_intermediate_row["volume emitted"] = (
                            row['"True" Rate (g/s)'] * days_in_first_year * 24 * 3600
                        ) / 1000
                        year = row["Date Began"].year
                        new_intermediate_row["year"] = year
                        int_data.loc[len(int_data)] = new_intermediate_row
                        # Calculate the volume emitted for the subsequent years
                        days_remaining = row["Days Active"] - days_in_first_year
                        while days_remaining > 0:
                            year += 1
                            days_in_year = days_remaining
                            if days_remaining > 365:
                                days_in_year = 365
                            new_intermediate_row["volume emitted"] = (
                                row['"True" Rate (g/s)'] * days_in_year * 24 * 3600
                            ) / 1000
                            new_intermediate_row["year"] = year
                            int_data.loc[len(int_data)] = new_intermediate_row
                            days_remaining -= days_in_year

                for year in distinct_years:
                    new_summary_row = {}

                    new_summary_row[
                        output_constants.EMIS_SIMPLE_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
                    ] = prog_name
                    new_summary_row[output_constants.EMIS_SIMPLE_SUMMARY_COLUMNS_ACCESSORS.SIM] = (
                        sim
                    )
                    new_summary_row[output_constants.EMIS_SIMPLE_SUMMARY_COLUMNS_ACCESSORS.YEAR] = (
                        year
                    )
                    yearly_emissions = int_data.loc[
                        int_data["year"] == year, "volume emitted"
                    ].sum()
                    new_summary_row[
                        output_constants.EMIS_SIMPLE_SUMMARY_COLUMNS_ACCESSORS.ANNUAL_EMISSIONS
                    ] = yearly_emissions

                    emis_summary_df.loc[len(emis_summary_df)] = new_summary_row

    merged = pd.merge(
        emis_estimate_summary_df,
        emis_summary_df,
        on=[
            output_constants.EMIS_SIMPLE_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME,
            output_constants.EMIS_SIMPLE_SUMMARY_COLUMNS_ACCESSORS.SIM,
            output_constants.EMIS_SIMPLE_SUMMARY_COLUMNS_ACCESSORS.YEAR,
        ],
    )
    return merged


def gen_ts_summary(dir: Path):
    ts_summary_df = pd.DataFrame(columns=output_constants.TS_SUMMARY_COLUMNS)
    with os.scandir(dir) as entries:
        for entry in entries:
            if (
                entry.is_file()
                and TS_PATTERN.match(entry.name)
                and not re.search(OUTPUT_KEEP_REGEX, entry.name)
            ):
                new_summary_row = {}
                ts_data: pd.DataFrame = pd.read_csv(entry.path)
                new_summary_row[output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME] = (
                    OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(1)
                )
                new_summary_row[output_constants.TS_SUMMARY_COLUMNS_ACCESSORS.SIM] = (
                    OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(2)
                )
                for sum_stat, calc in TS_MAPPING_TO_SUMMARY_COLS.items():
                    new_summary_row[sum_stat] = calc(ts_data)
                ts_summary_df.loc[len(ts_summary_df)] = new_summary_row
    return ts_summary_df


def gen_emissions_summary(dir: Path):
    emis_summary_df = pd.DataFrame(columns=output_constants.EMIS_SUMMARY_COLUMNS)
    add_annual_columns = False
    with os.scandir(dir) as entries:
        for entry in entries:
            if (
                entry.is_file()
                and EMIS_PATTERN.match(entry.name)
                and not re.search(OUTPUT_KEEP_REGEX, entry.name)
            ):
                new_summary_row = {}
                emis_data: pd.DataFrame = pd.read_csv(entry.path)
                new_summary_row[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME] = (
                    OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(1)
                )
                new_summary_row[output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.SIM] = (
                    OUTPUTS_NAME_SIM_EXTRACTION_REGEX.match(entry.name).group(2)
                )
                for sum_stat, calc in EMIS_MAPPING_TO_SUMMARY_COLS.items():
                    new_summary_row[sum_stat] = calc(emis_data)
                true_annuals = assign_part_sum_columns(
                    emis_data,
                    output_constants.EMIS_DATA_COL_ACCESSORS.T_VOL_EMIT,
                    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS,
                )
                estimated_annuals = assign_part_sum_columns(
                    emis_data,
                    output_constants.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT,
                    output_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS,
                )
                new_summary_row.update(true_annuals)
                new_summary_row.update(estimated_annuals)
                if not add_annual_columns:
                    # Add empty columns to the DataFrame based on the keys in true_annuals
                    for column_name in sorted(true_annuals.keys()):
                        emis_summary_df[column_name] = None
                    for column_name in sorted(estimated_annuals.keys()):
                        emis_summary_df[column_name] = None
                    add_annual_columns = True
                emis_summary_df.loc[len(emis_summary_df)] = new_summary_row
    return emis_summary_df


def get_summary_file(out_dir: Path, filename: str):
    filepath: Path = out_dir / filename
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return pd.read_csv(f)
    else:
        return pd.DataFrame()


def save_summary_file(summary_file: pd.DataFrame, out_dir: Path, filename: str):
    filepath: Path = out_dir / filename
    with open(filepath, "w", newline="") as f:
        summary_file.to_csv(f, index=False)


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
    leg_ts_sum: pd.DataFrame = get_summary_file(out_dir, output_constants.TS_SUMMARY_FILENAME)
    leg_emis_sum: pd.DataFrame = get_summary_file(out_dir, output_constants.EMIS_SUMMARY_FILENAME)
    leg_emis_estimate: pd.DataFrame = get_summary_file(
        out_dir, output_constants.EMIS_ESTIMATION_SUMMARY_FILENAME
    )
    program_dirs = [f.path for f in os.scandir(out_dir) if f.is_dir()]
    prog_ts_sum_dfs: list[pd.DataFrame] = []
    prog_emis_sum_dfs: list[pd.DataFrame] = []
    prog_emis_estimate_dfs: list[pd.DataFrame] = []
    for program_dir in program_dirs:
        prog_ts_sum_dfs.append(gen_ts_summary(program_dir))
        prog_emis_sum_dfs.append(gen_emissions_summary(program_dir))
        prog_emis_estimate_dfs.append(gen_emis_estimate_summary(program_dir))
        if clear_outputs:
            clear_directory(program_dir)
        else:
            mark_outputs_to_keep(program_dir)
    if not leg_ts_sum.empty and not leg_emis_sum.empty:
        prog_ts_sum_dfs.insert(0, leg_ts_sum)
        new_ts_sum: pd.DataFrame = pd.concat(prog_ts_sum_dfs, ignore_index=True)
        prog_emis_sum_dfs.insert(0, leg_emis_sum)
        new_emis_sum: pd.DataFrame = pd.concat(prog_emis_sum_dfs, ignore_index=True)
        prog_emis_estimate_dfs.insert(0, leg_emis_estimate)
        new_emis_estimate: pd.DataFrame = pd.concat(prog_emis_estimate_dfs, ignore_index=True)
        save_summary_file(new_ts_sum, out_dir, output_constants.TS_SUMMARY_FILENAME)
        save_summary_file(new_emis_sum, out_dir, output_constants.EMIS_SUMMARY_FILENAME)
        save_summary_file(
            new_emis_estimate, out_dir, output_constants.EMIS_ESTIMATION_SUMMARY_FILENAME
        )
    else:
        new_ts_sum: pd.DataFrame = pd.concat(prog_ts_sum_dfs, ignore_index=True)
        new_emis_sum: pd.DataFrame = pd.concat(prog_emis_sum_dfs, ignore_index=True)
        new_emis_estimate: pd.DataFrame = pd.concat(prog_emis_estimate_dfs, ignore_index=True)
        save_summary_file(new_ts_sum, out_dir, output_constants.TS_SUMMARY_FILENAME)
        save_summary_file(new_emis_sum, out_dir, output_constants.EMIS_SUMMARY_FILENAME)
        save_summary_file(
            new_emis_estimate, out_dir, output_constants.EMIS_ESTIMATION_SUMMARY_FILENAME
        )
