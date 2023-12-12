from datetime import date
from typing import Tuple
from virtual_world.sites import Site
from testing.unit_testing.test_virtual_world.test_sites.sites_testing_fixtures import (  # noqa
    mock_site_for_simple_activate_emissions_fix,
)


def test_000_simple_site_correctly_activates_emissions(
    mock_site_for_simple_activate_emissions: Tuple[Site, date, int]
) -> None:
    test_site: Site = mock_site_for_simple_activate_emissions[0]
    activate_date: date = mock_site_for_simple_activate_emissions[1]
    sim_num: int = mock_site_for_simple_activate_emissions[2]
    test_site.activate_emissions(activate_date, sim_num)
    for eqg in test_site._equipment_groups:
        for equip in eqg._equipment:
            assert equip._active_emissions is not None and len(equip._active_emissions) != 0
