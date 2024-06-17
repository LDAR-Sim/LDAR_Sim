from datetime import date
from virtual_world.emission_types.repairable_emission import RepairableEmission
from src.constants.general_const import Emission_Constants as ec
from testing.unit_testing.test_virtual_world.test_repairable_emission.repairable_emission_testing_fixtures import (  # noqa
    mock_simple_fugitive_emission_for_activate_testing_1_fix,
)


def test_000_activate_returns_inactive_when_fugitive_emissions_start_date_not_yet_reached_and_status_inactive(  # noqa
    mock_simple_fugitive_emission_for_activate_testing_1: RepairableEmission,
):
    assert mock_simple_fugitive_emission_for_activate_testing_1._status == ec.INACTIVE
    assert (
        mock_simple_fugitive_emission_for_activate_testing_1.activate(date(*[2016, 1, 1])) is False
    )


def test_000_activate_returns_already_active_when_fugitive_emissions_status_active(
    mock_simple_fugitive_emission_for_activate_testing_1: RepairableEmission,
):
    mock_simple_fugitive_emission_for_activate_testing_1._status = ec.ACTIVE
    assert (
        mock_simple_fugitive_emission_for_activate_testing_1.activate(date(*[2017, 1, 1])) is False
    )


def test_000_activate_returns_newly_active_when_fugitive_emissions_start_date_passed_as_activate_date(  # noqa
    mock_simple_fugitive_emission_for_activate_testing_1: RepairableEmission,
):
    assert (
        mock_simple_fugitive_emission_for_activate_testing_1.activate(date(*[2018, 1, 1])) is True
    )
    assert mock_simple_fugitive_emission_for_activate_testing_1._status == ec.ACTIVE
