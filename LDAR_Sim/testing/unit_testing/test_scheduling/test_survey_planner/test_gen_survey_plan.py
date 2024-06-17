"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_gen_survey_plan
Purpose: Unit test for generating survey plans

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
from scheduling.scheduled_survey_planner import ScheduledSurveyPlanner
from testing.unit_testing.test_scheduling.test_survey_planner.surveyPlanner_testing_fixtures import (
    gen_survey_plan_simple_case_1_fix,
    gen_survey_plan_simple_case_3_fix,
    gen_survey_plan_simple_case_5_fix,
    gen_survey_plan_simple_case_11_fix,
    gen_survey_plan_simple_case_12_fix,
    gen_survey_plan_split_2_fix,
    gen_survey_plan_complex_4_fix,
    gen_survey_plan_consecutive_2_fix,
    gen_survey_plan_consecutive_3_fix,
    gen_survey_plan_simple_split_2_fix,
    gen_survey_plan_split_4_fix,
    gen_survey_plan_split_complex_2_fix,
    mocker_fixture,
)


@pytest.mark.parametrize(
    "test_input, mocker_fix",
    [
        ("gen_survey_plan_simple_case_1", "mocker_fixture"),
        ("gen_survey_plan_simple_case_3", "mocker_fixture"),
        ("gen_survey_plan_simple_case_5", "mocker_fixture"),
        ("gen_survey_plan_simple_case_11", "mocker_fixture"),
        ("gen_survey_plan_simple_case_12", "mocker_fixture"),
    ],
)
def test_000_gen_survey_plan_gens_logical_survey_plans_with_full_deployment_months(
    test_input, mocker_fix, request
):
    """Unit test for testing simple deployment for scheduling"""
    start_year, end_year = 2020, 2025
    deploy_years = list(range(start_year, end_year + 1))
    deploy_months = request.getfixturevalue(test_input)[1]
    planner = ScheduledSurveyPlanner(
        request.getfixturevalue(mocker_fix),
        request.getfixturevalue(test_input)[0],
        date(start_year, 1, 1),
        date(end_year, 12, 31),
        deploy_years,
        deploy_months,
    )
    result = planner.get_survey_plan()
    assert result == request.getfixturevalue(test_input)[2]


@pytest.mark.parametrize(
    "test_input, mocker_fix",
    [
        ("gen_survey_plan_split_2", "mocker_fixture"),
        ("gen_survey_plan_complex_4", "mocker_fixture"),
        ("gen_survey_plan_consecutive_2", "mocker_fixture"),
        ("gen_survey_plan_consecutive_3", "mocker_fixture"),
        ("gen_survey_plan_simple_split_2", "mocker_fixture"),
        ("gen_survey_plan_split_4", "mocker_fixture"),
        ("gen_survey_plan_split_complex_2", "mocker_fixture"),
    ],
)
def test_000_gen_survey_plans_gens_logical_survey_plans_with_partial_deployment_months(
    test_input, mocker_fix, request
):
    """Unit test for testing more complex deployment for scheduling"""
    start_year, end_year = 2020, 2025
    deploy_years = list(range(start_year, end_year + 1))
    deploy_months = request.getfixturevalue(test_input)[1]
    planner = ScheduledSurveyPlanner(
        request.getfixturevalue(mocker_fix),
        request.getfixturevalue(test_input)[0],
        date(start_year, 1, 1),
        date(end_year, 12, 31),
        deploy_years,
        deploy_months,
    )
    result = planner.get_survey_plan()
    assert result == request.getfixturevalue(test_input)[2]
