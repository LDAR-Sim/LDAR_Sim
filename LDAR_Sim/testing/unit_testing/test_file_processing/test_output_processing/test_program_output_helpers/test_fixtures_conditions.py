"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_fixtures_conditions.py
Purpose: Contains fixtures used for testing condition-related functions.

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

from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def simple_increasing_rates():
    data = {
        eca.PREV_CONDITION: [None, None, None, None, None],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [1, 2, 3, 4, 5],
        eca.NEXT_CONDITION: [None, None, None, None, None],
    }
    return pd.DataFrame(data)


def simple_decreasing_rates():
    data = {
        eca.PREV_CONDITION: [None, None, None, None, None],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [5, 4, 3, 2, 1],
        eca.NEXT_CONDITION: [None, None, None, None, None],
    }
    return pd.DataFrame(data)


def mixed_rates():
    data = {
        eca.PREV_CONDITION: [None, None, None, None, None],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [5, 1, 5, 1, 5],
        eca.NEXT_CONDITION: [None, None, None, None, None],
    }
    return pd.DataFrame(data)


def mixed_zero_rates():
    data = {
        eca.PREV_CONDITION: [None, None, None, None, None],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [0, 3, 4, 0, 0],
        eca.NEXT_CONDITION: [None, None, None, None, None],
    }
    return pd.DataFrame(data)


def simple_increasing_rates_prev_cond_result():
    data = {
        eca.PREV_CONDITION: [False, False, False, False, False],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [1, 2, 3, 4, 5],
        eca.NEXT_CONDITION: [None, None, None, None, None],
    }
    return pd.DataFrame(data)


def simple_decreasing_rates_prev_cond_result():
    data = {
        eca.PREV_CONDITION: [False, True, True, True, True],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [5, 4, 3, 2, 1],
        eca.NEXT_CONDITION: [None, None, None, None, None],
    }
    return pd.DataFrame(data)


def mixed_rates_prev_cond_result():
    data = {
        eca.PREV_CONDITION: [False, True, False, True, False],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [5, 1, 5, 1, 5],
        eca.NEXT_CONDITION: [None, None, None, None, None],
    }
    return pd.DataFrame(data)


def simple_increasing_rates_next_cond_result():
    data = {
        eca.PREV_CONDITION: [None, None, None, None, None],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [1, 2, 3, 4, 5],
        eca.NEXT_CONDITION: [True, True, True, True, False],
    }
    return pd.DataFrame(data)


def simple_decreasing_rates_next_cond_result():
    data = {
        eca.PREV_CONDITION: [None, None, None, None, None],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [5, 4, 3, 2, 1],
        eca.NEXT_CONDITION: [False, False, False, False, False],
    }
    return pd.DataFrame(data)


def mixed_rates_next_cond_result():
    data = {
        eca.PREV_CONDITION: [None, None, None, None, None],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [5, 1, 5, 1, 5],
        eca.NEXT_CONDITION: [False, True, False, True, False],
    }
    return pd.DataFrame(data)


def mixed_zero_rates_next_cond_result():
    data = {
        eca.PREV_CONDITION: [None, None, None, None, None],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [0, 3, 4, 0, 0],
        eca.NEXT_CONDITION: [True, True, False, False, False],
    }
    return pd.DataFrame(data)


def mixed_zero_rates_prev_cond_result():
    data = {
        eca.PREV_CONDITION: [False, False, False, True, True],
        eca.SITE_ID: [
            1,
            1,
            1,
            1,
            1,
        ],
        eca.M_RATE: [0, 3, 4, 0, 0],
        eca.NEXT_CONDITION: [None, None, None, None, None],
    }
    return pd.DataFrame(data)
