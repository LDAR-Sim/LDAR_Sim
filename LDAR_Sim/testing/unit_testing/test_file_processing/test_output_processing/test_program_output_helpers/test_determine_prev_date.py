"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_determine_prev_date.py
Purpose: Unit tests for the function determine_prev_date

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

from file_processing.output_processing.program_output_helpers import determine_prev_date
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def test_determine_prev_date():
    # Test input data
    test_input = pd.DataFrame(
        {
            eca.SURVEY_COMPLETION_DATE: pd.to_datetime(
                [
                    "2021-01-01",
                    "2021-01-02",
                    "2021-01-03",
                    "2021-01-04",
                    "2021-01-05",
                ]
            ),
            "value": [1, 2, 3, 4, 5],
        }
    )
    result: pd.Series = determine_prev_date(test_input)
    # Expected output
    expected_output = pd.Series(
        pd.to_datetime(
            [
                "2021-01-01",
                "2021-01-01",
                "2021-01-02",
                "2021-01-03",
                "2021-01-04",
            ]
        ),
        name=eca.SURVEY_COMPLETION_DATE,
    )
    # Ensure the function works as expected
    assert result.equals(expected_output)
