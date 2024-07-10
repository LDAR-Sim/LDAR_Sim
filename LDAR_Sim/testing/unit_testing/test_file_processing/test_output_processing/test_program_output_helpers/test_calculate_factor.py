"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calculate_factor.py
Purpose: Unit tests for the function calculate_factor

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
import numpy as np
from file_processing.output_processing.program_output_helpers import calculate_factor
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def simple_all_true():
    data = [True, True, True, True, True]

    return pd.Series(data=data, name=eca.PREV_CONDITION)


def simple_all_false():
    data = [False, False, False, False, False]

    return pd.Series(data=data, name=eca.PREV_CONDITION)


def mixed():
    data = [True, False, True, False, True]

    return pd.Series(data=data, name=eca.PREV_CONDITION)


def simple_one():
    return np.array([1, 1, 1, 1, 1])


def simple_zero():
    return np.array([0, 0, 0, 0, 0])


def simple_three_quart():
    return np.array([0.75, 0.75, 0.75, 0.75, 0.75])


def simple_quart():
    return np.array([0.25, 0.25, 0.25, 0.25, 0.25])


def mixed_quart():
    return np.array([0.75, 0.25, 0.75, 0.25, 0.75])


def simple_half():
    return np.array([0.5, 0.5, 0.5, 0.5, 0.5])


def mixed_zero():
    return np.array([1, 0, 1, 0, 1])


def mixed_one():
    return np.array([0, 1, 0, 1, 0])


@pytest.mark.parametrize(
    "test_input, factor, expected",
    [
        (simple_all_true(), 1, simple_zero()),
        (simple_all_true(), 0, simple_one()),
        (simple_all_false(), 1, simple_one()),
        (simple_all_false(), 0, simple_zero()),
        (mixed(), 1, mixed_one()),
        (mixed(), 0, mixed_zero()),
    ],
)
def test_simple_cases_calculate_factor(test_input, factor, expected):
    result: list = calculate_factor(test_input, factor)
    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    "test_input, factor, expected",
    [
        (simple_all_true(), 0.5, simple_half()),
        (simple_all_false(), 0.5, simple_half()),
        (mixed(), 0.5, simple_half()),
    ],
)
def test_half_calculate_factor(test_input, factor, expected):
    result: list = calculate_factor(test_input, factor)
    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    "test_input, factor, expected",
    [
        (simple_all_true(), 0.25, simple_three_quart()),
        (simple_all_false(), 0.25, simple_quart()),
        (mixed(), 0.25, mixed_quart()),
    ],
)
def test_partial_calculate_factor(test_input, factor, expected):
    result: list = calculate_factor(test_input, factor)
    np.testing.assert_array_equal(result, expected)
