from file_processing.output_processing.output_utils import EmisInfo
from virtual_world.emission_types.non_repairable_emissions import NonRepairableEmission

from testing.unit_testing.test_virtual_world.test_non_repairable_emission.non_repairable_emission_testing_fixtures import (  # noqa
    mock_nonfugitive_emission_for_update_no_status_change_fix,
    mock_nonfugitive_emission_for_update_no_status_change_emission_recorded_fix,
    mock_nonfugitive_emission_for_update_will_expire_fix,
)


def test_000_update_returns_active_when_no_change_to_status_emission_active(
    mock_nonfugitive_emission_for_update_no_status_change: NonRepairableEmission,
) -> None:
    emis_info: EmisInfo = EmisInfo()
    emis_active: bool = mock_nonfugitive_emission_for_update_no_status_change.update(emis_info)
    assert emis_active
    assert emis_info.emis_expired == 0


def test_000_update_returns_active_when_no_change_to_status_emission_recorded_and_not_expired(  # noqa
    mock_nonfugitive_emission_for_update_no_status_change_emission_recorded: NonRepairableEmission,
) -> None:
    emis_info: EmisInfo = EmisInfo()
    emis_active: bool = (
        mock_nonfugitive_emission_for_update_no_status_change_emission_recorded.update(emis_info)
    )
    assert emis_active
    assert emis_info.emis_expired == 0


def test_000_update_returns_inactive_if_leak_newly_expired(
    mock_nonfugitive_emission_for_update_will_expire: NonRepairableEmission,
) -> None:
    emis_info: EmisInfo = EmisInfo()
    emis_active: bool = mock_nonfugitive_emission_for_update_will_expire.update(emis_info)
    assert not emis_active
    assert emis_info.emis_expired == 1
