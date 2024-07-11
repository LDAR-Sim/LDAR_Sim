"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        program_output_helpers.py
Purpose: Contains helper functions for processing program output data.

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

import pandas as pd
import numpy as np
from typing import Any
from constants.general_const import Conversion_Constants as conv_const
from constants.output_file_constants import (
    EMIS_DATA_COL_ACCESSORS as eca,
    EMIS_DATA_TEMP_COLUMNS as edtc,
)


def find_closest_future_date(
    reference_date: pd.Timestamp, potential_futureDates: list[tuple[pd.Timestamp, pd.Timestamp]]
) -> pd.Timestamp:

    # Find the index of the closest future survey completion date
    closest_index = min(
        [i for i, d in enumerate(potential_futureDates) if d[0] > reference_date],
        default=None,
        key=lambda i: abs(potential_futureDates[i][0] - reference_date),
    )
    # if no future survey completion date is found, return None
    if closest_index is None:
        return None
    # if the new start date based on the ratio is before repair date, return the repair date
    elif potential_futureDates[closest_index][1] < reference_date:
        return reference_date
    # otherwise, return the new start date
    else:
        return potential_futureDates[closest_index][1]


def find_df_row_value_w_match(
    value_to_match: Any, value_col: str, return_col: str, df: pd.DataFrame
):
    if not df.empty:
        matching_rows = df.loc[df.loc[:, value_col] == value_to_match, return_col].values
        if len(matching_rows) > 0:
            return matching_rows[0]
        else:
            # Handle case where no matching rows were found
            return False
    else:
        return False


def determine_prev_date(df: pd.DataFrame):
    prev_dates = df[eca.SURVEY_COMPLETION_DATE].shift(1).fillna(df[eca.SURVEY_COMPLETION_DATE])
    return pd.Series(prev_dates, index=df.index)


def determine_next_date(df: pd.DataFrame):
    next_dates = df[eca.SURVEY_COMPLETION_DATE].shift(-1).fillna(df[eca.SURVEY_COMPLETION_DATE])
    return pd.Series(next_dates, index=df.index)


def calculate_duration_between_dates(
    dataframe: pd.DataFrame, start_date_col: str, end_date_col: str
):
    # Ensure both dates are datetime objects
    dataframe[start_date_col] = pd.to_datetime(dataframe[start_date_col])
    dataframe[end_date_col] = pd.to_datetime(dataframe[end_date_col])

    # Vectorized operation to calculate duration
    duration = (dataframe[end_date_col] - dataframe[start_date_col]).dt.days

    return duration


def calculate_factor(condition: pd.Series, factor):
    series_factor: pd.Series = np.where(condition, 1 - factor, factor)
    return series_factor


def calculate_start_date(df: pd.DataFrame, factor: float):
    condition = df[eca.PREV_CONDITION]
    df[edtc.PREV_DATE] = determine_prev_date(df)

    # Calculate the factor to use based on the condition
    duration_scaling_factor: np.array[float] = calculate_factor(condition, factor)

    # Calculate the duration between the previous date and the current date
    df[edtc.DURATION] = calculate_duration_between_dates(
        df, edtc.PREV_DATE, eca.SURVEY_COMPLETION_DATE
    )

    # Calculate start dates using the adjusted duration and factor
    start_dates = df[eca.SURVEY_COMPLETION_DATE] - pd.to_timedelta(
        np.ceil(df[edtc.DURATION] * duration_scaling_factor), unit="D"
    )
    return start_dates


def calculate_end_date(df: pd.DataFrame, factor: float):
    condition = df[eca.NEXT_CONDITION]
    df[edtc.NEXT_DATE] = determine_next_date(df)

    # Calculate the factor to use based on the condition
    duration_scaling_factor: pd.Series = calculate_factor(condition, factor)

    # Calculate the duration between the current date and the next date
    df[edtc.DURATION] = calculate_duration_between_dates(
        df, eca.SURVEY_COMPLETION_DATE, edtc.NEXT_DATE
    )

    # Calculate end dates using the adjusted duration and factor
    end_dates = df[eca.SURVEY_COMPLETION_DATE] + pd.to_timedelta(
        np.floor(df[edtc.DURATION] * duration_scaling_factor), unit="D"
    )
    return end_dates


def calculate_volume_emitted(row):
    start_date = row[eca.START_DATE]
    end_date = row[eca.END_DATE]
    measured_rate = row[eca.M_RATE]

    volume = (
        measured_rate * (end_date - start_date).days * conv_const.GRAMS_PER_SECOND_TO_KG_PER_DAY
    )
    return volume


def expand_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Expand a column of a DataFrame that contains lists of dictionaries
    Args:
        df (pd.DataFrame): The DataFrame
        column (str): The column to expand
    Returns:
        pd.DataFrame: The expanded DataFrame
    """
    # Explode the column
    exploded_df = df.explode(column).reset_index(drop=True)
    expanded_df = pd.json_normalize(exploded_df[column])

    # Concatenate exploded_df and expanded_df along the columns axis
    combined_df = pd.concat([expanded_df, exploded_df], axis=1)

    # Remove duplicate columns
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    return combined_df


def calculate_prev_condition(site_summary_data, grouped_by_site_summary):
    """
    Calculate the previous condition based on the emission rate difference.

    Parameters:
    - site_summary_data: DataFrame containing the emission rates and other related data.
    - grouped_by_site_summary: groupby of the site_summary_data DataFrame.
    Returns:
    - DataFrame with updated previous condition column.
    """
    site_summary_data[eca.PREV_CONDITION] = grouped_by_site_summary[eca.M_RATE].diff() <= 0
    return site_summary_data


def calculate_next_condition(site_summary_data, grouped_by_site_summary):
    """
    Calculate the next condition based on the emission rate difference.

    Parameters:
    - site_summary_data: DataFrame containing the emission rates and other related data.
    - grouped_by_site_summary: groupby of the site_summary_data DataFrame.

    Returns:
    - DataFrame with updated next condition column.
    """
    site_summary_data[eca.NEXT_CONDITION] = grouped_by_site_summary[eca.M_RATE].diff(-1) < 0
    return site_summary_data
