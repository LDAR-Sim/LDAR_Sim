"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_update.py
Purpose: Contains unit tests for testing the update function of emissions

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

from src.virtual_world.emissions import Emission
from src.file_processing.output_processing.output_utils import EmisInfo
from testing.unit_testing.test_virtual_world.test_emissions.emissions_testing_fixtures import (  # Noqa
    mock_simple_emission_1_fix,
)


def test_000_update_correctly_results_in_no_state_change_on_inactive_emission(
    mock_simple_emission_1: Emission,
):
    emis_info = EmisInfo(0, 0, 0, 0, 0)
    mock_simple_emission_1.update(emis_info)
    assert mock_simple_emission_1._active_days == 0
    assert emis_info == EmisInfo(0, 0, 0, 0, 0)


def test_000_update_correctly_results_in_active_days_change_on_active_emission(
    mock_simple_emission_1: Emission,
):
    emis_info = EmisInfo(0, 0, 0, 0, 0)
    mock_simple_emission_1._status = "Active"
    mock_simple_emission_1.update(emis_info)
    assert mock_simple_emission_1._active_days == 1
    assert emis_info == EmisInfo(0, 0, 0, 0, 0)


def test_000_update_correctly_results_in_days_since_tagged_change_if_tagged(
    mock_simple_emission_1: Emission,
):
    emis_info = EmisInfo(0, 0, 0, 0, 0)
    mock_simple_emission_1._tagged = True
    mock_simple_emission_1.update(emis_info)
    assert mock_simple_emission_1._active_days == 0
    assert emis_info == EmisInfo(0, 0, 0, 0, 0)
