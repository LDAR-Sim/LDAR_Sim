"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calculate_start_date_factor.py
Purpose: Unit tests for the function calculate_start_date

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

from file_processing.output_processing.program_output_helpers import calculate_start_date
from testing.unit_testing.test_file_processing.test_output_processing.test_program_output_helpers.test_fixtures_start_dates import (  # noqa
    simple_all_prev_condition_df,
    simple_all_not_prev_condition_df,
    simple_all_prev_condition_start_dates_half,
    simple_all_prev_condition_start_dates_quarter,
    simple_all_prev_condition_start_dates_zero,
    simple_all_prev_condition_start_dates_one,
    mix_condition_df,
    mix_start_dates_quarter,
    mix_start_dates_one,
)


# the simple_all_not_prev_condition tests should use the
# opposite of the all_prev_condition  results
@pytest.mark.parametrize(
    "test_input,ratio, expected",
    [
        (simple_all_prev_condition_df(), 0.5, simple_all_prev_condition_start_dates_half()),
        (simple_all_prev_condition_df(), 0.75, simple_all_prev_condition_start_dates_quarter()),
        (simple_all_not_prev_condition_df(), 0.5, simple_all_prev_condition_start_dates_half()),
        (simple_all_not_prev_condition_df(), 0.25, simple_all_prev_condition_start_dates_quarter()),
    ],
)
def test_calculate_start_date(test_input, ratio, expected):
    result = calculate_start_date(test_input, ratio)
    assert result.equals(expected)


@pytest.mark.parametrize(
    "test_input,ratio, expected",
    [
        (simple_all_prev_condition_df(), 0.0, simple_all_prev_condition_start_dates_one()),
        (simple_all_prev_condition_df(), 1.0, simple_all_prev_condition_start_dates_zero()),
        (simple_all_not_prev_condition_df(), 0.0, simple_all_prev_condition_start_dates_zero()),
        (simple_all_not_prev_condition_df(), 1.0, simple_all_prev_condition_start_dates_one()),
    ],
)
def test_calculate_start_date_edge_cases(test_input, ratio, expected):
    result = calculate_start_date(test_input, ratio)
    assert result.equals(expected)


@pytest.mark.parametrize(
    "test_input,ratio, expected",
    [
        (mix_condition_df(), 0.75, mix_start_dates_quarter()),
        (mix_condition_df(), 1.0, mix_start_dates_one()),
    ],
)
def test_calculate_start_date_mixed_conditions(test_input, ratio, expected):
    result = calculate_start_date(test_input, ratio)
    assert result.equals(expected)
