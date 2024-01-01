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
from src.scheduling.survey_planner import SurveyPlanner
from src.virtual_world.infrastructure import Site
from collections import defaultdict
from src.scheduling.workplan import SiteSurveyReport


@pytest.fixture
def mocker_fixture(mocker):
    def mock_initialize_sensor(properties):
        return {}

    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    return mocker


def mock_initialize_sensor(self, properties):
    return {}


def mocker_get_method_survey_time(method_name, *args, **kwargs):
    return 120


def mocker_check_weather(self, state, curr_date, site):
    return False


def mocker_check_weather_t(self, state, curr_date, site):
    return True


@pytest.fixture(name="simple_method_values")
def simple_method_values_fix(mocker):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "check_weather",
        mocker_check_weather,
    )
    properties: dict = {
        "n_crews": 5,
        "sensor": "default",
        "max_workday": 8,
        "consider_daylight": False,
        "weather_envs": {"wind": [0, 10], "temp": [-30, 30], "precip": [0, 1]},
    }
    current_date: date = date(2023, 1, 2)
    survey_plan: SurveyPlanner = SurveyPlanner(
        mocker,
        1,
        date(2023, 1, 1),
        date(2023, 12, 31),
        [2023],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    )
    state = {"weather": create_random_state(), "daylight": [], "t": []}
    survey_report = SiteSurveyReport(site_id=1)

    return (
        mocker,
        properties,
        current_date,
        survey_plan,
        state,
        survey_report,
    )


@pytest.fixture(name="simple_method_values2")
def simple_method_values2_fix(mocker):
    # Create a mock object for Site
    site_mock = mocker.Mock(spec=Site)
    site_mock.id = 1

    mocker.patch.object(site_mock, "get_method_survey_time", mocker_get_method_survey_time)
    mocker.patch.object(
        Method,
        "_initialize_sensor",
        mock_initialize_sensor,
    )

    mocker.patch.object(
        Method,
        "check_weather",
        mocker_check_weather_t,
    )
    properties: dict = {
        "n_crews": 5,
        "sensor": "default",
        "max_workday": 8,
        "consider_daylight": False,
        "weather_envs": {"wind": [0, 10], "temp": [-30, 30], "precip": [0, 1]},
    }
    current_date: date = date(2023, 1, 2)
    survey_plan: SurveyPlanner = SurveyPlanner(
        site_mock,
        1,
        date(2023, 1, 1),
        date(2023, 12, 31),
        [2023],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    )
    state = {"weather": create_random_state(), "daylight": [], "t": []}
    survey_report = SiteSurveyReport(site_id=1)

    return (
        mocker,
        properties,
        current_date,
        survey_plan,
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
