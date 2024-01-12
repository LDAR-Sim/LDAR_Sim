"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_get_simulation_years
Purpose: Unit test for getting the simulation years

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
from typing import Tuple
from datetime import date
from hypothesis import given, strategies as st, settings, HealthCheck
from scheduling.scheduled_survey_planner import ScheduledSurveyPlanner
from src.virtual_world.sites import Site
from testing.unit_testing.test_scheduling.test_survey_planner.surveyPlanner_testing_fixtures import (
    mocker_fixture,
)


@st.composite
def generate_date_range(draw):
    """hypothesis strategy for generating date objects"""
    start_year = draw(st.integers(min_value=1980, max_value=2040))
    end_year = draw(st.integers(min_value=start_year, max_value=2040))

    start_month = draw(st.integers(min_value=1, max_value=12))
    end_month = draw(st.integers(min_value=start_month, max_value=12))

    start_day = draw(st.integers(min_value=1, max_value=28))
    end_day = draw(st.integers(min_value=start_day, max_value=28))

    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)

    return start_date, end_date, start_year, end_year


@given(date_range=generate_date_range())
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])  # TODO: move later
def test_000_get_simulation_years(date_range: Tuple[date, date, int, int], mocker_fixture):
    start_date, end_date, start_year, end_year = date_range

    # Use the mocker fixture from the mocker_fixture parameter
    mocker = mocker_fixture

    # Your existing test code here
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    mocker.patch.object(ScheduledSurveyPlanner, "_gen_survey_plan", return_value=[date(2023, 1, 1)])
    deploy_years = list(range(start_year, end_year + 1))
    deploy_months = list(range(1, 13))
    planner = ScheduledSurveyPlanner(mocker, 1, start_date, end_date, deploy_years, deploy_months)
    result = planner._get_simulation_years(start_date, end_date)

    # Ensure that the result is a list of integers
    assert isinstance(result, list)
    assert all(isinstance(year, int) for year in result)

    # Ensure that the mocked values are returned
    assert result == deploy_years


# def test_000_get_simulation_years_throws_exceptions_on_invalid_inputs():
#     return
