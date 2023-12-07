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
from datetime import date
from src.scheduling.survey_planner import SurveyPlanner
from src.virtual_world.sites import Site
from testing.unit_testing.test_scheduling.test_survey_planner.surveyPlanner_testing_fixtures import (
    gen_survey_plan_simple_case_1_fix,
    gen_survey_plan_simple_case_3_fix,
    gen_survey_plan_simple_case_5_fix,
    gen_survey_plan_simple_case_11_fix,
    gen_survey_plan_simple_case_12_fix,
    gen_survey_plan_split_2_fix,
    gen_survey_plan_complex_2_fix,
    gen_survey_plan_complex_4_fix,
    gen_survey_plan_split_complex_4_fix,
)


def test_000_gen_survey_plan_gens_logical_survey_plans_with_full_deployment_months(
    gen_survey_plan_simple_case_1,
    gen_survey_plan_simple_case_3,
    gen_survey_plan_simple_case_5,
    gen_survey_plan_simple_case_11,
    gen_survey_plan_simple_case_12,
    mocker,
):
    fixtures = [
        gen_survey_plan_simple_case_1,
        gen_survey_plan_simple_case_3,
        gen_survey_plan_simple_case_5,
        gen_survey_plan_simple_case_11,
        gen_survey_plan_simple_case_12,
    ]
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    start_year, end_year = 2020, 2025
    deploy_years = list(range(start_year, end_year + 1))

    for fixture in fixtures:
        deploy_months = fixture[1]
        planner = SurveyPlanner(
            mocker,
            fixture[0],
            date(start_year, 1, 1),
            date(end_year, 12, 31),
            deploy_years,
            deploy_months,
        )
        result = planner.get_survey_plan()
        assert result == fixture[2]


def test_000_gen_survey_plans_gens_logical_survey_plans_with_partial_deployment_months(
    gen_survey_plan_split_2, gen_survey_plan_complex_2, mocker
):
    fixtures = [
        gen_survey_plan_split_2,
        gen_survey_plan_complex_2,
    ]
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    start_year, end_year = 2020, 2025
    deploy_years = list(range(start_year, end_year + 1))
    for fixture in fixtures:
        deploy_months = fixture[1]
        planner = SurveyPlanner(
            mocker,
            fixture[0],
            date(start_year, 1, 1),
            date(end_year, 12, 31),
            deploy_years,
            deploy_months,
        )
        result = planner.get_survey_plan()
        assert result == fixture[2]


def test_000_gen_survey_plans_gens_logical_survey_plans_with_partial_deployment_months_complex(
    gen_survey_plan_split_complex_4, gen_survey_plan_complex_4, mocker
):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    start_year = 2020
    end_year = 2025
    deploy_years = list(range(start_year, end_year + 1))
    deploy_months = gen_survey_plan_split_complex_4[1]
    planner = SurveyPlanner(
        mocker,
        gen_survey_plan_split_complex_4[0],
        date(2020, 1, 1),
        date(2025, 12, 31),
        deploy_years,
        deploy_months,
    )
    result = planner.get_survey_plan()
    assert result == gen_survey_plan_split_complex_4[2]
