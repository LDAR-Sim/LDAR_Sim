"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_fixtures_end_dates.py
Purpose: Contains fixtures for unit tests of program_output_helpers.
In particular, the dataframes used to test the the calculate_end_date_factor function.

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


def simple_all_next_condition_df():
    data = {
        eca.NEXT_CONDITION: [True, True, True, True, True],
        eca.SURVEY_COMPLETION_DATE: pd.to_datetime(
            [
                "2021-01-01",
                "2021-01-10",
                "2021-01-20",
                "2021-01-30",
                "2021-02-09",
            ]
        ),
    }
    return pd.DataFrame(data)


def simple_all_not_next_condition_df():
    data = {
        eca.NEXT_CONDITION: [False, False, False, False, False],
        eca.SURVEY_COMPLETION_DATE: pd.to_datetime(
            [
                "2021-01-01",
                "2021-01-10",
                "2021-01-20",
                "2021-01-30",
                "2021-02-09",
            ]
        ),
    }
    return pd.DataFrame(data)


def simple_all_next_condition_end_dates_half():
    return pd.Series(
        pd.to_datetime(
            [
                "2021-01-05",
                "2021-01-15",
                "2021-01-25",
                "2021-02-04",
                "2021-02-09",
            ]
        ),
        name=eca.SURVEY_COMPLETION_DATE,
    )


def simple_all_next_condition_end_dates_zero():
    return pd.Series(
        pd.to_datetime(
            [
                "2021-01-10",
                "2021-01-20",
                "2021-01-30",
                "2021-02-09",
                "2021-02-09",
            ]
        ),
        name=eca.SURVEY_COMPLETION_DATE,
    )


def simple_all_next_condition_end_dates_one():
    return pd.Series(
        pd.to_datetime(
            [
                "2021-01-01",
                "2021-01-10",
                "2021-01-20",
                "2021-01-30",
                "2021-02-09",
            ]
        ),
        name=eca.SURVEY_COMPLETION_DATE,
    )


def simple_all_next_condition_end_dates_quarter():
    return pd.Series(
        pd.to_datetime(
            [
                "2021-01-07",
                "2021-01-17",
                "2021-01-27",
                "2021-02-06",
                "2021-02-09",
            ]
        ),
        name=eca.SURVEY_COMPLETION_DATE,
    )
