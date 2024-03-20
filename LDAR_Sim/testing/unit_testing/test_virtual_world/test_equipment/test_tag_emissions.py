"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_tag_emissions.py
Purpose: Testing for the Equipment class tag_emissions method.

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
from src.virtual_world.equipment import (
    Equipment,
    TaggingInfo,
    FugitiveEmission,
    NonRepairableEmission,
)


def mock_active_emissions(emis_count: int = 3):
    active_emissions = []
    for i in range(emis_count):
        active_emissions.append(FugitiveEmission())
    for i in range(emis_count):
        active_emissions.append(NonRepairableEmission())
    return active_emissions


def mock_tagging_info():
    return TaggingInfo(
        measured_rate=10,
        curr_date=date(2024, 1, 1),
        t_since_LDAR=5,
        company="Test Company",
        crew="Test Crew",
        report_delay=0,
    )


def mock_fugitive_emission_init(self, *args, **kwargs):
    self._tagged = False
    self._init_detect_by = None


def mock_non_rep_emission_init(self, *args, **kwargs):
    self._record = False
    self._init_detect_by = None


def mock_equipment_init(self, *args, **kwargs):
    self._active_emissions = kwargs["emissions"] if kwargs else []


def setup_mock_equipment(mocker):
    mocker.patch.object(FugitiveEmission, "__init__", mock_fugitive_emission_init)
    mocker.patch.object(NonRepairableEmission, "__init__", mock_non_rep_emission_init)
    mocker.patch.object(Equipment, "__init__", mock_equipment_init)


def test_tag_emissions_with_multiple_emissions(mocker):
    setup_mock_equipment(mocker)
    emissions = mock_active_emissions()
    mock_equipment = Equipment(emissions=emissions)
    tagging_info = mock_tagging_info()
    expected_rates = tagging_info.measured_rate / len(emissions)
    mock_equipment.tag_emissions(tagging_info=tagging_info)

    for emission in emissions:
        if isinstance(emission, FugitiveEmission):
            assert emission._tagged
            assert emission._tagged_by_company == "Test Company"
            assert emission._tagged_by_crew == "Test Crew"
            assert emission._measured_rate == expected_rates
        elif isinstance(emission, NonRepairableEmission):
            assert emission._record
            assert emission._recorded_by_company == "Test Company"
            assert emission._recorded_by_crew == "Test Crew"
            assert emission._measured_rate == expected_rates
