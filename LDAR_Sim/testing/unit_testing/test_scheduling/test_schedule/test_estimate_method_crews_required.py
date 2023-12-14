"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_estimate_method_crews_required
Purpose: Unit test for testing the estimation of the number of crews required
for surveys

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
from src.scheduling.schedules import GenericSchedule
from src.virtual_world.sites import Site
from testing.unit_testing.test_scheduling.test_schedule.schedule_fixtures import (
    mocker_fixture,
    mocker_fixture2,
)


def test_000_return_estimate_not_followup_simple(mocker_fixture):
    mocker = mocker_fixture

    # Set up mock data for the test
    method_follow_up = False
    methods_t_btw_sites = [60, 60, 60]
    method_max_work_hours = 8
    # Create a Mock object for Site with the required attributes
    site_mock = mocker.Mock(spec=Site)
    site_mock._survey_frequencies = {"test": 5}
    site_mock._deployment_years = {"test": [2022]}
    site_mock._deployment_months = {"test": [1]}
    sites = [site_mock for _ in range(10)]

    instance = GenericSchedule(
        method_name="test",
        sites=sites,
        sim_start_date=date(2020, 1, 1),
        sim_end_date=date(2025, 12, 31),
        method_follow_up=method_follow_up,
        methods_t_btw_sites=methods_t_btw_sites,
        method_max_work_hours=method_max_work_hours,
    )
    expected_crews_required = 1
    assert instance._crews_for_method == expected_crews_required


def test_000_return_estimate_not_followup(mocker_fixture2):
    mocker = mocker_fixture2

    # Set up mock data for the test
    method_follow_up = False
    methods_t_btw_sites = [60, 60, 60]
    method_max_work_hours = 8
    # Create a Mock object for Site with the required attributes
    site_mock = mocker.Mock(spec=Site)
    site_mock._survey_frequencies = {"test": 5}
    site_mock._deployment_years = {"test": [2022]}
    site_mock._deployment_months = {"test": [1]}
    sites = [site_mock for _ in range(1050)]

    instance = GenericSchedule(
        method_name="test",
        sites=sites,
        sim_start_date=date(2020, 1, 1),
        sim_end_date=date(2025, 12, 31),
        method_follow_up=method_follow_up,
        methods_t_btw_sites=methods_t_btw_sites,
        method_max_work_hours=method_max_work_hours,
    )
    expected_crews_required = 5
    assert instance._crews_for_method == expected_crews_required


def test_000_return_estimate_1_if_followup(mocker_fixture):
    mocker = mocker_fixture

    # Set up mock data for the test
    method_follow_up = True
    methods_t_btw_sites = []
    method_max_work_hours = 8
    sites = [mocker.Mock(spec=Site) for x in range(10)]

    crews_required = GenericSchedule._estimate_method_crews_required(
        GenericSchedule, method_follow_up, methods_t_btw_sites, method_max_work_hours, sites
    )

    expected_crews_required = 1
    assert crews_required == expected_crews_required
