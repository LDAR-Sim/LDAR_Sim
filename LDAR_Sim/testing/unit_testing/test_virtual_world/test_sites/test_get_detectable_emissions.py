from typing import Tuple
from virtual_world.sites import Site
from testing.unit_testing.test_virtual_world.test_sites.sites_testing_fixtures import (  # noqa
    mock_site_for_simple_get_detectable_emissions_fix,
)


def test_000_get_detectable_emissions_returns_expected_emissions(
    mock_site_for_simple_get_detectable_emissions: Tuple[Site, str, str],
) -> None:
    site: Site = mock_site_for_simple_get_detectable_emissions[0]
    method = mock_site_for_simple_get_detectable_emissions[1]
    survey_level = mock_site_for_simple_get_detectable_emissions[2]
    detectable_emissions = site.get_detectable_emissions(
        method_name=method, survey_level=survey_level
    )
    assert detectable_emissions is not None
