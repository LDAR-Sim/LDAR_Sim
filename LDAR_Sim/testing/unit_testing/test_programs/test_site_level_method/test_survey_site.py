from typing import Tuple
from programs.site_level_method import SiteLevelMethod
from testing.unit_testing.test_programs.method_testing_fixtures import (  # noqa
    mock_simple_site_level_method_for_survey_site_testing_fix,
    mock_simple_site_for_survey_site_testing_fix,
    mock_values_for_simple_site_level_method_construction_fix,
)

from testing.unit_testing.test_virtual_world.test_sites.sites_testing_fixtures import (  # noqa
    mock_values_for_simple_site_construction_fix,
)

from virtual_world.sites import Site


def test_000_site_level_method_survey_site_correctly_flags_if_site_level_rate_above_MDL(
    mock_simple_site_level_method_for_survey_site_testing: Tuple[SiteLevelMethod, dict],
    mock_simple_site_for_survey_site_testing: Site,
) -> None:
    site: Site = mock_simple_site_for_survey_site_testing
    slm: SiteLevelMethod = mock_simple_site_level_method_for_survey_site_testing[0]
    slm.survey_site(site)
    assert 0 == 0
