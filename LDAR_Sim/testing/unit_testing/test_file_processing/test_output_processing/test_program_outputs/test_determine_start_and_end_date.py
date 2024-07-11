"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_determine_start_and_end_date.py
Purpose: Unit tests for the function to test if the start and end date determining
functions work together correctly. Individual functions are tested separately in
program_output_helpers

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
from datetime import date
from file_processing.output_processing.program_output import (
    determine_start_and_end_dates,
)
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def sorted_by_site_summary_df():
    data = {
        eca.SITE_ID: [1, 1, 1, 1, 2, 2, 2, 2],
        eca.SURVEY_COMPLETION_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
        ],
        eca.M_RATE: [1, 5, 0, 5, 1, 1, 5, 5],
    }
    df = pd.DataFrame(data)
    group_by = df.groupby(eca.SITE_ID)
    return df, group_by


def expected_df_one():
    data = {
        eca.SITE_ID: [1, 1, 1, 1, 2, 2, 2, 2],
        eca.SURVEY_COMPLETION_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
        ],
        eca.M_RATE: [1, 5, 0, 5, 1, 1, 5, 5],
        eca.PREV_CONDITION: [False, False, True, False, False, True, False, True],
        eca.NEXT_CONDITION: [True, False, True, False, False, True, False, False],
        eca.START_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 1),
            date(2021, 1, 20),
            date(2021, 1, 20),
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 10),
            date(2021, 1, 30),
        ],
        eca.END_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 20),
            date(2021, 1, 20),
            date(2021, 1, 30),
            date(2021, 1, 10),
            date(2021, 1, 10),
            date(2021, 1, 30),
            date(2021, 1, 30),
        ],
    }
    df = pd.DataFrame(data)
    df[eca.START_DATE] = pd.to_datetime(df[eca.START_DATE])
    df[eca.END_DATE] = pd.to_datetime(df[eca.END_DATE])
    return df


def expected_df_zero():
    data = {
        eca.SITE_ID: [1, 1, 1, 1, 2, 2, 2, 2],
        eca.SURVEY_COMPLETION_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
        ],
        eca.M_RATE: [1, 5, 0, 5, 1, 1, 5, 5],
        eca.PREV_CONDITION: [False, False, True, False, False, True, False, True],
        eca.NEXT_CONDITION: [True, False, True, False, False, True, False, False],
        eca.START_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 10),
            date(2021, 1, 30),
            date(2021, 1, 1),
            date(2021, 1, 1),
            date(2021, 1, 20),
            date(2021, 1, 20),
        ],
        eca.END_DATE: [
            date(2021, 1, 10),
            date(2021, 1, 10),
            date(2021, 1, 30),
            date(2021, 1, 30),
            date(2021, 1, 1),
            date(2021, 1, 20),
            date(2021, 1, 20),
            date(2021, 1, 30),
        ],
    }
    df = pd.DataFrame(data)
    df[eca.START_DATE] = pd.to_datetime(df[eca.START_DATE])
    df[eca.END_DATE] = pd.to_datetime(df[eca.END_DATE])
    return df


def expected_df_half():
    data = {
        eca.SITE_ID: [1, 1, 1, 1, 2, 2, 2, 2],
        eca.SURVEY_COMPLETION_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
        ],
        eca.M_RATE: [1, 5, 0, 5, 1, 1, 5, 5],
        eca.PREV_CONDITION: [False, False, True, False, False, True, False, True],
        eca.NEXT_CONDITION: [True, False, True, False, False, True, False, False],
        eca.START_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 5),
            date(2021, 1, 15),
            date(2021, 1, 25),
            date(2021, 1, 1),
            date(2021, 1, 5),
            date(2021, 1, 15),
            date(2021, 1, 25),
        ],
        eca.END_DATE: [
            date(2021, 1, 5),
            date(2021, 1, 15),
            date(2021, 1, 25),
            date(2021, 1, 30),
            date(2021, 1, 5),
            date(2021, 1, 15),
            date(2021, 1, 25),
            date(2021, 1, 30),
        ],
    }
    df = pd.DataFrame(data)
    df[eca.START_DATE] = pd.to_datetime(df[eca.START_DATE])
    df[eca.END_DATE] = pd.to_datetime(df[eca.END_DATE])
    return df


def expected_df_quart():
    data = {
        eca.SITE_ID: [1, 1, 1, 1, 2, 2, 2, 2],
        eca.SURVEY_COMPLETION_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
            date(2021, 1, 1),
            date(2021, 1, 10),
            date(2021, 1, 20),
            date(2021, 1, 30),
        ],
        eca.M_RATE: [1, 5, 0, 5, 1, 1, 5, 5],
        eca.PREV_CONDITION: [False, False, True, False, False, True, False, True],
        eca.NEXT_CONDITION: [True, False, True, False, False, True, False, False],
        eca.START_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 7),
            date(2021, 1, 12),
            date(2021, 1, 27),
            date(2021, 1, 1),
            date(2021, 1, 3),
            date(2021, 1, 17),
            date(2021, 1, 22),
        ],
        eca.END_DATE: [
            date(2021, 1, 7),
            date(2021, 1, 12),
            date(2021, 1, 27),
            date(2021, 1, 30),
            date(2021, 1, 3),
            date(2021, 1, 17),
            date(2021, 1, 22),
            date(2021, 1, 30),
        ],
    }
    df = pd.DataFrame(data)
    df[eca.START_DATE] = pd.to_datetime(df[eca.START_DATE])
    df[eca.END_DATE] = pd.to_datetime(df[eca.END_DATE])
    return df


@pytest.mark.parametrize(
    "test_input, ratio, expected",
    [
        (sorted_by_site_summary_df(), 1.0, expected_df_one()),
        (sorted_by_site_summary_df(), 0.0, expected_df_zero()),
        (sorted_by_site_summary_df(), 0.5, expected_df_half()),
        (sorted_by_site_summary_df(), 0.25, expected_df_quart()),
    ],
)
def test_determine_start_and_end_dates(test_input, ratio, expected):
    df, group_by = test_input
    result = determine_start_and_end_dates(df, group_by, ratio)
    pd.testing.assert_frame_equal(result, expected)
