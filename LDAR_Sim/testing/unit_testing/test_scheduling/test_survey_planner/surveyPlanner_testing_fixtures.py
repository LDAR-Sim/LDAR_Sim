"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        surveyPlanner_testing_fixtures
Purpose: To hold the fixtures used for testing survey planner functions

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
from src.virtual_world.sites import Site
from scheduling.scheduled_survey_planner import Survey_Counter


@pytest.fixture()
def mocker_fixture(mocker):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    return mocker


@pytest.fixture(name="gen_survey_plan_simple_case_1")
def gen_survey_plan_simple_case_1_fix():
    """Simple case for testing generate survey plan
        RS: 1
        Full deployment months
    Returns:
        RS
        Valid Months
        Result
    """
    RS: int = 1
    valid_months: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    expected_outcome: list[date] = [date(2023, 1, 1)]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_simple_case_3")
def gen_survey_plan_simple_case_3_fix():
    """Simple case for testing generate survey plan
    RS: 3
    Full deployment months
    """
    RS: int = 3
    valid_months: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    expected_outcome: list[date] = [date(2023, 1, 1), date(2023, 5, 2), date(2023, 8, 31)]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_simple_case_5")
def gen_survey_plan_simple_case_5_fix():
    """Simple case for testing generate survey plan
    RS: 5
    Full deployment months
    """
    RS: int = 5
    valid_months: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    expected_outcome: list[date] = [
        date(2023, 1, 1),
        date(2023, 3, 14),
        date(2023, 5, 26),
        date(2023, 8, 7),
        date(2023, 10, 19),
    ]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_simple_case_11")
def gen_survey_plan_simple_case_11_fix():
    """Simple case for testing generate survey plan
    RS: 11
    Full deployment months
    """
    RS: int = 11
    valid_months: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    expected_outcome: list[date] = [
        date(2023, 1, 1),
        date(2023, 2, 3),
        date(2023, 3, 8),
        date(2023, 4, 10),
        date(2023, 5, 13),
        date(2023, 6, 15),
        date(2023, 7, 18),
        date(2023, 8, 20),
        date(2023, 9, 22),
        date(2023, 10, 25),
        date(2023, 11, 27),
    ]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_simple_case_12")
def gen_survey_plan_simple_case_12_fix():
    """Simple case for testing generate survey plan
    RS: 12
    Full deployment months
    """
    RS: int = 12
    valid_months: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    expected_outcome: list[date] = [
        date(2023, 1, 1),
        date(2023, 1, 31),
        date(2023, 3, 2),
        date(2023, 4, 2),
        date(2023, 5, 2),
        date(2023, 6, 1),
        date(2023, 7, 2),
        date(2023, 8, 1),
        date(2023, 8, 31),
        date(2023, 10, 1),
        date(2023, 10, 31),
        date(2023, 11, 30),
    ]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_simple_split_2")
def gen_survey_plan_simple_split_2_fix():
    """Simple case for testing generate survey plan where months are split
    RS: 2
    Deployment_months: [5,8]
    """
    RS: int = 2
    valid_months: list[int] = [5, 8]
    expected_outcome: list[date] = [date(2023, 5, 1), date(2023, 5, 31)]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_split_2")
def gen_survey_plan_split_2_fix():
    """More complex case for testing generate survey plan where months are split
    RS: 2
    Deployment_months: [3,4,5,8,9,10]
    """
    RS: int = 2
    valid_months: list[int] = [3, 4, 5, 8, 9, 10]
    expected_outcome: list[date] = [date(2023, 3, 1), date(2023, 5, 31)]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_complex_4")
def gen_survey_plan_complex_4_fix():
    """Complex case for testing generate survey plan, with non-consecutive deployment months
    RS: 4
    Deployment_months: [2,4,6,8,10,11]
    """
    RS: int = 4
    valid_months: list[int] = [2, 4, 6, 8, 10, 11]
    expected_outcome: list[date] = [
        date(2023, 2, 1),
        date(2023, 4, 18),
        date(2023, 8, 2),
        date(2023, 10, 16),
    ]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_consecutive_2")
def gen_survey_plan_consecutive_2_fix():
    """Complex case for testing consecutive months
    RS: 2
    Deployment months: [4,5,6,7,8,9]"""
    RS: int = 2
    valid_months: list[int] = [4, 5, 6, 7, 8, 9]
    expected_outcome: list[date] = [
        date(2023, 4, 1),
        date(2023, 7, 1),
    ]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_consecutive_3")
def gen_survey_plan_consecutive_3_fix():
    """Complex case for testing consecutive months
    RS: 3
    Deployment months: [4,5,6,7,8,9]"""
    RS: int = 3
    valid_months: list[int] = [4, 5, 6, 7, 8, 9]
    expected_outcome: list[date] = [
        date(2023, 4, 1),
        date(2023, 5, 31),
        date(2023, 7, 31),
    ]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_split_4")
def gen_survey_plan_split_4_fix():
    """Simple case for testing generate survey plan
    RS: 4
    Deployment_months: [3, 4, 5, 8, 10, 11]
    """
    RS: int = 4
    valid_months: list[int] = [3, 4, 5, 9, 10, 11]
    expected_outcome: list[date] = [
        date(2023, 3, 1),
        date(2023, 4, 15),
        date(2023, 5, 31),
        date(2023, 10, 16),
    ]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_survey_plan_split_complex_2")
def gen_survey_plan_split_complex_2_fix():
    """Simple case for testing generate survey plan
    RS: 2
    Deployment_months: [1,2,3,10,11,12]
    """
    RS: int = 2
    valid_months: list[int] = [1, 2, 3, 10, 11, 12]
    expected_outcome: list[date] = [
        date(2023, 1, 1),
        date(2023, 10, 1),
    ]
    return RS, valid_months, expected_outcome


@pytest.fixture(name="gen_set_survey_per_year_tests_1")
def gen_set_survey_per_year_tests_1_fix():
    """Case where beginning years are missing"""
    valid_years: list[int] = [2024, 2025]
    start_year: date = date(2020, 1, 1)
    end_year: date = date(2025, 12, 31)
    surveys: int = 5
    expected_outcome: dict[int, Survey_Counter] = {
        2020: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2021: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2022: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2023: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2024: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2025: Survey_Counter(Required_surveys=5, Surveys_done=0),
    }
    return start_year, end_year, valid_years, surveys, expected_outcome


@pytest.fixture(name="gen_set_survey_per_year_tests_2")
def gen_set_survey_per_year_tests_2_fix():
    """Case where ending years are missing"""
    valid_years: list[int] = [2020, 2021, 2022]
    start_year: date = date(2020, 1, 1)
    end_year: date = date(2025, 12, 31)
    surveys: int = 5
    expected_outcome: dict[int, Survey_Counter] = {
        2020: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2021: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2022: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2023: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2024: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2025: Survey_Counter(Required_surveys=0, Surveys_done=0),
    }
    return start_year, end_year, valid_years, surveys, expected_outcome


@pytest.fixture(name="gen_set_survey_per_year_tests_3")
def gen_set_survey_per_year_tests_3_fix():
    """Case where the middle years are missing"""
    valid_years: list[int] = [2020, 2023, 2025]
    start_year: date = date(2020, 1, 1)
    end_year: date = date(2025, 12, 31)
    surveys: int = 5
    expected_outcome: dict[int, Survey_Counter] = {
        2020: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2021: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2022: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2023: Survey_Counter(Required_surveys=5, Surveys_done=0),
        2024: Survey_Counter(Required_surveys=0, Surveys_done=0),
        2025: Survey_Counter(Required_surveys=5, Surveys_done=0),
    }
    return start_year, end_year, valid_years, surveys, expected_outcome
