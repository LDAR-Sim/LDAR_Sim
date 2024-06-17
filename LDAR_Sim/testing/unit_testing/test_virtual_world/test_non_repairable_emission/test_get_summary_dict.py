"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_get_summary_dict.py
Purpose: Testing for the NonRepairableEmission class get_summary_dict method.

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

from typing import Any, Tuple
from datetime import date
from testing.unit_testing.test_virtual_world.test_non_repairable_emission.non_repairable_emission_testing_fixtures import (  # noqa
    mock_simple_emission_for_get_summary_dict_1_fix,
)
from virtual_world.emission_types.non_repairable_emissions import NonRepairableEmission


def test_000_get_summary_dict_fe_returns_expected_values_for_simple_case(
    mock_simple_emission_for_get_summary_dict: Tuple[date, NonRepairableEmission, dict[str, int]]
) -> None:
    end_date, emission, expected_result = mock_simple_emission_for_get_summary_dict
    summary_dict: dict[str, Any] = emission.get_summary_dict(end_date)
    assert summary_dict == expected_result
