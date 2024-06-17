"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_get_detectable_emissions.py
Purpose: Contains unit tests for testing the get_detectable_emissions method in the Component class.

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

from virtual_world import emission_types
from virtual_world.component import Component


def mock_component_initialization(
    self, active_emissions: list[emission_types.IntermittentRepairableEmission]
):
    self._active_emissions = active_emissions


def mock_emission_initialization(self, spatial_coverage: int, emitting: bool = True):
    self._status = "active"
    self._tech_spat_covs = {"test Spatial Coverage": spatial_coverage}
    self._emitting = emitting


def gen_mock_emissions() -> list[emission_types.Emission]:
    return [
        emission_types.IntermittentRepairableEmission(0, True),
        emission_types.IntermittentRepairableEmission(0, False),
        emission_types.IntermittentRepairableEmission(1, True),
        emission_types.IntermittentRepairableEmission(1, False),
        emission_types.IntermittentNonRepairableEmission(0, True),
        emission_types.IntermittentNonRepairableEmission(0, False),
        emission_types.IntermittentNonRepairableEmission(1, True),
        emission_types.IntermittentNonRepairableEmission(1, False),
    ]


def test_get_detectable_emissions_returns_only_detectable_intermittent_emissions(monkeypatch):
    monkeypatch.setattr(
        "virtual_world.component.Component.__init__",
        mock_component_initialization,
    )

    monkeypatch.setattr(
        (
            "virtual_world.emission_types.intermittent_repairable_emission"
            ".IntermittentRepairableEmission.__init__"
        ),
        mock_emission_initialization,
    )

    monkeypatch.setattr(
        (
            "virtual_world.emission_types.intermittent_non_repairable_emission"
            ".IntermittentNonRepairableEmission.__init__"
        ),
        mock_emission_initialization,
    )
    emissions_at_component: list[emission_types.Emission] = gen_mock_emissions()
    expected_indexes: list[int] = [2, 6]
    expected_detectable_emissions: list[emission_types.Emission] = [
        emissions_at_component[i] for i in expected_indexes
    ]
    test_component: Component = Component(emissions_at_component)

    detectable_emissions: list[emission_types.Emission] = test_component.get_detectable_emissions(
        "test"
    )

    assert detectable_emissions == expected_detectable_emissions
