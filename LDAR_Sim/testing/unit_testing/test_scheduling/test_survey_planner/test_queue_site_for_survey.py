"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_queue_site_for_survey
Purpose: Unit test for testing the if the sites should be queued based on the survey plan

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
from scheduling.scheduled_survey_planner import ScheduledSurveyPlanner


def test_000_queue_site_for_survey_returns_true_first_survey(mocker):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    start_year, end_year = 2020, 2025
    deploy_years = list(range(start_year, end_year + 1))
    RS = 5
    deploy_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    planner = ScheduledSurveyPlanner(
        mocker,
        RS,
        date(start_year, 1, 1),
        date(end_year, 12, 31),
        deploy_years,
        deploy_months,
    )
    planner.update_date(date(2020, 1, 2))
    result = planner.queue_site_for_survey()
    assert result is True


def test_000_queue_site_for_survey_returns_false_when_site_it_has_yet_to_reach_survey_date(mocker):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    start_year, end_year = 2020, 2025
    deploy_years = list(range(start_year, end_year + 1))
    RS = 5
    deploy_months = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    planner = ScheduledSurveyPlanner(
        mocker,
        RS,
        date(start_year, 1, 1),
        date(end_year, 12, 31),
        deploy_years,
        deploy_months,
    )
    result = planner.queue_site_for_survey()
    assert result is False


def test_000_queue_site_for_survey_returns_false_when_site_is_not_due_to_be_queued_for_survey(
    mocker,
):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    start_year, end_year = 2020, 2023
    deploy_years = [2021, 2022, 2023]
    RS = 5
    deploy_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    planner = ScheduledSurveyPlanner(
        mocker,
        RS,
        date(start_year, 1, 1),
        date(end_year, 12, 31),
        deploy_years,
        deploy_months,
    )
    result = planner.queue_site_for_survey()
    assert result is False


# def test_000_queue_site_for_survey_returns_false_when_site_has_already_been_queued_for_survey():
#     return
# TODO : the above test should be done in the surveys not in survey Planner
