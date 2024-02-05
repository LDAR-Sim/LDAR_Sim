from virtual_world.emissions import Emission

from testing.unit_testing.test_virtual_world.test_emissions.emissions_testing_fixtures import (  # Noqa
    mock_simple_emission_1_fix,
)


def test_000_update_correctly_results_in_no_state_change_on_inactive_emission(
    mock_simple_emission_1: Emission,
):
    mock_simple_emission_1.update()
    assert mock_simple_emission_1._active_days == 0
    assert mock_simple_emission_1._days_since_tagged == 0


def test_000_update_correctly_results_in_active_days_change_on_active_emission(
    mock_simple_emission_1: Emission,
):
    mock_simple_emission_1._status = "Active"
    mock_simple_emission_1.update()
    assert mock_simple_emission_1._active_days == 1
    assert mock_simple_emission_1._days_since_tagged == 0


def test_000_update_correctly_results_in_days_since_tagged_change_if_tagged(
    mock_simple_emission_1: Emission,
):
    mock_simple_emission_1._tagged = True
    mock_simple_emission_1.update()
    assert mock_simple_emission_1._active_days == 0
    assert mock_simple_emission_1._days_since_tagged == 1
