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
from src.scheduling.generic_schedule import GenericSchedule
from src.scheduling.workplan import Workplan


def test_000_get_daily_sites_to_survey_returns_expected_sites_for_survey(mocker):
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
        est_meth_daily_surveys=5,
        method_avail_crews=1,
    )
    result = instance.get_workplan(date(2020, 1, 1))
    expected = Workplan(instance._survey_plans[:8], date(2020, 1, 1))
    assert expected.date == result.date
    assert expected.site_survey_planners == result.site_survey_planners


def test_000_get_daily_sites_to_survey_returns_expected_sites_for_survey2(
    mocker,
):
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
        est_meth_daily_surveys=5,
        method_avail_crews=1,
    )
    instance.get_workplan(date(2020, 1, 1))
    result = instance.get_daily_sites_to_survey()
    expected = []
    assert expected == result
