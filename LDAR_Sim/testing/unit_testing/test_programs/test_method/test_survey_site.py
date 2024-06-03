"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_survey_site
Purpose: Module for testing survey_site for Methods

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
from scheduling.schedule_dataclasses import SiteSurveyReport
from testing.unit_testing.test_programs.test_method.method_testing_fixtures import (  # noqa
    simple_method_values4_fix,
    simple_method_values5_fix,
)
from src.scheduling.schedule_dataclasses import CrewDailyReport
from src.virtual_world.infrastructure import Site


def test_000_simple_weather_fail_to_survey_site(simple_method_values4):
    (
        mocker,
        properties,
        current_date,
        state,
        survey_report,
    ) = simple_method_values4
    sites = [mocker.Mock(spec=Site) for i in range(5)]
    method = Method("test_method", properties, True, sites)
    daily_report = CrewDailyReport(1, 400)
    surveyed_report, travel_time, last_survey, site_visited = method.survey_site(
        daily_report, survey_report, sites[0], state, current_date
    )
    expected = survey_report
    assert surveyed_report == expected
    assert not last_survey
    assert travel_time == 0
    assert site_visited == 0


def test_000_simple_weather_fail_to_finish_site(simple_method_values5):
    (
        mocker,
        site_mock,
        properties,
        current_date,
        state,
        survey_report,
    ) = simple_method_values5
    sites = [mocker.Mock(spec=Site) for i in range(5)]
    method = Method("test_method", properties, True, sites)
    daily_report = CrewDailyReport(1, 10)
    surveyed_report, travel_time, last_survey, site_visited = method.survey_site(
        daily_report, survey_report, site_mock, state, current_date
    )
    expected = SiteSurveyReport(
        site_id=1,
        survey_in_progress=True,
        time_surveyed=8,
        time_spent_to_travel=1,
        survey_start_date=date(2023, 1, 2),
    )
    assert surveyed_report == expected
    assert last_survey
    assert travel_time == 1
    assert site_visited == 1


def test_000_simple_weather_finish_site(simple_method_values5):
    (
        mocker,
        site_mock,
        properties,
        current_date,
        state,
        survey_report,
    ) = simple_method_values5
    sites = [mocker.Mock(spec=Site) for i in range(5)]
    method = Method("test_method", properties, True, sites)
    daily_report = CrewDailyReport(1, 200)
    surveyed_report, travel_time, last_survey, site_visited = method.survey_site(
        daily_report, survey_report, site_mock, state, current_date
    )

    expected = SiteSurveyReport(
        site_id=1,
        survey_in_progress=False,
        time_surveyed=120,
        time_spent_to_travel=1,
        survey_level="site_level",
        site_measured_rate=1.0,
        site_true_rate=1,
        survey_complete=True,
        survey_start_date=date(2023, 1, 2),
        survey_completion_date=date(2023, 1, 2),
        method="test_method",
    )
    assert surveyed_report == expected
    assert not last_survey
    assert travel_time == 1
    assert site_visited == 1
