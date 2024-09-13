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
from constants import file_processing_const, output_file_constants as ofc


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
    """
    Calculates the part of a value that can be attributed to the current year, given start
    and end dates, assuming that the provided value
    is unchanging and the entire year should be considered.
    EI: For the year 2022, all values are considered to last until the end of the year 2022
    if no end is provided. There is no ability to calculate the value for a partial year.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing the data.
        column (str): The name of the column containing the value to be calculated.
        year (int): The year for which the calculation is performed.
        start_date_col (str): The name of the column containing the start dates.
        end_date_col (str): The name of the column containing the end dates.

    Returns:
        float: The calculated yearly value.

    """
    # Initialize the yearly sum
    yearly_sum = 0

    # If the DataFrame is empty, return 0, there is no data to process
    if df.empty:
        return yearly_sum

    # Convert the start and end dates to datetime objects
    df[start_date_col] = df[start_date_col].astype("datetime64[ns]")
    df[end_date_col] = df[end_date_col].astype("datetime64[ns]")

    # Filter the DataFrame to only include rows that are relevant for the current year
    filtered_df = df.loc[
        (df[start_date_col].dt.year <= year)
        & ((df[end_date_col].dt.year >= year) | (df[end_date_col].isna()))
    ]

    # Iterate over the filtered DataFrame and calculate the yearly sum
    for index, row in filtered_df.iterrows():
        # Extract the start and end dates from the row
        start_date: pd.Timestamp = row[start_date_col]
        start_year: int = start_date.year
        end_date: pd.Timestamp = row[end_date_col]
        # If the end date is not provided, assume it is the end of the year
        if end_date is pd.NaT:
            end_date = df[end_date_col].max()
            end_year: int = end_date.year
            if end_date is pd.NaT:
                end_year: int = year

            end_date = pd.Timestamp("-".join([str(end_year), "12", "31"]))
        else:
            end_year: int = end_date.year
        # Extract the value from the row
        value: np.number = row[column]

        # Initialize timestamps for the start and end of the current year
        start_of_current_year: pd.Timestamp = pd.Timestamp("-".join([str(year), "01", "01"]))
        end_of_current_year: pd.Timestamp = pd.Timestamp("-".join([str(year), "12", "31"]))

        # Calculate the total time the value is active and the time it is active in the current year
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

        # Multiply the value by the ratio of the time active
        # in the current year to the total time active
        value *= time_in_year / total_time
        # Add the value to the yearly sum
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
    filepath: Path = (out_dir / filename).with_suffix(".csv")
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
    rename_operations: list[tuple[str, str]] = []
    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.is_file():
                if re.search(
                    file_processing_const.Multi_Sim_Output_Const.OUTPUT_KEEP_REGEX, entry.name
                ):
                    continue
                old_file_path = entry.path
                new_name = file_processing_const.Multi_Sim_Output_Const.OUTPUT_KEEP_STR + entry.name
                new_file_path = os.path.join(dir, new_name)
                rename_operations.append((old_file_path, new_file_path))

    for old_file_path, new_file_path in rename_operations:
        os.rename(old_file_path, new_file_path)


def get_non_baseline_prog_names(programs, baseline_program) -> list:
    return [program_name for program_name in programs if program_name != baseline_program]


def get_annual_emissions_at_all_sites_with_extrapolation(
    estimated_emissions_data: pd.DataFrame, year: int
) -> float:
    """
    Calculate the total annual emissions at all sites with extrapolation for sites that were not
    measured.

    Parameters:
        estimated_emissions_data (pd.DataFrame): Data from an estimated emissions csv file.
        year (int): The year for which the emissions are to be calculated.

    Returns:
        float: The total annual emissions at all sites with extrapolation for sites that were not
        measured for the given year.
    """
    # Calculate the annual emissions for each site
    annual_emissions: pd.Series = estimated_emissions_data.groupby(
        ofc.EMIS_DATA_COL_ACCESSORS.SITE_ID
    ).apply(
        lambda x: get_yearly_value_for_multi_day_stat(
            x,
            ofc.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT,
            year,
            ofc.EMIS_DATA_COL_ACCESSORS.START_DATE,
            ofc.EMIS_DATA_COL_ACCESSORS.END_DATE,
        )
    )

    # Convert the annual emissions to a DataFrame and join it with site type
    # and measured information
    annual_emissions_and_site_type: pd.DataFrame = (
        pair_site_annual_emissions_with_site_type_and_measurement_info(
            annual_emissions, estimated_emissions_data
        )
    )

    # Filter out sites that were not measured
    annual_emissions_and_site_type_measured = annual_emissions_and_site_type[
        annual_emissions_and_site_type[ofc.EMIS_DATA_COL_ACCESSORS.SITE_MEASURED]
    ]

    # Group the measured sites by site type and average the annual emissions
    annual_emissions_site_type_averages: pd.Series = (
        annual_emissions_and_site_type_measured.groupby(
            annual_emissions_and_site_type_measured[ofc.EMIS_DATA_COL_ACCESSORS.SITE_TYPE]
        ).apply(lambda x: x[ofc.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT].mean())
    )

    # Calculate the average of all measured sites
    average_emissions_all_sites: float = annual_emissions_and_site_type_measured[
        ofc.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT
    ].mean()

    # Extrapolate the average emissions to sites that were not measured based on site type
    # If there are no measured sites of a given type, use the average of all measured sites
    # as the extrapolated value

    # Map average emissions to site IDs based on site type (where possible)
    # This will be used as the list of replacement values for sites that were not measured
    average_emissions_map: list[float] = [
        annual_emissions_site_type_averages.get(site_type, average_emissions_all_sites)
        for site_type in annual_emissions_and_site_type[ofc.EMIS_DATA_COL_ACCESSORS.SITE_TYPE]
    ]

    # Replace the annual emissions for sites that were not measured with the extrapolated values
    extrapolated_annual_emissions: pd.Series = annual_emissions.where(
        annual_emissions.index.isin(
            annual_emissions_and_site_type_measured[ofc.EMIS_DATA_COL_ACCESSORS.SITE_ID]
        ),
        average_emissions_map,
    )

    return extrapolated_annual_emissions.sum()


def pair_site_annual_emissions_with_site_type_and_measurement_info(
    site_annual_emissions: pd.Series, estimated_emissions_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Pair the annual emissions with the site type and measured information from the
    estimated emissions data.

    Parameters:
        site_annual_emissions (pd.Series): The annual emissions at each site.
        estimated_emissions_data (pd.DataFrame): Data from an estimated emissions csv file.

    Returns:
        pd.DataFrame: A DataFrame containing the annual emissions, site type, and
        whether the site was measured.
    """
    # Convert the annual emissions to a DataFrame
    annual_emissions_df: pd.DataFrame = (
        site_annual_emissions.to_frame()
        .reset_index()
        .rename(columns={0: ofc.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT})
    )
    # Extract site type and measured information from the estimated emissions data
    site_type_info: pd.DataFrame = estimated_emissions_data[
        [
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_ID,
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_TYPE,
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_MEASURED,
        ]
    ].drop_duplicates()
    # Merge the annual emissions with the site type and measured information
    annual_emissions_and_site_type: pd.DataFrame = annual_emissions_df.merge(
        site_type_info, on=ofc.EMIS_DATA_COL_ACCESSORS.SITE_ID
    )

    return annual_emissions_and_site_type
