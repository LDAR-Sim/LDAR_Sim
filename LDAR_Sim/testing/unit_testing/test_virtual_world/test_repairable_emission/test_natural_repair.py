from datetime import date
from typing import Tuple
from testing.unit_testing.test_virtual_world.test_repairable_emission.repairable_emission_testing_fixtures import (  # noqa
    mock_simple_fugitive_emission_for_natural_repair_testing_1_fix,
    mock_simple_fugitive_emission_for_natural_repair_testing_2_fix,
)
from virtual_world.emission_types.repairable_emission import RepairableEmission
from src.file_processing.output_processing.output_utils import EmisInfo


def test_000_natural_repair_applies_correctly_to_simple_case(
    mock_simple_fugitive_emission_for_natural_repair_testing_1: Tuple[RepairableEmission, date],
):
    emis_info = EmisInfo(0, 0, 0, 0, 0)
    mock_simple_fugitive_emission_for_natural_repair_testing_1[0].natural_repair(emis_info)
    assert mock_simple_fugitive_emission_for_natural_repair_testing_1[0]._tagged is True
    assert (
        mock_simple_fugitive_emission_for_natural_repair_testing_1[0]._tagged_by_company
        == "natural"
    )
    assert mock_simple_fugitive_emission_for_natural_repair_testing_1[0]._status == "repaired"
    assert (
        mock_simple_fugitive_emission_for_natural_repair_testing_1[0]._repair_date
        == mock_simple_fugitive_emission_for_natural_repair_testing_1[1]
    )


def test_000_natural_repair_applies_correctly_to_pregen_emission_simple(
    mock_simple_fugitive_emission_for_natural_repair_testing_2: Tuple[RepairableEmission, date],
):
    emis_info = EmisInfo(0, 0, 0, 0, 0)
    mock_simple_fugitive_emission_for_natural_repair_testing_2[0].natural_repair(emis_info)
    assert mock_simple_fugitive_emission_for_natural_repair_testing_2[0]._tagged is True
    assert (
        mock_simple_fugitive_emission_for_natural_repair_testing_2[0]._tagged_by_company
        == "natural"
    )
    assert mock_simple_fugitive_emission_for_natural_repair_testing_2[0]._status == "repaired"
    assert (
        mock_simple_fugitive_emission_for_natural_repair_testing_2[0]._repair_date
        == mock_simple_fugitive_emission_for_natural_repair_testing_2[1]
    )
