"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calculate_new_start_date.py
Purpose: Contains unit tests for testing test_calculate_new_start_date function.

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
from datetime import date

from file_processing.output_processing.program_output_helpers import calculate_new_start_date


def half_duration():
    return ([date(2021, 1, 1), date(2021, 1, 30), 0.5], date(2021, 1, 15))


def failing_case1():
    return ([date(2021, 1, 1), date(2021, 1, 30), 0], ValueError)


def failing_case2():
    return ([date(2021, 1, 1), date(2021, 1, 30), -0.9], ValueError)


def failing_case3():
    return ([date(2021, 1, 1), date(2021, 1, 30), 2.3], ValueError)


def part_duration():
    return ([date(2021, 1, 1), date(2021, 1, 10), 0.75], date(2021, 1, 3))


@pytest.mark.parametrize(
    "input, expected",
    [half_duration(), failing_case1(), failing_case2(), failing_case3(), part_duration()],
)
def test_calculate_new_start_date(input, expected):
    if expected == ValueError:
        with pytest.raises(ValueError):
            calculate_new_start_date(*input)
    else:
        assert calculate_new_start_date(*input) == expected
