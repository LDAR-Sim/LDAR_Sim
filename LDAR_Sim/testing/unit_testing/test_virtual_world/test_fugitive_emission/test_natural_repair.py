from datetime import date
from typing import Tuple
from testing.unit_testing.test_virtual_world.test_fugitive_emission.fugitive_emission_testing_fixtures import (  # noqa
    mock_simple_fugitive_emission_for_natural_repair_testing_1_fix,
)
from virtual_world.fugitive_emission import FugitiveEmission


def test_000_natural_repair_applies_correctly_to_simple_case(
    mock_simple_fugitive_emission_for_natural_repair_testing_1: Tuple[FugitiveEmission, date],
):
    mock_simple_fugitive_emission_for_natural_repair_testing_1[0].natural_repair()
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