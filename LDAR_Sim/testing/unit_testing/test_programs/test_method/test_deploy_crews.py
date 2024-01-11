"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_deploy_crews
Purpose: Unit test for testing the deployment of crews

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
from src.programs.method import Method
from src.virtual_world.sites import Site
from testing.unit_testing.test_programs.test_method.method_testing_fixtures import (
    deploy_crews_testing_fix,
    deploy_crews_testing2_fix,
)
from src.scheduling.schedule_dataclasses import (
    SiteSurveyReport,
    CrewDailyReport,
)


def test_000_test_initialization_of_crews(
    deploy_crews_testing,
):
    (sites, properties, state, workplan) = deploy_crews_testing
    method = Method("test_method", properties, True, sites)
    assert len(method._crew_reports) == 1
    assert isinstance(method._crew_reports[0], CrewDailyReport)
    assert method._crew_reports[0].day_time_remaining == 0


def test_000_simple_deployment_of_crews_no_crews_deployed_no_valid_sites(
    deploy_crews_testing,
):
    (sites, properties, state, workplan) = deploy_crews_testing
    method = Method("test_method", properties, True, sites)
    method.deploy_crews(workplan, state)
    assert isinstance(method._crew_reports[0], CrewDailyReport)
    assert method._crew_reports[0].day_time_remaining == 8
    expected = SiteSurveyReport(1)
    assert workplan._site_survey_reports[1] == expected


def test_000_simple_deployment_of_crews_work_a_day(deploy_crews_testing2):
    (sites, properties, state, workplan) = deploy_crews_testing2
    method = Method("test_method", properties, True, sites)
    assert workplan._site_survey_reports == {}
    assert len(workplan.site_survey_planners) == 1
    method.deploy_crews(workplan, state)
    expected = SiteSurveyReport(
        1,
        120,
        1,
        True,
        False,
        [],
        "Site_level",
        1.0,
        1.0,
        False,
        date(2023, 1, 1),
        date(2023, 1, 1),
        "test_method",
    )
    assert isinstance(method._crew_reports[0], CrewDailyReport)
    assert method._crew_reports[0].day_time_remaining == 0
    assert len(workplan._site_survey_reports) == 1
    assert len(workplan.site_survey_planners) == 1
    assert workplan._site_survey_reports[1] == expected
