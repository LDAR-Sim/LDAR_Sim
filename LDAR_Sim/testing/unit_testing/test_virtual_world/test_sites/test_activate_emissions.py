from datetime import date
from typing import Tuple
from src.virtual_world.sites import Site
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
    active_emission = False
    # Don't know which equipment component the emission will be added to.
    # But with production_rate of 1, there should be at least 1 emission active
    for eqg in test_site._equipment_groups:
        for comp in eqg._component:
            if len(comp._active_emissions) > 0:
                active_emission = True

    assert active_emission
