"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        method_testing_fixtures
Purpose: Contains fixtures for testing Methods

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
from datetime import date
from src.programs.method import Method
from src.virtual_world.infrastructure import Site
from collections import defaultdict
from src.scheduling.schedule_dataclasses import SiteSurveyReport
from src.sensors.default_site_level_sensor import DefaultSiteLevelSensor
from src.sensors.default_sensor import DefaultSensor
from src.virtual_world.emissions import Emission


@pytest.fixture
def mocker_fixture(mocker):
    def mock_initialize_sensor(properties):
        return {}

    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1)
    )
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    return mocker


def mock_average_t_btw_site(self):
    return 0


def mock_initialize_sensor(self, properties):
    return {}


def mock_get_method_survey_time(method_name, *args, **kwargs):
    return 120


def mock_check_weather(self, state, curr_date, site):
    return False


def mock_check_weather_t(self, state, curr_date, site):
    return True


def mock_get_average_method_surveys_required(self, site):
    return 1


def mock_get_travel_time(self):
    return 1


def mock_detect_emissions(self, site, meth_name, survey_report):
    return True


def mock_get_detectable_emissions(method_name):
    return {
        "test_meth": {
            "test_meth": [
                Emission(
                    1, 1, date(2023, 1, 1), date(2023, 1, 2), True, {"test_meth": 1}
                )
            ],
        },
    }


@pytest.fixture(name="simple_method_values")
def simple_method_values_fix(mocker):
    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1)
    )
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    properties: dict = {
        "n_crews": 5,
        "sensor": "default",
        "max_workday": 8,
        "consider_daylight": False,
        "t_bw_sites": [1],
        "is_follow_up": False,
        "weather_envs": {"wind": [0, 10], "temp": [-30, 30], "precip": [0, 1]},
    }
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        properties,
        current_date,
        state,
    )


@pytest.fixture(name="simple_method_values2")
def simple_method_values2_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1

    mocker.patch.object(
        site_mock, "get_method_survey_time", mock_get_method_survey_time
    )
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    properties: dict = {
        "n_crews": 5,
        "sensor": "default",
        "max_workday": 1,
        "t_bw_sites": [1],
        "is_follow_up": False,
        "consider_daylight": False,
        "weather_envs": {"wind": [0, 10], "temp": [-30, 30], "precip": [0, 1]},
    }
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        properties,
        current_date,
        state,
    )


@pytest.fixture(name="simple_method_values3")
def simple_method_values3_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1

    mocker.patch.object(
        site_mock, "get_method_survey_time", mock_get_method_survey_time
    )
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    properties: dict = {
        "n_crews": 5,
        "sensor": "default",
        "max_workday": 1,
        "t_bw_sites": [1],
        "is_follow_up": True,
        "consider_daylight": False,
        "weather_envs": {"wind": [0, 10], "temp": [-30, 30], "precip": [0, 1]},
    }
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        properties,
        current_date,
        state,
    )


@pytest.fixture(name="simple_method_values4")
def simple_method_values4_fix(mocker):
    mocker.patch.object(
        Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1)
    )
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    properties: dict = {
        "n_crews": 5,
        "sensor": "default",
        "max_workday": 8,
        "consider_daylight": False,
        "t_bw_sites": [1],
        "is_follow_up": False,
        "weather_envs": {"wind": [0, 10], "temp": [-30, 30], "precip": [0, 1]},
    }
    survey_report = SiteSurveyReport(site_id=1)
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        properties,
        current_date,
        state,
        survey_report,
    )


@pytest.fixture(name="simple_method_values5")
def simple_method_values5_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1

    mocker.patch.object(
        site_mock, "get_method_survey_time", mock_get_method_survey_time
    )
    mocker.patch.object(DefaultSensor, "detect_emissions", mock_detect_emissions)
    mocker.patch.object(
        Method,
        "_get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        Method,
        "_get_avg_t_bt_sites",
        mock_average_t_btw_site,
    )
    mocker.patch.object(
        Method,
        "check_weather",
        mock_check_weather_t,
    )
    mocker.patch.object(
        Method,
        "_get_average_survey_time_for_method",
        mock_get_method_survey_time,
    )
    mocker.patch.object(Method, "_get_travel_time", mock_get_travel_time)
    mocker.patch.object(
        DefaultSiteLevelSensor, "detect_emissions", mock_detect_emissions
    )
    mocker.patch.object(
        site_mock, "get_detectable_emissions", mock_get_detectable_emissions
    )
    properties: dict = {
        "n_crews": 5,
        "sensor": {"type": "default", "MDL": 1, "QE": 0},
        "max_workday": 8,
        "consider_daylight": False,
        "t_bw_sites": [1],
        "is_follow_up": False,
        "weather_envs": {"wind": [0, 10], "temp": [-30, 30], "precip": [0, 1]},
    }
    survey_report = SiteSurveyReport(site_id=1)
    current_date: date = date(2023, 1, 2)
    state = {"weather": create_random_state(), "daylight": [], "t": []}

    return (
        mocker,
        site_mock,
        properties,
        current_date,
        state,
        survey_report,
    )


def create_random_state():
    state = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    for givendate in [date(2023, 1, 1), date(2023, 1, 2), date(2023, 1, 3)]:
        for lat in [40, 35]:
            for long in [-75, -110]:
                temp = 20
                wind = 10
                precip = 0.5

                state[givendate][lat][long]["temp"] = temp
                state[givendate][lat][long]["wind"] = wind
                state[givendate][lat][long]["precip"] = precip

    return state
