"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calculate_duration_between_dates.py
Purpose: Unit tests for the function to calculate the duration between dates

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
import numpy as np
import pandas as pd
from datetime import date
from file_processing.output_processing.program_output_helpers import (
    calculate_duration_between_dates,
)
from constants.output_file_constants import (
    EMIS_DATA_COL_ACCESSORS as eca,
    EMIS_DATA_TEMP_COLUMNS as edtc,
)


def simple_dates():
    data = {
        eca.SURVEY_COMPLETION_DATE: [
            date(2021, 1, 1),
            date(2021, 1, 2),
            date(2021, 1, 3),
            date(2021, 1, 4),
            date(2021, 1, 5),
        ],
        edtc.NEXT_DATE: [
            date(2021, 1, 5),
            date(2021, 1, 6),
            date(2021, 1, 7),
            date(2021, 1, 8),
            date(2021, 1, 9),
        ],
    }
    return pd.DataFrame(data)


def simple_dates_result():
    data = [4, 4, 4, 4, 4]
    return pd.Series(data=data)


@pytest.mark.parametrize("test_input, expected", [(simple_dates(), simple_dates_result())])
def test_calculate_duration_between_dates_simple_case(test_input, expected):
    # Test input data

    result = calculate_duration_between_dates(
        test_input, eca.SURVEY_COMPLETION_DATE, edtc.NEXT_DATE
    )

    np.testing.assert_array_equal(result, expected)
