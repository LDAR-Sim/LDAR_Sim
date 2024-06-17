"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test get yearly value for multi day stat
Purpose: Unit testing the get yearly value for multi day stat method.

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
import pytest

from file_processing.output_processing.summary_output_helpers import (
    get_yearly_value_for_multi_day_stat,
)


def test_000_get_yearly_value_for_multi_day_stat_functions_as_expected_simple_1():

    # Setup test data
    df = pd.DataFrame(
        {
            "start_date": ["2020-01-01", "2020-01-01", "2020-01-01", "2020-01-01"],
            "end_date": ["2021-12-31", "2021-12-31", "2020-01-02", "2020-01-02"],
            "value": [5, 5, 5, 5],
        }
    )
    column = "value"
    year = 2020
    start_date_col = "start_date"
    end_date_col = "end_date"

    # Define expected output
    expected_output = 15

    # Get the result
    result = get_yearly_value_for_multi_day_stat(df, column, year, start_date_col, end_date_col)

    # Check if the result matches the expected output
    assert result == pytest.approx(expected_output, 1e-1)


def test_000_get_yearly_value_for_multi_day_stat_functions_as_expected_simple_2():

    # Setup test data
    df = pd.DataFrame(
        {
            "start_date": ["2020-01-01", "2020-01-01", "2020-01-01", "2020-01-01"],
            "end_date": ["2023-12-31", "2023-12-31", "2020-01-02", "2020-01-02"],
            "value": [20, 20, 5, 5],
        }
    )
    column = "value"
    year = 2021
    start_date_col = "start_date"
    end_date_col = "end_date"

    # Define expected output
    expected_output = 10

    # Get the result
    result = get_yearly_value_for_multi_day_stat(df, column, year, start_date_col, end_date_col)

    # Check if the result matches the expected output
    assert result == pytest.approx(expected_output, 1e-1)


def test_000_get_yearly_value_for_multi_day_stat_functions_as_expected_simple_3():

    # Setup test data
    df = pd.DataFrame(
        {
            "start_date": ["2020-01-01", "2020-01-01", "2021-06-30", "2021-06-30"],
            "end_date": ["2021-06-30", "2021-06-30", "2022-12-31", "2022-12-31"],
            "value": [15, 15, 15, 15],
        }
    )
    column = "value"
    year = 2021
    start_date_col = "start_date"
    end_date_col = "end_date"

    # Define expected output
    expected_output = 20

    # Get the result
    result = get_yearly_value_for_multi_day_stat(df, column, year, start_date_col, end_date_col)

    # Check if the result matches the expected output
    assert result == pytest.approx(expected_output, abs=1e-1)


def test_000_get_yearly_value_for_multi_day_stat_functions_as_expected_missing_end_dates():
    df = pd.DataFrame(
        {
            "start_date": ["2020-01-01", "2020-01-01", "2020-01-01", "2020-01-01"],
            "end_date": ["2021-06-30", pd.NaT, "2021-12-31", pd.NaT],
            "value": [15, 20, 20, 20],
        }
    )
    column = "value"
    year = 2021
    start_date_col = "start_date"
    end_date_col = "end_date"

    # Define expected output
    expected_output = 35

    # Get the result
    result = get_yearly_value_for_multi_day_stat(df, column, year, start_date_col, end_date_col)

    # Check if the result matches the expected output
    assert result == pytest.approx(expected_output, abs=1e-1)
