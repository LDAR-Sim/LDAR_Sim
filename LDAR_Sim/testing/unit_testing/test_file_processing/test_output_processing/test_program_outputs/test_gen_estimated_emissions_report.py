"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_gen_estimated_emissions_report
Purpose: Testing the gen estimated emissions report method.

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

from pathlib import Path
from typing import Tuple
import pytest  # noqa
import pandas as pd
from datetime import date
from src.file_processing.output_processing.program_outputs import gen_estimated_emissions_report
from src.file_processing.output_processing import output_constants
import numpy as np


tolerance = 1e-9


def generate_fake_test_data_no_fugitives() -> (
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, date, date]
):
    site_survey_reports_summary: pd.DataFrame = pd.DataFrame(
        {
            "site_id": [1, 1, 1, 1, 2, 2, 2, 2],
            "site_measured_rate": [1, 2, 3, 4, 4, 3, 2, 1],
            "survey_completion_date": [
                "2024-01-30",
                "2024-02-01",
                "2024-05-06",
                "2024-09-04",
                "2024-01-29",
                "2024-03-04",
                "2024-08-09",
                "2024-11-11",
            ],
        }
    )

    fugitive_emissions_rates_and_repair_dates: pd.DataFrame = pd.DataFrame()

    start_date: date = date(2024, 1, 1)

    end_date: date = date(2024, 12, 31)

    expected_output: pd.DataFrame = pd.DataFrame(
        {"site_id": [1, 2], "year": [2024, 2024], "volume_emitted": [110073.6, 83289.6]}
    )
    expected_output["year"] = expected_output["year"].astype("int32")

    return (
        site_survey_reports_summary,
        fugitive_emissions_rates_and_repair_dates,
        expected_output,
        start_date,
        end_date,
    )


def generate_fake_test_data_with_fugitives() -> (
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, date, date]
):
    site_survey_reports_summary: pd.DataFrame = pd.DataFrame(
        {
            "site_id": [1, 1, 1, 1, 2, 2, 2, 2],
            "site_measured_rate": [1, 2, 3, 4, 4, 3, 2, 1],
            "survey_completion_date": [
                "2024-01-30",
                "2024-02-01",
                "2024-05-06",
                "2024-09-04",
                "2024-01-29",
                "2024-03-04",
                "2024-08-09",
                "2024-11-11",
            ],
        }
    )

    fugitive_emissions_rates_and_repair_dates: pd.DataFrame = pd.DataFrame(
        {
            output_constants.EMIS_DATA_COL_ACCESSORS.SITE_ID: [1, 1, 2, 2],
            output_constants.EMIS_DATA_COL_ACCESSORS.DATE_REP: [
                "2024-03-03",
                "2024-05-28",
                "2024-03-16",
                "2024-08-26",
            ],
            output_constants.EMIS_DATA_COL_ACCESSORS.M_RATE: [1, 1, 2, 2],
        }
    )

    start_date: date = date(2024, 1, 1)

    end_date: date = date(2024, 12, 31)

    expected_output: pd.DataFrame = pd.DataFrame(
        {"site_id": [1, 2], "year": [2024, 2024], "volume_emitted": [110073.6, 44755.2]}
    )
    expected_output["year"] = expected_output["year"].astype("int32")

    return (
        site_survey_reports_summary,
        fugitive_emissions_rates_and_repair_dates,
        expected_output,
        start_date,
        end_date,
    )


def generate_fake_test_data_with_partial_fugitives() -> (
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, date, date]
):
    site_survey_reports_summary: pd.DataFrame = pd.DataFrame(
        {
            "site_id": [1, 1, 1, 1, 2, 2, 2, 2],
            "site_measured_rate": [1, 2, 3, 4, 4, 3, 2, 1],
            "survey_completion_date": [
                "2024-01-30",
                "2024-02-01",
                "2024-05-06",
                "2024-09-04",
                "2024-01-29",
                "2024-03-04",
                "2024-08-09",
                "2024-11-11",
            ],
        }
    )

    fugitive_emissions_rates_and_repair_dates: pd.DataFrame = pd.DataFrame(
        {
            output_constants.EMIS_DATA_COL_ACCESSORS.SITE_ID: [2, 2],
            output_constants.EMIS_DATA_COL_ACCESSORS.DATE_REP: [
                "2024-03-16",
                "2024-08-26",
            ],
            output_constants.EMIS_DATA_COL_ACCESSORS.M_RATE: [2, 2],
        }
    )

    start_date: date = date(2024, 1, 1)

    end_date: date = date(2024, 12, 31)

    expected_output: pd.DataFrame = pd.DataFrame(
        {"site_id": [1, 2], "year": [2024, 2024], "volume_emitted": [110073.6, 44755.2]}
    )
    expected_output["year"] = expected_output["year"].astype("int32")

    return (
        site_survey_reports_summary,
        fugitive_emissions_rates_and_repair_dates,
        expected_output,
        start_date,
        end_date,
    )


def test_gen_estimated_emissions_report_simple_case_no_fugitives(mocker):
    captured_output: list[pd.DataFrame] = []

    # Define a mock to_csv function that will capture the dataframe
    # calling to csv and do nothing else
    def mock_to_csv(self, *args, **kwargs):
        captured_output.append(self)

    # Patch pd.DataFrame.to_csv with the mock function
    mocker.patch.object(pd.DataFrame, "to_csv", mock_to_csv)

    # Setup test data
    mock_survey_data, mock_fugitives_date, expected_output, start_date, end_date = (
        generate_fake_test_data_no_fugitives()
    )
    mock_survey_data: pd.DataFrame
    mock_fugitives_date: pd.DataFrame
    expected_output: pd.DataFrame
    start_date: date
    end_date: date

    # Call the method to test
    gen_estimated_emissions_report(
        site_survey_reports_summary=mock_survey_data,
        fugutive_emissions_rates_and_repair_dates=mock_fugitives_date,
        output_dir=Path("test_output_dir"),
        name="test_name",
        start_date=start_date,
        end_date=end_date,
    )

    assert np.allclose(captured_output[0], expected_output, atol=tolerance)


def test_gen_estimated_emissions_report_simple_case_with_fugitives(mocker):
    captured_output: list[pd.DataFrame] = []

    # Define a mock to_csv function that will capture the dataframe
    # calling to csv and do nothing else
    def mock_to_csv(self, *args, **kwargs):
        captured_output.append(self)

    # Patch pd.DataFrame.to_csv with the mock function
    mocker.patch.object(pd.DataFrame, "to_csv", mock_to_csv)

    # Setup test data
    mock_survey_data, mock_fugitives_date, expected_output, start_date, end_date = (
        generate_fake_test_data_with_fugitives()
    )
    mock_survey_data: pd.DataFrame
    mock_fugitives_date: pd.DataFrame
    expected_output: pd.DataFrame
    start_date: date
    end_date: date

    # Call the method to test
    gen_estimated_emissions_report(
        site_survey_reports_summary=mock_survey_data,
        fugutive_emissions_rates_and_repair_dates=mock_fugitives_date,
        output_dir=Path("test_output_dir"),
        name="test_name",
        start_date=start_date,
        end_date=end_date,
    )

    assert np.allclose(captured_output[0], expected_output, atol=tolerance)


def test_gen_estimated_emissions_report_simple_case_with_partial_fugitives(mocker):
    captured_output: list[pd.DataFrame] = []

    # Define a mock to_csv function that will capture the dataframe
    # calling to csv and do nothing else
    def mock_to_csv(self, *args, **kwargs):
        captured_output.append(self)

    # Patch pd.DataFrame.to_csv with the mock function
    mocker.patch.object(pd.DataFrame, "to_csv", mock_to_csv)

    # Setup test data
    mock_survey_data, mock_fugitives_date, expected_output, start_date, end_date = (
        generate_fake_test_data_with_partial_fugitives()
    )
    mock_survey_data: pd.DataFrame
    mock_fugitives_date: pd.DataFrame
    expected_output: pd.DataFrame
    start_date: date
    end_date: date

    # Call the method to test
    gen_estimated_emissions_report(
        site_survey_reports_summary=mock_survey_data,
        fugutive_emissions_rates_and_repair_dates=mock_fugitives_date,
        output_dir=Path("test_output_dir"),
        name="test_name",
        start_date=start_date,
        end_date=end_date,
    )

    assert np.allclose(captured_output[0], expected_output, atol=tolerance)
