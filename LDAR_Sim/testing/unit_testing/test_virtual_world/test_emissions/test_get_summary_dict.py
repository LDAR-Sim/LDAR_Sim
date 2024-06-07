from typing import Any, Tuple
from src.virtual_world.emission_types.emission import Emission

from testing.unit_testing.test_virtual_world.test_emissions.emissions_testing_fixtures import (  # Noqa
    mock_simple_emission_for_get_summary_dict_fix,
)


def test_000_get_summary_dict_returns_expected_values_for_simple_case(
    mock_simple_emission_for_get_summary_dict: Tuple[Emission, dict[str, int]]
) -> None:
    emission, expected_result = mock_simple_emission_for_get_summary_dict
    summary_dict: dict[str, Any] = emission.get_summary_dict()
    assert summary_dict == expected_result
