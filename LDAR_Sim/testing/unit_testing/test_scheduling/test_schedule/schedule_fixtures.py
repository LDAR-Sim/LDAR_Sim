"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        schedule_fixtures
Purpose: Contains the fixtures used to test schedules

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

from scheduling.generic_schedule import GenericSchedule


@pytest.fixture
def mocker_fixture(mocker):
    def mock_get_average_method_surveys_required(self, method_name, sites):
        return 5

    def mock_get_average_method_survey_time(self, method_name, avg_travel_time, sites):
        return 60

    mocker.patch.object(
        GenericSchedule,
        "get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        GenericSchedule, "get_average_method_survey_time", mock_get_average_method_survey_time
    )

    return mocker


@pytest.fixture
def mocker_fixture2(mocker):
    def mock_get_average_method_surveys_required(self, method_name, sites):
        return 5

    def mock_get_average_method_survey_time(self, method_name, avg_travel_time, sites):
        return 120

    mocker.patch.object(
        GenericSchedule,
        "get_average_method_surveys_required",
        mock_get_average_method_surveys_required,
    )
    mocker.patch.object(
        GenericSchedule, "get_average_method_survey_time", mock_get_average_method_survey_time
    )

    return mocker
