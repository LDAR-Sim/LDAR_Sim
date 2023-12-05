from virtual_world.fugitive_emission import FugitiveEmission

from testing.unit_testing.test_virtual_world.test_fugitive_emission.fugitive_emission_testing_fixtures import (  # noqa
    mock_fugitive_emission_for_update_ready_for_nat_repair_fix,
    mock_fugitive_emission_for_update_no_status_change_fix,
    mock_fugitive_emission_for_update_no_status_change_emission_tagged_fix,
    mock_fugitive_emission_for_update_newly_repaired_fix,
)


def test_000_update_returns_nat_repair_and_calls_nat_repair_if_ready_for_nat_repair(
    mock_fugitive_emission_for_update_ready_for_nat_repair: FugitiveEmission,
) -> None:
    update_status: str = mock_fugitive_emission_for_update_ready_for_nat_repair.update()
    assert update_status == "nat_repaired"


def test_000_update_returns_no_status_change_when_no_change_to_status_emission_active(
    mock_fugitive_emission_for_update_no_status_change: FugitiveEmission,
) -> None:
    update_status: str = mock_fugitive_emission_for_update_no_status_change.update()
    assert update_status == "no_status_change"


def test_000_update_returns_no_status_change_when_no_change_to_status_emission_tagged_but_not_repaired(  # noqa
    mock_fugitive_emission_for_update_no_status_change_emission_tagged: FugitiveEmission,
) -> None:
    update_status: str = mock_fugitive_emission_for_update_no_status_change_emission_tagged.update()
    assert update_status == "no_status_change"


def test_000_update_returns_repaired_if_leak_newly_repaired(
    mock_fugitive_emission_for_update_newly_repaired: FugitiveEmission,
) -> None:
    update_status: str = mock_fugitive_emission_for_update_newly_repaired.update()
    assert update_status == "repaired"
