"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        summary_output_helpers.py
Purpose: Contains helper functions for summarizing output data.

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
import numpy as np
import pandas as pd
import os
import re
from constants import file_processing_const


def get_mean_val(df: pd.DataFrame, column: str) -> float:
    return df[column].mean()


def get_sum(df: pd.DataFrame, column: str) -> float:
    return df[column].sum()


# TODO add this comment to the relevant User Manual Section
# Currently defined to compute percentiles using a median-unbiased method as described in:
# https://numpy.org/doc/stable/reference/generated/numpy.percentile.html and
# Rob J. Hyndman & Yanan Fan (1996) Sample Quantiles in Statistical
# Packages, The American Statistician, 50:4, 361-365
# As this is described as the suggested method for unknown distributions
def get_nth_percentile(df: pd.DataFrame, column: str, percentile: float) -> float:
    return np.percentile(df[column], percentile, method="median_unbiased")


def get_yearly_value_for_multi_day_stat(
    df: pd.DataFrame, column: str, year: int, start_date_col: str, end_date_col: str
) -> float:
    yearly_sum = 0

    if df.empty:
        return yearly_sum

    df[start_date_col] = df[start_date_col].astype("datetime64[ns]")
    df[end_date_col] = df[end_date_col].astype("datetime64[ns]")

    filtered_df = df.loc[
        (df[start_date_col].dt.year <= year)
        & ((df[end_date_col].dt.year >= year) | (df[end_date_col].isna()))
    ]

    for index, row in filtered_df.iterrows():
        start_date: pd.Timestamp = row[start_date_col]
        start_year: int = start_date.year
        end_date: pd.Timestamp = row[end_date_col]
        if end_date is pd.NaT:
            end_date = df[end_date_col].max()
            end_year: int = end_date.year
            end_date = pd.Timestamp("-".join([str(end_year), "12", "31"]))
        else:
            end_year: int = end_date.year
        value: np.number = row[column]

        start_of_current_year: pd.Timestamp = pd.Timestamp("-".join([str(year), "01", "01"]))
        end_of_current_year: pd.Timestamp = pd.Timestamp("-".join([str(year), "12", "31"]))

        if start_year == year and end_year == year:
            total_time: int = 1
            time_in_year: int = 1
        elif start_year == year:
            total_time: int = (end_date - start_date).days + 1
            time_in_year: int = (end_of_current_year - start_date).days + 1
        elif end_year == year:
            total_time: int = (end_date - start_date).days + 1
            time_in_year: int = (end_date - start_of_current_year).days + 1
        else:
            total_time: int = (end_date - start_date).days + 1
            time_in_year: int = 365

        value *= time_in_year / total_time
        yearly_sum += value

    return yearly_sum


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
            if not re.search(
                file_processing_const.Multi_Sim_Output_Const.OUTPUT_KEEP_REGEX, entry.name
            ):
                os.remove(entry.path)


def mark_outputs_to_keep(dir: Path):
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file():
                old_file_path = entry.path
                new_name = file_processing_const.Multi_Sim_Output_Const.OUTPUT_KEEP_STR + entry.name
                new_file_path = os.path.join(dir, new_name)
                os.rename(old_file_path, new_file_path)
