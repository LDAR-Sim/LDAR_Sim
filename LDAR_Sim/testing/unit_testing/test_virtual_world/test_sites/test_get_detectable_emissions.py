from typing import Tuple
from src.virtual_world.sites import Site
from testing.unit_testing.test_virtual_world.test_sites.sites_testing_fixtures import (  # noqa
    mock_site_for_simple_get_detectable_emissions_fix,
)


def test_000_get_detectable_emissions_returns_expected_emissions(
    mock_site_for_simple_get_detectable_emissions: Tuple[Site, str],
) -> None:
    site: Site = mock_site_for_simple_get_detectable_emissions[0]
    method: str = mock_site_for_simple_get_detectable_emissions[1]
    detectable_emissions: dict[str, dict[str, list]] = site.get_detectable_emissions(
        method_name=method
    )
    for key, val in detectable_emissions.items():
        assert isinstance(key, (str, int))
        assert isinstance(val, dict)
        for key2, val2 in val.items():
            assert isinstance(key2, (str, int))
            assert isinstance(val2, list)
