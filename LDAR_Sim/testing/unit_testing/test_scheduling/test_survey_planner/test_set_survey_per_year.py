"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_set_survey_per_year
Purpose: Tests the function that initializes the dictionary used to hold data

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
from src.virtual_world.sites import Site
from scheduling.scheduled_survey_planner import ScheduledSurveyPlanner, Survey_Counter
from testing.unit_testing.test_scheduling.test_survey_planner.surveyPlanner_testing_fixtures import (
    mocker_fixture,
    gen_set_survey_per_year_tests_1_fix,
    gen_set_survey_per_year_tests_2_fix,
    gen_set_survey_per_year_tests_3_fix,
)


def test_000_set_survey_per_year_dictionary_simple(mocker):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    start_year, end_year = 2020, 2025
    deploy_years = list(range(start_year, end_year + 1))
    RS = 5
    deploy_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    planner = ScheduledSurveyPlanner(
        mocker,
        RS,
        date(start_year, 1, 1),
        date(end_year, 12, 31),
        deploy_years,
        deploy_months,
    )
    result = planner._surveys_this_year  # TODO: may need to make this an accessor instead..?
    expected: dict[int, Survey_Counter] = {
        2020: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2021: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2022: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2023: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2024: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2025: Survey_Counter(Required_surveys=5, Surveys_done=0),
    }
    assert result == expected


@pytest.mark.parametrize(
    "test_input, mocker_fix",
    [
        ("gen_set_survey_per_year_tests_1", "mocker_fixture"),
        ("gen_set_survey_per_year_tests_2", "mocker_fixture"),
        ("gen_set_survey_per_year_tests_3", "mocker_fixture"),
    ],
)
def test_000_set_not_full_deployment_year_surveys(test_input, mocker_fix, request):
    planner = ScheduledSurveyPlanner(
        request.getfixturevalue(mocker_fix),
        request.getfixturevalue(test_input)[3],
        request.getfixturevalue(test_input)[0],
        request.getfixturevalue(test_input)[1],
        request.getfixturevalue(test_input)[2],
        [1, 2, 3, 4, 5],
    )
    result = planner._surveys_this_year  # TODO: may need to make this an accessor instead..?
    assert result == request.getfixturevalue(test_input)[4]
