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
from file_processing.output_processing.output_utils import CrewDeploymentStats
from src.programs.method import Method
from testing.unit_testing.test_programs.test_method.method_testing_fixtures import (  # noqa
    deploy_crews_testing_fix,
    deploy_crews_testing2_fix,
)
from scheduling.schedule_dataclasses import (
    SiteSurveyReport,
    CrewDailyReport,
)
from src.scheduling.workplan import Workplan


def test_000_test_initialization_of_crews(
    deploy_crews_testing,
):
    (sites, properties, weather, workplan, daylight) = deploy_crews_testing
    method = Method("test_method", properties, True, sites, None)
    assert len(method._crew_reports) == 1
    assert isinstance(method._crew_reports[0], CrewDailyReport)
    assert method._crew_reports[0].day_time_remaining == 0


def test_000_simple_deployment_of_crews_no_crews_deployed_no_valid_sites(
    deploy_crews_testing,
):
    (sites, properties, weather, workplan, daylight) = deploy_crews_testing
    workplan: Workplan
    method = Method("test_method", properties, True, sites, None)
    method.deploy_crews(workplan, weather, daylight)
    assert isinstance(method._crew_reports[0], CrewDailyReport)
    assert method._crew_reports[0].day_time_remaining == 8 * 60
    expected = SiteSurveyReport(1)
    assert workplan._site_survey_reports[1] == expected


def test_000_simple_deployment_of_crews_work_a_day(deploy_crews_testing2):
    (sites, properties, weather, workplan, daylight) = deploy_crews_testing2
    workplan: Workplan
    method = Method("test_method", properties, True, sites, None)
    assert workplan._site_survey_reports == {}
    assert len(workplan.site_survey_planners) == 1
    deploy_stats: CrewDeploymentStats = method.deploy_crews(workplan, weather, daylight)
    expected = SiteSurveyReport(
        site_id=1,
        time_surveyed=120,
        time_surveyed_current_day=120,
        time_spent_to_travel=1,
        survey_complete=True,
        survey_in_progress=False,
        equipment_groups_surveyed=[],
        survey_level="Site_level",
        site_measured_rate=1.0,
        site_true_rate=1.0,
        site_flagged=False,
        survey_completion_date=date(2023, 1, 1),
        survey_start_date=date(2023, 1, 1),
        method="test_method",
    )
    expected_deployment_stats = CrewDeploymentStats(500.0, 1, 2, 120)
    assert isinstance(method._crew_reports[0], CrewDailyReport)
    assert method._crew_reports[0].day_time_remaining == 0
    assert len(workplan._site_survey_reports) == 1
    assert len(workplan.site_survey_planners) == 1
    assert workplan._site_survey_reports[1] == expected
    assert deploy_stats == expected_deployment_stats
