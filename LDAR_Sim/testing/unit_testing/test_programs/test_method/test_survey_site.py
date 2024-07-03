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

import pytest
from pytest_mock import MockerFixture
from constants import param_default_const as pdc
from scheduling.schedule_dataclasses import SiteSurveyReport
from src.programs.method import Method
from src.scheduling.schedule_dataclasses import CrewDailyReport
from src.virtual_world.infrastructure import Site
from testing.unit_testing.test_programs.test_method.method_testing_fixtures import (  # noqa
    simple_method_values4_fix,
    simple_method_values5_fix,
)
from testing.unit_testing.test_programs.test_method.survey_site_testing_resources import (
    setup_mock_objects_for_survey_report_testing,
)


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
        time_surveyed_current_day=8,
        time_spent_to_travel=1,
        survey_start_date=date(2023, 1, 2),
        method="test_method",
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
        time_surveyed_current_day=120,
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


@pytest.mark.parametrize(
    "site_properties, method_properties, existing_survey_report, crew_time, expected_survey_report",
    [
        (
            {"_id": 1, pdc.Method_Params.TIME: 120},
            {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
            SiteSurveyReport(site_id=1),
            180,
            SiteSurveyReport(
                site_id=1,
                time_surveyed=120,
                survey_in_progress=False,
                time_surveyed_current_day=120,
                survey_complete=True,
                time_spent_to_travel=30,
                method="test_method",
                survey_start_date=date(2023, 1, 1),
                survey_completion_date=date(2023, 1, 1),
            ),
        ),
        (
            {"_id": 1, pdc.Method_Params.TIME: 200},
            {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
            SiteSurveyReport(site_id=1),
            180,
            SiteSurveyReport(
                site_id=1,
                time_surveyed=120,
                survey_in_progress=True,
                time_surveyed_current_day=120,
                survey_complete=False,
                time_spent_to_travel=30,
                method="test_method",
                survey_start_date=date(2023, 1, 1),
                survey_completion_date=None,
            ),
        ),
        (
            {"_id": 1, pdc.Method_Params.TIME: 120},
            {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
            SiteSurveyReport(
                site_id=1,
                time_surveyed=60,
                time_surveyed_current_day=60,
                time_spent_to_travel=30,
                survey_in_progress=True,
                method="test_method",
                survey_start_date=date(2022, 1, 1),
            ),
            180,
            SiteSurveyReport(
                site_id=1,
                time_surveyed=120,
                survey_in_progress=False,
                time_surveyed_current_day=60,
                survey_complete=True,
                time_spent_to_travel=60,
                method="test_method",
                survey_start_date=date(2022, 1, 1),
                survey_completion_date=date(2023, 1, 1),
            ),
        ),
        (
            {"_id": 1, pdc.Method_Params.TIME: 120},
            {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
            SiteSurveyReport(
                site_id=1,
                survey_start_date=date(2022, 12, 1),
                time_surveyed=60,
                time_surveyed_current_day=30,
                time_spent_to_travel=30,
                survey_in_progress=True,
                method="test_method",
            ),
            90,
            SiteSurveyReport(
                site_id=1,
                time_surveyed=90,
                survey_in_progress=True,
                time_surveyed_current_day=30,
                survey_complete=False,
                time_spent_to_travel=60,
                method="test_method",
                survey_start_date=date(2022, 12, 1),
                survey_completion_date=None,
            ),
        ),
        (
            {"_id": 1, pdc.Method_Params.TIME: 120},
            {pdc.Method_Params.DEPLOYMENT_TYPE: "mobile", "travel_times": 30},
            SiteSurveyReport(
                site_id=1,
                survey_start_date=date(2022, 12, 1),
                time_surveyed=60,
                time_surveyed_current_day=30,
                time_spent_to_travel=30,
                survey_in_progress=True,
                method="test_method",
            ),
            60,
            SiteSurveyReport(
                site_id=1,
                time_surveyed=60,
                survey_in_progress=True,
                time_surveyed_current_day=0,
                survey_complete=False,
                time_spent_to_travel=0,
                method="test_method",
                survey_start_date=date(2022, 12, 1),
                survey_completion_date=None,
            ),
        ),
    ],
)
def test_000_survey_site_correctly_updates_survey_report(
    mocker: MockerFixture,
    site_properties,
    method_properties,
    existing_survey_report,
    crew_time,
    expected_survey_report,
):
    mock_site, method, daily_report = setup_mock_objects_for_survey_report_testing(
        mocker, site_properties, method_properties, crew_time
    )

    survey_report: SiteSurveyReport = method.survey_site(
        daily_report,
        existing_survey_report,
        mock_site,
        mocker.Mock(),
        date(2023, 1, 1),
    )[0]

    assert survey_report == expected_survey_report
