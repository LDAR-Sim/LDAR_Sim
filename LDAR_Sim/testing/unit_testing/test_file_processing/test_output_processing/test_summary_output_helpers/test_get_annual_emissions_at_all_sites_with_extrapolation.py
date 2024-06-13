"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_get_annual_emissions_at_all_sites_with_extrapolation.py
Purpose: Unit testing the get_annual_emissions_at_all_sites_with_extrapolation method.

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
import pytest
from constants import output_file_constants as ofc
from file_processing.output_processing.summary_output_helpers import (
    get_annual_emissions_at_all_sites_with_extrapolation,
)


@pytest.fixture(name="mock_est_emis_data_1_subtype_few_sites")
def mock_est_emis_data_1_subtype_few_sites_fix():
    return pd.DataFrame(
        {
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_ID: [1, 1, 1, 1, 2, 2],
            ofc.EMIS_DATA_COL_ACCESSORS.SURVEY_COMPLETION_DATE: [
                "2024-01-01",
                "2024-06-01",
                "2025-06-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.START_DATE: [
                "2024-01-01",
                "2024-01-01",
                "2025-06-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.END_DATE: [
                "2024-01-01",
                "2025-06-01",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.M_RATE: [0, 3, 0, 0, 0, 0],
            ofc.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT: [0, 1551, 0, 0, 0, 0],
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_MEASURED: [True, True, True, True, False, False],
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_TYPE: ["A", "A", "A", "A", "A", "A"],
        }
    )


@pytest.fixture(name="mock_est_emis_data_1_subtype_few_sites_expected_results")
def mock_est_emis_data_1_subtype_few_sites_expected_results_fix():
    return {
        2024: 2190,
        2025: 912,
    }


@pytest.fixture(name="mock_est_emis_data_1_subtype_multiple_sites")
def mock_est_emis_data_1_subtype_multiple_sites_fix():
    return pd.DataFrame(
        {
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_ID: [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4],
            ofc.EMIS_DATA_COL_ACCESSORS.SURVEY_COMPLETION_DATE: [
                "2024-01-01",
                "2024-06-01",
                "2025-06-01",
                "2025-12-31",
                "2024-01-01",
                "2024-03-01",
                "2025-04-01",
                "2025-12-31",
                "2024-01-01",
                "2024-07-01",
                "2025-08-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.START_DATE: [
                "2024-01-01",
                "2024-01-01",
                "2025-06-01",
                "2025-12-31",
                "2024-01-01",
                "2024-03-01",
                "2024-03-01",
                "2025-12-31",
                "2024-01-01",
                "2024-01-01",
                "2025-08-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.END_DATE: [
                "2024-01-01",
                "2025-06-01",
                "2025-12-31",
                "2025-12-31",
                "2024-03-01",
                "2024-03-01",
                "2025-12-31",
                "2025-12-31",
                "2024-01-01",
                "2025-08-01",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.M_RATE: [0, 3, 0, 0, 0, 0, 4, 0, 0, 2, 0, 0, 0, 0],
            ofc.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT: [
                0,
                1551,  # Emitting 1095 year 1 and 456 year 2
                0,
                0,
                0,
                0,
                2680,  # Emitting 1220 year 1 and 1460 year 2
                0,
                0,
                1156,  # Emitting 730 year 1 and 426 year 2
                0,
                0,
                0,
                0,
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_MEASURED: [
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_TYPE: [
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
            ],
        }
    )


@pytest.fixture(name="mock_est_emis_data_1_subtype_multiple_sites_expected_results")
def mock_est_emis_data_1_subtype_multiple_sites_expected_results_fix():
    return {
        # 4(1095 + 1220 + 730)/3 = 4060
        2024: 4060,
        # 4(456 + 1460 + 426)/3 = 3122.7
        2025: 3122.7,
    }


@pytest.fixture(name="mock_est_emis_data_3_subtypes_multiple_sites")
def mock_est_emis_data_3_subtypes_multiple_sites_fix():
    return pd.DataFrame(
        {
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_ID: [
                1,
                1,
                1,
                1,
                2,
                2,
                2,
                2,
                3,
                3,
                3,
                3,
                4,
                4,
                5,
                5,
                5,
                5,
                6,
                6,
                6,
                6,
                7,
                7,
                8,
                8,
                8,
                8,
                9,
                9,
                9,
                9,
                10,
                10,
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.SURVEY_COMPLETION_DATE: [
                "2024-01-01",
                "2024-06-01",
                "2025-06-01",
                "2025-12-31",
                "2024-01-01",
                "2024-03-01",
                "2025-04-01",
                "2025-12-31",
                "2024-01-01",
                "2024-07-01",
                "2025-08-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
                "2024-01-01",
                "2024-03-01",
                "2025-04-01",
                "2025-12-31",
                "2024-01-01",
                "2024-07-01",
                "2025-08-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
                "2024-01-01",
                "2024-03-01",
                "2025-04-01",
                "2025-12-31",
                "2024-01-01",
                "2024-07-01",
                "2025-08-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.START_DATE: [
                "2024-01-01",
                "2024-01-01",
                "2025-06-01",
                "2025-12-31",
                "2024-01-01",
                "2024-03-01",
                "2024-03-01",
                "2025-12-31",
                "2024-01-01",
                "2024-01-01",
                "2025-08-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
                "2024-01-01",
                "2024-03-01",
                "2024-03-01",
                "2025-12-31",
                "2024-01-01",
                "2024-01-01",
                "2025-08-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
                "2024-01-01",
                "2024-03-01",
                "2024-03-01",
                "2025-12-31",
                "2024-01-01",
                "2024-01-01",
                "2025-08-01",
                "2025-12-31",
                "2024-01-01",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.END_DATE: [
                "2024-01-01",
                "2025-06-01",
                "2025-12-31",
                "2025-12-31",
                "2024-03-01",
                "2024-03-01",
                "2025-12-31",
                "2025-12-31",
                "2024-01-01",
                "2025-08-01",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
                "2024-03-01",
                "2024-03-01",
                "2025-12-31",
                "2025-12-31",
                "2024-01-01",
                "2025-08-01",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
                "2024-03-01",
                "2024-03-01",
                "2025-12-31",
                "2025-12-31",
                "2024-01-01",
                "2025-08-01",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
                "2025-12-31",
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.M_RATE: [
                0,
                3,
                0,
                0,
                0,
                0,
                4,
                0,
                0,
                2,
                0,
                0,
                0,
                0,
                0,
                0,
                4,
                0,
                0,
                2,
                0,
                0,
                0,
                0,
                0,
                0,
                4,
                0,
                0,
                3,
                0,
                0,
                0,
                0,
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.EST_VOL_EMIT: [
                0,
                1551,  # Emitting 1095 year 1 and 456 year 2
                0,
                0,
                0,
                0,
                2680,  # Emitting 1220 year 1 and 1460 year 2
                0,
                0,
                1156,  # Emitting 730 year 1 and 426 year 2
                0,
                0,
                0,
                0,
                0,
                0,
                2680,  # Emitting 1220 year 1 and 1460 year 2
                0,
                0,
                1156,  # Emitting 730 year 1 and 426 year 2
                0,
                0,
                0,
                0,
                0,
                0,
                2680,  # Emitting 1220 year 1 and 1460 year 2
                0,
                0,
                1734,  # Emitting 1095 year 1 and 639 year 2
                0,
                0,
                0,
                0,
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_MEASURED: [
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
            ],
            ofc.EMIS_DATA_COL_ACCESSORS.SITE_TYPE: [
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "A",
                "B",
                "B",
                "B",
                "B",
                "B",
                "B",
                "B",
                "B",
                "B",
                "B",
                "C",
                "C",
                "C",
                "C",
                "C",
                "C",
                "C",
                "C",
                "C",
                "C",
            ],
        }
    )


@pytest.fixture(name="mock_est_emis_data_3_subtypes_multiple_sites_expected_results")
def mock_est_emis_data_3_subtypes_multiple_sites_expected_results_fix():
    return {
        # 4(1095 + 1220 + 730)/3 + 3(1220 + 730)/2 + 3(1220 + 1095)/2 = 10457.5
        2024: 10457.5,
        # 4(456 + 1460 + 426)/3 + 3(1460 + 426)/2 + 3(1460 + 639)/2 = 9100.166666667
        2025: 9100.17,
    }


@pytest.mark.parametrize(
    "mock_est_emis_data_name, mock_est_emis_data_expected_results_name, year",
    [
        (
            "mock_est_emis_data_1_subtype_few_sites",
            "mock_est_emis_data_1_subtype_few_sites_expected_results",
            2024,
        ),
        (
            "mock_est_emis_data_1_subtype_few_sites",
            "mock_est_emis_data_1_subtype_few_sites_expected_results",
            2025,
        ),
        (
            "mock_est_emis_data_1_subtype_multiple_sites",
            "mock_est_emis_data_1_subtype_multiple_sites_expected_results",
            2024,
        ),
        (
            "mock_est_emis_data_1_subtype_multiple_sites",
            "mock_est_emis_data_1_subtype_multiple_sites_expected_results",
            2025,
        ),
        (
            "mock_est_emis_data_3_subtypes_multiple_sites",
            "mock_est_emis_data_3_subtypes_multiple_sites_expected_results",
            2024,
        ),
        (
            "mock_est_emis_data_3_subtypes_multiple_sites",
            "mock_est_emis_data_3_subtypes_multiple_sites_expected_results",
            2025,
        ),
    ],
)
def test_get_annual_emissions_at_all_sites_with_extrapolation_returns_expected(
    request: pytest.FixtureRequest,
    mock_est_emis_data_name: str,
    mock_est_emis_data_expected_results_name: str,
    year: str,
):
    # Get the fixture values
    mock_est_emis_data: pd.DataFrame = request.getfixturevalue(mock_est_emis_data_name)
    mock_est_emis_data_expected_results: dict = request.getfixturevalue(
        mock_est_emis_data_expected_results_name
    )

    # Compute the result
    annual_emis_data: float = get_annual_emissions_at_all_sites_with_extrapolation(
        mock_est_emis_data, year
    )

    # Check if the result matches the expected output
    assert annual_emis_data == pytest.approx(mock_est_emis_data_expected_results[year], 1e-1)
