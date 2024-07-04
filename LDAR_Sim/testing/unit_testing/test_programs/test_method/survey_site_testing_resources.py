"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        survey_site_testing_resources.py
Purpose: Module for setup for testing survey_site for Methods

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

from datetime import date
from typing import Tuple
import pytest
from pytest_mock import MockerFixture
from scheduling.schedule_dataclasses import CrewDailyReport
from scheduling.schedule_dataclasses import SiteSurveyReport
from virtual_world.infrastructure import Site
from programs.method import Method
from sensors.default_sensor import DefaultSensor
from constants import param_default_const as pdc


def mock_site_initialization(self, site_properties: dict):
    for property, value in site_properties.items():
        setattr(self, property, value)


def mock_method_initialization(self, name: str, method_properties: dict, mock_sensor):
    self._name = name
    self._weather = False
    self._sensor = mock_sensor
    for property, value in method_properties.items():
        setattr(self, f"_{property}", value)


def setup_mock_objects_for_survey_report_testing(
    mocker: MockerFixture, site_properties: dict, method_properties: dict, crew_time: int
) -> Tuple[Site, Method, CrewDailyReport]:

    mocker.patch.object(Site, "__init__", mock_site_initialization)
    mocker.patch.object(
        Site, "get_method_survey_time", return_value=site_properties[pdc.Method_Params.TIME]
    )
    mock_site: Site = Site(site_properties)

    mocker.patch.object(Method, "__init__", mock_method_initialization)
    mock_sensor: DefaultSensor = mocker.Mock()
    mock_sensor.detect_emissions.return_value = True
    method: Method = Method("test_method", method_properties, mock_sensor)

    daily_report = CrewDailyReport(1, crew_time)

    return mock_site, method, daily_report


@pytest.fixture(name="survey_site_not_in_progress_can_complete_data")
def survey_site_not_in_progress_can_complete_data_fix():
    return (
        {"_id": 1, pdc.Method_Params.TIME: 120},
        {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
        SiteSurveyReport(site_id=1),
        180,
        SiteSurveyReport(
            site_id=1,
            time_surveyed=120,
            survey_in_progress=False,
            time_surveyed_current_day=120,
            survey_complete=True,
            time_spent_to_travel=30,
            method="test_method",
            survey_start_date=date(2023, 1, 1),
            survey_completion_date=date(2023, 1, 1),
        ),
    )


@pytest.fixture(name="survey_site_not_in_progress_cant_complete_data")
def survey_site_not_in_progress_cant_complete_data_fix():
    return (
        {"_id": 1, pdc.Method_Params.TIME: 200},
        {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
        SiteSurveyReport(site_id=1),
        180,
        SiteSurveyReport(
            site_id=1,
            time_surveyed=120,
            survey_in_progress=True,
            time_surveyed_current_day=120,
            survey_complete=False,
            time_spent_to_travel=30,
            method="test_method",
            survey_start_date=date(2023, 1, 1),
            survey_completion_date=None,
        ),
    )


@pytest.fixture(name="survey_site_in_progress_can_complete_data")
def survey_site_in_progress_can_complete_data_fix():
    return (
        {"_id": 1, pdc.Method_Params.TIME: 120},
        {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
        SiteSurveyReport(
            site_id=1,
            time_surveyed=60,
            time_surveyed_current_day=60,
            time_spent_to_travel=30,
            survey_in_progress=True,
            method="test_method",
            survey_start_date=date(2022, 1, 1),
        ),
        180,
        SiteSurveyReport(
            site_id=1,
            time_surveyed=120,
            survey_in_progress=False,
            time_surveyed_current_day=60,
            survey_complete=True,
            time_spent_to_travel=60,
            method="test_method",
            survey_start_date=date(2022, 1, 1),
            survey_completion_date=date(2023, 1, 1),
        ),
    )


@pytest.fixture(name="survey_site_in_progress_cant_complete_data")
def survey_site_in_progress_cant_complete_data_fix():
    return (
        {"_id": 1, pdc.Method_Params.TIME: 120},
        {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
        SiteSurveyReport(
            site_id=1,
            survey_start_date=date(2022, 12, 1),
            time_surveyed=60,
            time_surveyed_current_day=30,
            time_spent_to_travel=30,
            survey_in_progress=True,
            method="test_method",
        ),
        90,
        SiteSurveyReport(
            site_id=1,
            time_surveyed=90,
            survey_in_progress=True,
            time_surveyed_current_day=30,
            survey_complete=False,
            time_spent_to_travel=60,
            method="test_method",
            survey_start_date=date(2022, 12, 1),
            survey_completion_date=None,
        ),
    )


@pytest.fixture(name="survey_site_in_progress_no_time_to_survey_data")
def survey_site_in_progress_no_time_to_survey_data_fix():
    return (
        {"_id": 1, pdc.Method_Params.TIME: 120},
        {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
        SiteSurveyReport(
            site_id=1,
            survey_start_date=date(2022, 12, 1),
            time_surveyed=60,
            time_surveyed_current_day=30,
            time_spent_to_travel=30,
            survey_in_progress=True,
            method="test_method",
        ),
        60,
        SiteSurveyReport(
            site_id=1,
            time_surveyed=60,
            survey_in_progress=True,
            time_surveyed_current_day=0,
            survey_complete=False,
            time_spent_to_travel=0,
            method="test_method",
            survey_start_date=date(2022, 12, 1),
            survey_completion_date=None,
        ),
    )
