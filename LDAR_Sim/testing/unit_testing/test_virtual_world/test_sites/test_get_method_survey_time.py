"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_get_method_survey_time.py
Purpose: Unit test for testing the get_method_survey_time method in the Site class

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
from src.virtual_world.sites import Site
from virtual_world.equipment_groups import Equipment_Group


def mock_site_init(self, equipment_groups: int, survey_times: dict):
    equipment_group_survey_times: dict = {
        method: time / equipment_groups for method, time in survey_times.items()
    }

    self._equipment_groups = []
    for equipment_group in range(equipment_groups):
        self._equipment_groups.append(Equipment_Group(equipment_group_survey_times))


def mock_equipment_group_init(self, method_survey_times: dict):
    self._meth_survey_times = method_survey_times


@pytest.mark.parametrize(
    "equipment_groups, survey_times",
    [
        (3, {"method1": 10}),
        (3, {"method1": 10, "method2": 20}),
        (3, {"method1": 10, "method2": 20, "method3": 30}),
    ],
)
def test_000_get_method_survey_time_returns_expected_with_multiple_equipment(
    monkeypatch, equipment_groups: int, survey_times: dict
):
    monkeypatch.setattr(Site, "__init__", mock_site_init)

    monkeypatch.setattr(Equipment_Group, "__init__", mock_equipment_group_init)

    test_site: Site = Site(equipment_groups, survey_times)

    for method in survey_times.keys():
        assert test_site.get_method_survey_time(method) == survey_times[method]
        assert isinstance(test_site.get_method_survey_time(method), int)
