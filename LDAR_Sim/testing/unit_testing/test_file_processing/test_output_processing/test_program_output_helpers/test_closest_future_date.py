"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_closest_future_date.py
Purpose: Contains unit tests for testing closest_future_date function.

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

from file_processing.output_processing.program_output_helpers import closest_future_date


@pytest.fixture
def future_and_past_dates():
    return {
        "input_date": pd.Timestamp("2023-01-01"),
        "date_dict": [
            (pd.Timestamp("2023-01-02"), pd.Timestamp("2023-01-03")),
            (pd.Timestamp("2022-12-31"), pd.Timestamp("2022-12-30")),
        ],
        "expected": pd.Timestamp("2023-01-03"),
    }


@pytest.fixture
def only_past_dates():
    return {
        "input_date": pd.Timestamp("2023-01-01"),
        "date_dict": [
            (pd.Timestamp("2022-12-30"), pd.Timestamp("2022-12-29")),
            (pd.Timestamp("2022-12-31"), pd.Timestamp("2022-12-28")),
        ],
        "expected": None,
    }


@pytest.fixture
def empty_dates():
    return {
        "input_date": pd.Timestamp("2023-01-01"),
        "date_dict": [],
        "expected": None,
    }


@pytest.fixture
def future_date_with_past_start_date():
    return {
        "input_date": pd.Timestamp("2023-01-01"),
        "date_dict": [(pd.Timestamp("2023-01-03"), pd.Timestamp("2022-12-31"))],
        "expected": pd.Timestamp("2023-01-01"),
    }


@pytest.fixture
def multiple_future_dates():
    return {
        "input_date": pd.Timestamp("2023-01-01"),
        "date_dict": [
            (pd.Timestamp("2023-01-04"), pd.Timestamp("2023-01-05")),
            (pd.Timestamp("2023-01-02"), pd.Timestamp("2023-01-03")),
            (pd.Timestamp("2023-01-05"), pd.Timestamp("2023-01-06")),
        ],
        "expected": pd.Timestamp("2023-01-03"),
    }


@pytest.mark.parametrize(
    "fixture",
    [
        "future_and_past_dates",
        "only_past_dates",
        "empty_dates",
        "future_date_with_past_start_date",
        "multiple_future_dates",
    ],
)
def test_closest_future_date_new(request, fixture):
    test_data = request.getfixturevalue(fixture)
    assert (
        closest_future_date(test_data["input_date"], test_data["date_dict"])
        == test_data["expected"]
    )
