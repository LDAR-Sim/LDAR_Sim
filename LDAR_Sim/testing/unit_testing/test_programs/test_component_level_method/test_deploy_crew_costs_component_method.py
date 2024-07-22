"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_deploy_crew_costs.py
Purpose: Unit test for testing the cost portion of crew deployment

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

from file_processing.output_processing.output_utils import CrewDeploymentStats
from src.programs.component_level_method import ComponentLevelMethod
from testing.unit_testing.test_programs.test_component_level_method.component_method_testing_fixtures import (  # noqa
    deploy_crews_testing3_fix,
    deploy_crews_testing4_fix,
    deploy_crews_testing5_fix,
    deploy_crews_testing6_fix,
)
from src.scheduling.workplan import Workplan


def test_000_simple_single_crew_daily_cost(deploy_crews_testing3):
    """
    This tests for the most simple case where there's a single site, and a single crew being
    deployed using the per day cost.
    """
    (sites, properties, weather, workplan, daylight, expected_deployment_stats) = (
        deploy_crews_testing3
    )
    workplan: Workplan
    method = ComponentLevelMethod("test_method", properties, True, sites, None)

    deploy_stats: CrewDeploymentStats = method.deploy_crews(workplan, weather, daylight)

    assert deploy_stats == expected_deployment_stats


def test_000_multi_site_single_crew_daily_cost(deploy_crews_testing4):
    """
    This tests for the case where there is a single crew deployed to multiple sites.
    4 mocked sites
    1 crews
    2 hour surveys
    9 hours total work time
    only one crew deployed on the given day
    """
    (sites, properties, weather, workplan, daylight, expected_deployment_stats) = (
        deploy_crews_testing4
    )
    workplan: Workplan
    method = ComponentLevelMethod("test_method", properties, True, sites, None)

    deploy_stats: CrewDeploymentStats = method.deploy_crews(workplan, weather, daylight)

    assert deploy_stats == expected_deployment_stats


def test_000_multi_site_crew_daily_cost(deploy_crews_testing5):
    """
    This tests for the case where there are multiple crews deployed to multiple sites.
    8 mocked sites
    2 crews
    2 hour surveys
    9 hours total work time
    both crews deployed on the given day.
    """
    (sites, properties, weather, workplan, daylight, expected_deployment_stats) = (
        deploy_crews_testing5
    )
    workplan: Workplan
    method = ComponentLevelMethod("test_method", properties, True, sites, None)

    deploy_stats: CrewDeploymentStats = method.deploy_crews(workplan, weather, daylight)

    assert deploy_stats == expected_deployment_stats


def test_000_multi_site_single_crew_required_daily_cost(deploy_crews_testing6):
    """
    This tests for the case where there are multiple crews deployed to multiple sites.
    3 mocked sites
    4 crews
    2 hour surveys
    9 hours total work time
    3 crews  out of 4 deployed.
    """
    (sites, properties, weather, workplan, daylight, expected_deployment_stats) = (
        deploy_crews_testing6
    )
    workplan: Workplan
    method = ComponentLevelMethod("test_method", properties, True, sites, None)

    deploy_stats: CrewDeploymentStats = method.deploy_crews(workplan, weather, daylight)

    assert deploy_stats == expected_deployment_stats
