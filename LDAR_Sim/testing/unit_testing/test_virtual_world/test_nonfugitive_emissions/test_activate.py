from datetime import date
from src.virtual_world.nonfugitive_emissions import NonRepairableEmission

from testing.unit_testing.test_virtual_world.test_nonfugitive_emissions.nonfugitive_emission_testing_fixtures import (  # noqa
    mock_simple_nonfugitive_emission_for_activate_testing_1_fix,
)


def test_000_activate_returns_inactive_when_nonfugitive_emissions_start_date_not_yet_reached_and_status_inactive(  # noqa
    mock_simple_nonfugitive_emission_for_activate_testing_1: NonRepairableEmission,
):
    mock_simple_nonfugitive_emission_for_activate_testing_1.activate(date(*[2017, 1, 1]))
    assert (
        mock_simple_nonfugitive_emission_for_activate_testing_1._status
        == "Inactive"
    )


def test_000_activate_returns_already_active_when_nonfugitive_emissions_status_active(
    mock_simple_nonfugitive_emission_for_activate_testing_1: NonRepairableEmission,
):
    mock_simple_nonfugitive_emission_for_activate_testing_1._status = "Active"
    mock_simple_nonfugitive_emission_for_activate_testing_1.activate(date(*[2017, 1, 1]))
    assert (
        mock_simple_nonfugitive_emission_for_activate_testing_1._status == "Active"
    )


def test_000_activate_returns_newly_active_when_nonfugitive_emissions_start_date_passed_as_activate_date(  # noqa
    mock_simple_nonfugitive_emission_for_activate_testing_1: NonRepairableEmission,
):
    mock_simple_nonfugitive_emission_for_activate_testing_1.activate(date(*[2018, 1, 1]))
    assert (
        mock_simple_nonfugitive_emission_for_activate_testing_1._status == "Active"
    )