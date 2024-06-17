"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_get_summary_dict.py
Purpose: Contains unit tests for testing the get_summary_dict method in the
         IntermittentRepairableEmission class.

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
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca
from constants.general_const import Conversion_Constants as cc
from testing.unit_testing.test_virtual_world.test_intermittent_repairable_emission.intermittent_repairable_emission_creation_fixtures import (  # noqa
    intermittent_repairable_emission_creation_params_fixture,
)
from virtual_world.emission_types.intermittent_repairable_emission import (
    IntermittentRepairableEmission,
)


def test_get_summary_dict_returns_expected_true_emissions_volume(
    intermittent_repairable_emission_creation_params: str,
):
    emissions_properties: dict = {"active_days": 20, "days_emitting": 10}
    expected_volume_emitted: float = 10.0 * cc.GRAMS_PER_SECOND_TO_KG_PER_DAY
    end_date: date = date(2024, 1, 31)

    emission: IntermittentRepairableEmission = IntermittentRepairableEmission(
        **intermittent_repairable_emission_creation_params
    )

    for property, value in emissions_properties.items():
        setattr(emission, f"_{property}", value)

    summary_dict: dict = emission.get_summary_dict(end_date=end_date)

    assert summary_dict[eca.T_VOL_EMIT] == expected_volume_emitted
