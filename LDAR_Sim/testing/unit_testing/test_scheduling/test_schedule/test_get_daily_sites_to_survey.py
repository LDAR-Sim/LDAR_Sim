"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_get_daily_sites_to_survey
Purpose: Contains unit tests to test the function that obtains daily sites to survey

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
from src.virtual_world.sites import Site
from src.scheduling.schedules import GenericSchedule
from testing.unit_testing.test_scheduling.test_schedule.schedule_fixtures import (
    mocker_fixture,
)


def test_000_get_daily_sites_to_survey_returns_expected_sites_for_survey(mocker_fixture):
    mocker = mocker_fixture

    # Set up mock data for the test
    method_follow_up = False
    methods_t_btw_sites = [60, 60, 60]
    method_max_work_hours = 8
    # Create a Mock object for Site with the required attributes
    site_mock = mocker.Mock(spec=Site)
    site_mock._survey_frequencies = {"test": 5}
    site_mock._deployment_years = {"test": [2020]}
    site_mock._deployment_months = {"test": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
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
    instance.update_schedule()
    result = instance.get_daily_sites_to_survey()
    expected = [sites[0]]
    assert expected == result


def test_000_get_daily_sites_to_survey_returns_expected_sites_for_survey2(mocker_fixture):
    mocker = mocker_fixture

    # Set up mock data for the test
    method_follow_up = False
    methods_t_btw_sites = [60, 60, 60]
    method_max_work_hours = 8
    # Create a Mock object for Site with the required attributes
    site_mock = mocker.Mock(spec=Site)
    site_mock._survey_frequencies = {"test": 5}
    site_mock._deployment_years = {"test": [2022]}
    site_mock._deployment_months = {"test": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}
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
    instance.update_schedule()
    result = instance.get_daily_sites_to_survey()
    expected = []
    assert expected == result
