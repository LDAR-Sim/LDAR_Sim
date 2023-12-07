from datetime import date
from typing import Tuple
from testing.unit_testing.test_virtual_world.test_fugitive_emission.fugitive_emission_testing_fixtures import (  # noqa
    mock_simple_fugitive_emission_for_check_if_repaired_testing_1_fix,
    mock_simple_fugitive_emission_for_check_if_repaired_testing_2_fix,
)
from virtual_world.fugitive_emission import FugitiveEmission


def test_000_check_if_repaired_does_not_repair_if_not_repairable(
    mock_simple_fugitive_emission_for_check_if_repaired_testing_1: FugitiveEmission,
) -> None:
    mock_simple_fugitive_emission_for_check_if_repaired_testing_1.check_if_repaired()
    assert mock_simple_fugitive_emission_for_check_if_repaired_testing_1._status != "repaired"
    assert mock_simple_fugitive_emission_for_check_if_repaired_testing_1._repair_date is None


def test_000_check_if_repaired_correctly_repairs_if_repair_delay_passed(
    mock_simple_fugitive_emission_for_check_if_repaired_testing_2: Tuple[FugitiveEmission, date],
) -> None:
    fug_emission: FugitiveEmission = mock_simple_fugitive_emission_for_check_if_repaired_testing_2[
        0
    ]
    fug_emission.check_if_repaired()
    assert fug_emission._status == "repaired"
    assert (
        fug_emission._repair_date
        == mock_simple_fugitive_emission_for_check_if_repaired_testing_2[1]
    )
