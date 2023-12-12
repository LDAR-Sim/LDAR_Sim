from typing import Tuple
from virtual_world.sites import Site
from testing.unit_testing.test_virtual_world.test_sites.sites_testing_fixtures import (  # noqa
    mock_values_for_simple_site_construction_fix,
)


def test_000_simple_site_is_properly_constructed(
    mock_values_for_simple_site_construction: Tuple[str, float, float, int, dict, dict]
):
    id, lat, lon, equip_groups, prop_params, site_info = mock_values_for_simple_site_construction
    test_site = Site(
        id=id,
        lat=lat,
        long=lon,
        equipment_groups=equip_groups,
        propagating_params=prop_params,
        infrastructure_inputs=site_info,
    )
    assert isinstance(test_site, Site)
