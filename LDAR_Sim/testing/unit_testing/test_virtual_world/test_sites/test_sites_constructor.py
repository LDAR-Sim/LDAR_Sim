from typing import Tuple
from src.virtual_world.sites import Site
from testing.unit_testing.test_virtual_world.test_sites.sites_testing_fixtures import (  # noqa
    mock_values_for_simple_site_construction_fix,
)


def test_000_simple_site_is_properly_constructed(
    mock_values_for_simple_site_construction: Tuple[str, float, float, int, dict, dict]
):
    id, lat, lon, start_date, equip_groups, prop_params, site_info, method = (
        mock_values_for_simple_site_construction
    )
    test_site = Site(
        id=id,
        lat=lat,
        long=lon,
        start_date=start_date,
        equipment_groups=equip_groups,
        propagating_params=prop_params,
        infrastructure_inputs=site_info,
        methods=method,
    )
    assert isinstance(test_site, Site)
