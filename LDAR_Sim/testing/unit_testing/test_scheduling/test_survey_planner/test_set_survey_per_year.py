"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_set_survey_per_year
Purpose: Tests the function that initializes the dictionary used to hold data

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
from src.scheduling.survey_planner import SurveyPlanner


def test_000_set_survey_per_year_dictionary(mocker):
    mocker.patch.object(Site, "__init__", lambda self, *args, **kwargs: setattr(self, "id", 1))
    start_year, end_year = 2020, 2025
    deploy_years = list(range(start_year, end_year + 1))
    RS = 5
    deploy_months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    planner = SurveyPlanner(
        mocker,
        RS,
        date(start_year, 1, 1),
        date(end_year, 12, 31),
        deploy_years,
        deploy_months,
    )
    result = planner._surveys_this_year  # TODO: may need to make this an accessor instead..?
    expected: dict[int, list[int]] = {
        2020: [5, 0],
        2021: [5, 0],
        2022: [5, 0],
        2023: [5, 0],
        2024: [5, 0],
        2025: [5, 0],
    }
    assert result == expected
