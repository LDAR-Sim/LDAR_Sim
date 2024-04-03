from typing import Any, Tuple
from testing.unit_testing.test_virtual_world.test_fugitive_emission.fugitive_emission_testing_fixtures import (  # noqa
    mock_simple_emission_for_get_summary_dict_1_fix,
)
from src.virtual_world.fugitive_emission import FugitiveEmission


def test_000_get_summary_dict_fe_returns_expected_values_for_simple_case(
    mock_simple_emission_for_get_summary_dict: Tuple[FugitiveEmission, dict[str, int]]
) -> None:
    end_date, emission, expected_result = mock_simple_emission_for_get_summary_dict
    summary_dict: dict[str, Any] = emission.get_summary_dict(end_date)
    assert summary_dict == expected_result
