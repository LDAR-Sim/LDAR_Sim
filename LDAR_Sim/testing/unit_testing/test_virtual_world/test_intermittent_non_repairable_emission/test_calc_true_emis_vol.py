"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calc_true_emis_vol.py
Purpose: Contains unit tests for testing the calc_true_emis_vol method in the
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

import pytest
from virtual_world.emission_types.intermittent_non_repairable_emission import (
    IntermittentNonRepairableEmission,
)

from testing.unit_testing.test_virtual_world.test_intermittent_non_repairable_emission.intermittent_non_repairable_emission_creation_fixtures import (  # noqa
    intermittent_non_repairable_emission_creation_params_fixture,
)

from constants.general_const import Conversion_Constants as cc


@pytest.mark.parametrize(
    "emission_creation_params, emission_properties, expected_volume",
    [
        (
            "intermittent_non_repairable_emission_creation_params",
            {"active_days": 20, "days_emitting": 10},
            10.0 * cc.GRAMS_PER_SECOND_TO_KG_PER_DAY,
        ),
        (
            "intermittent_non_repairable_emission_creation_params",
            {"active_days": 20, "days_emitting": 20},
            20.0 * cc.GRAMS_PER_SECOND_TO_KG_PER_DAY,
        ),
        (
            "intermittent_non_repairable_emission_creation_params",
            {"active_days": 20, "days_emitting": 0},
            0.0,
        ),
    ],
)
def test_calc_true_emis_vol_return_expected_values_when_days_active_longer_than_days_emitting(
    emission_creation_params: str,
    emission_properties: dict,
    expected_volume: float,
    request: pytest.FixtureRequest,
):
    emission_creation_params_dict: dict = request.getfixturevalue(emission_creation_params)

    emission: IntermittentNonRepairableEmission = IntermittentNonRepairableEmission(
        **emission_creation_params_dict
    )

    for property, value in emission_properties.items():
        setattr(emission, f"_{property}", value)

    calculated_volume: float = emission.calc_true_emis_vol()
    assert calculated_volume == expected_volume
