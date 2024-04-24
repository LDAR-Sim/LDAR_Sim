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
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def closest_future_date(date: pd.Timestamp, date_list: list[pd.Timestamp]) -> pd.Timestamp:
    return min([d for d in date_list if d > date], default=None, key=lambda x: abs(x - date))


def find_df_row_value_w_match(
    value_to_match: Any, value_col: str, return_col: str, df: pd.DataFrame
):
    return df.loc[df.loc[:, value_col] == value_to_match, return_col].values[0]


# Function to calculate start_date based on conditions


def calculate_start_date(df):
    condition = df[eca.PREV_CONDITION]
    start_dates = np.where(
        condition,
        df[eca.SURVEY_COMPLETION_DATE],
        df[eca.SURVEY_COMPLETION_DATE].shift(1).fillna(df[eca.SURVEY_COMPLETION_DATE]),
    )
    return pd.Series(start_dates, index=df.index)


def calculate_end_date(df):
    condition = df[eca.NEXT_CONDITION]
    end_dates = np.where(
        condition,
        df[eca.SURVEY_COMPLETION_DATE],
        df[eca.SURVEY_COMPLETION_DATE].shift(-1).fillna(df[eca.SURVEY_COMPLETION_DATE]),
    )
    return pd.Series(end_dates, index=df.index)


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
