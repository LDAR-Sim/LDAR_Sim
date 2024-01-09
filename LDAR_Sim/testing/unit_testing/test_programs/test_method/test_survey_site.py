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

from src.programs.method import Method
from src.scheduling.schedule_dataclasses import SiteSurveyReport
from testing.unit_testing.test_programs.test_method.method_testing_fixtures import (  # noqa
    simple_method_values_fix,
    simple_method_values2_fix,
)
from src.scheduling.workplan import CrewDailyReport


def test_000_simple_weather_fail_to_survey_site(simple_method_values):
    mocker, properties, current_date, survey_plan, state, survey_report = simple_method_values
    method = Method("test_method", properties, True)
    daily_report = CrewDailyReport(1, 400)
    surveyed_report, crew_report = method.survey_site(
        daily_report, survey_plan, survey_report, state, current_date
    )
    expected = survey_report
    assert surveyed_report == expected
    assert crew_report == daily_report


def test_000_simple_weather_fail_to_finish_site(simple_method_values2):
    mocker, properties, current_date, survey_plan, state, survey_report = simple_method_values2
    method = Method("test_method", properties, True)
    daily_report = CrewDailyReport(1, 10)
    surveyed_report, crew_report = method.survey_site(
        daily_report, survey_plan, survey_report, state, current_date
    )
    expected = SiteSurveyReport(site_id=1, survey_in_progress=True, time_surveyed=10)
    assert surveyed_report == expected
    assert crew_report == CrewDailyReport(1, 0)


def test_000_simple_weather_finish_site(simple_method_values2):
    mocker, properties, current_date, survey_plan, state, survey_report = simple_method_values2
    method = Method("test_method", properties, True)
    daily_report = CrewDailyReport(1, 200)
    surveyed_report, crew_report = method.survey_site(
        daily_report, survey_plan, survey_report, state, current_date
    )

    expected = SiteSurveyReport(
        site_id=1, survey_in_progress=False, time_surveyed=120, survey_complete=True
    )
    assert surveyed_report == expected
    assert crew_report == CrewDailyReport(1, 80)
