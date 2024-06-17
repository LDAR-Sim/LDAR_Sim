"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_update.py
Purpose: Contains unit tests for testing the update method in the
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

from testing.unit_testing.test_virtual_world.test_intermittent_repairable_emission.intermittent_repairable_emission_creation_fixtures import (  # noqa
    intermittent_repairable_emission_creation_params_fixture,
)
from virtual_world.emission_types.intermittent_repairable_emission import (
    IntermittentRepairableEmission,
)

from file_processing.output_processing.output_utils import EmisInfo


def test_update_correctly_changes_emitting_state_when_on_emitting_to_non_emitting_boundary(
    intermittent_repairable_emission_creation_params,
):
    emission_info: EmisInfo = EmisInfo()
    emission: IntermittentRepairableEmission = IntermittentRepairableEmission(
        **intermittent_repairable_emission_creation_params
    )
    emission.activate(emission._start_date)

    emission_active_duration: int = intermittent_repairable_emission_creation_params[
        "active_duration"
    ]

    for _ in range(emission_active_duration + 1):
        emission.update(emission_info)

    assert emission._emitting is False
    assert emission._days_emitting == emission_active_duration
    assert emission._emitting_period_day_count == 0
    assert emission._non_emitting_period_day_count == 1


def test_update_correctly_changes_emitting_state_when_on_non_emitting_to_emitting_boundary(
    intermittent_repairable_emission_creation_params,
):
    emission_info: EmisInfo = EmisInfo()
    emission: IntermittentRepairableEmission = IntermittentRepairableEmission(
        **intermittent_repairable_emission_creation_params
    )
    emission.activate(emission._start_date)
    emission._emitting = False

    emission_inactive_duration: int = intermittent_repairable_emission_creation_params[
        "inactive_duration"
    ]

    for _ in range(emission_inactive_duration + 1):
        emission.update(emission_info)

    assert emission._emitting is True
    assert emission._days_emitting == 1
    assert emission._emitting_period_day_count == 1
    assert emission._non_emitting_period_day_count == 0


def test_update_correctly_results_in_no_change_to_emitting_state_when_not_on_boundary_and_emitting(
    intermittent_repairable_emission_creation_params,
):
    emission_info: EmisInfo = EmisInfo()
    emission: IntermittentRepairableEmission = IntermittentRepairableEmission(
        **intermittent_repairable_emission_creation_params
    )
    emission.activate(emission._start_date)

    emission_active_duration: int = intermittent_repairable_emission_creation_params[
        "active_duration"
    ]

    for _ in range(emission_active_duration - 1):
        emission.update(emission_info)

    assert emission._emitting is True
    assert emission._days_emitting == emission_active_duration - 1
    assert emission._emitting_period_day_count == emission_active_duration - 1
    assert emission._non_emitting_period_day_count == 0


def test_update_correctly_results_in_no_change_to_emitting_state_when_not_on_boundary_and_not_emitting(  # noqa
    intermittent_repairable_emission_creation_params,
):
    emission_info: EmisInfo = EmisInfo()
    emission: IntermittentRepairableEmission = IntermittentRepairableEmission(
        **intermittent_repairable_emission_creation_params
    )
    emission.activate(emission._start_date)
    emission._emitting = False

    emission_inactive_duration: int = intermittent_repairable_emission_creation_params[
        "inactive_duration"
    ]

    for _ in range(emission_inactive_duration - 1):
        emission.update(emission_info)

    assert emission._emitting is False
    assert emission._days_emitting == 0
    assert emission._emitting_period_day_count == 0
    assert emission._non_emitting_period_day_count == emission_inactive_duration - 1
