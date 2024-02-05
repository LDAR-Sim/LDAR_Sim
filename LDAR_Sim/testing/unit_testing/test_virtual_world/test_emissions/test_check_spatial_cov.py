import numpy as np
from typing import Tuple
from virtual_world.emissions import Emission

from testing.unit_testing.test_virtual_world.test_emissions.emissions_testing_fixtures import (  # Noqa
    mock_simple_emission_spat_cov_testing_1_fix,
    mock_random_emission_spat_cov_testing_1_fix,
)


def test_000_check_spatial_cov_correctly_return_emission_spatial_coverage(
    mock_simple_emission_spat_cov_testing_1: Tuple[Emission, dict[str, int]],
):
    emission, expected_results = mock_simple_emission_spat_cov_testing_1
    for method, result in expected_results.items():
        assert emission.check_spatial_cov(method) == result


def test_000_check_spatial_cov_correctly_return_emission_spatial_coverage_random(
    mock_random_emission_spat_cov_testing_1: Tuple[Emission, dict[str, int]],
):
    np.random.seed(1)
    emission, expected_results = mock_random_emission_spat_cov_testing_1
    for method, result in expected_results.items():
        assert emission.check_spatial_cov(method) == result
