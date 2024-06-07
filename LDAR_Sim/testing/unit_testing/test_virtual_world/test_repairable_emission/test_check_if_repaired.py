from datetime import date
from typing import Tuple
from testing.unit_testing.test_virtual_world.test_repairable_emission.repairable_emission_testing_fixtures import (  # noqa
    mock_simple_fugitive_emission_for_check_if_repaired_testing_1_fix,
    mock_simple_fugitive_emission_for_check_if_repaired_testing_2_fix,
)
from virtual_world.emission_types.repairable_emission import RepairableEmission
from src.file_processing.output_processing.output_utils import EmisInfo
from src.constants.general_const import Emission_Constants as ec


def test_000_check_if_repaired_does_not_repair_if_not_repairable(
    mock_simple_fugitive_emission_for_check_if_repaired_testing_1: RepairableEmission,
) -> None:

    emis_info = EmisInfo(0, 0, 0, 0, 0)

    mock_simple_fugitive_emission_for_check_if_repaired_testing_1.check_if_repaired(emis_info)
    assert mock_simple_fugitive_emission_for_check_if_repaired_testing_1._status != ec.REPAIRED
    assert mock_simple_fugitive_emission_for_check_if_repaired_testing_1._repair_date is None


def test_000_check_if_repaired_correctly_repairs_if_repair_delay_passed(
    mock_simple_fugitive_emission_for_check_if_repaired_testing_2: Tuple[RepairableEmission, date],
) -> None:
    fug_emission: RepairableEmission = (
        mock_simple_fugitive_emission_for_check_if_repaired_testing_2[0]
    )
    emis_info = EmisInfo(0, 0, 0, 0, 0)
    fug_emission.check_if_repaired(emis_info)
    assert fug_emission._status == ec.REPAIRED
    assert (
        fug_emission._repair_date
        == mock_simple_fugitive_emission_for_check_if_repaired_testing_2[1]
    )
