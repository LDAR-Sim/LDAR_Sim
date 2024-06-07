"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_activate.py
Purpose: Contains unit tests for testing the activate method in the
         IntermittentNonRepairableEmission class.

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

from testing.unit_testing.test_virtual_world.test_intermittent_non_repairable_emission.intermittent_non_repairable_emission_creation_fixtures import (  # noqa
    intermittent_non_repairable_emission_creation_params_fixture,
)
from virtual_world.emission_types.intermittent_non_repairable_emission import (
    IntermittentNonRepairableEmission,
)


def test_activate_correctly_sets_emitting_true_if_emission_activated(
    intermittent_non_repairable_emission_creation_params,
):
    emission: IntermittentNonRepairableEmission = IntermittentNonRepairableEmission(
        **intermittent_non_repairable_emission_creation_params
    )

    activate_date: date = date(2024, 1, 1)

    emission.activate(activate_date)

    assert emission._emitting is True
