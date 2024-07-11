"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calculate_prev_condition.py
Purpose: Unit tests for the function calculate_prev_condition

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

import pytest
import pandas as pd
from file_processing.output_processing.program_output_helpers import calculate_prev_condition
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca
from testing.unit_testing.test_file_processing.test_output_processing.test_program_output_helpers.test_fixtures_conditions import (  # noqa
    simple_decreasing_rates,
    simple_increasing_rates,
    simple_increasing_rates_prev_cond_result,
    simple_decreasing_rates_prev_cond_result,
    mixed_rates,
    mixed_rates_prev_cond_result,
    mixed_zero_rates,
    mixed_zero_rates_prev_cond_result,
)


def test_calculate_prev_condition_for_empty_df():
    # Create an empty DataFrame
    expected_columns = [eca.SITE_ID, eca.M_RATE, eca.PREV_CONDITION]
    df = pd.DataFrame(columns=expected_columns)
    groupby = df.groupby(eca.SITE_ID)
    # Call the function
    result_df = calculate_prev_condition(df, groupby)
    assert result_df.empty
    assert all(column in result_df.columns for column in expected_columns)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (simple_decreasing_rates(), simple_decreasing_rates_prev_cond_result()),
        (simple_increasing_rates(), simple_increasing_rates_prev_cond_result()),
    ],
)
def test_calculate_simple_prev_condition(test_input, expected):
    groupby = test_input.groupby(eca.SITE_ID)
    # Call the function
    result_df = calculate_prev_condition(test_input, groupby)
    assert result_df.equals(expected)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (mixed_rates(), mixed_rates_prev_cond_result()),
        (mixed_zero_rates(), mixed_zero_rates_prev_cond_result()),
    ],
)
def test_calculate_complex_prev_condition(test_input, expected):
    groupby = test_input.groupby(eca.SITE_ID)
    # Call the function
    result_df = calculate_prev_condition(test_input, groupby)
    assert result_df.equals(expected)
