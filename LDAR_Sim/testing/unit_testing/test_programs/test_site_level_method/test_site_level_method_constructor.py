from typing import Tuple
from programs.site_level_method import SiteLevelMethod
from testing.unit_testing.test_programs.method_testing_fixtures import (  # noqa
    mock_values_for_simple_site_level_method_construction_fix,
)


def test_000_simple_sl_method_can_be_constructed(
    mock_values_for_simple_site_level_method_construction: Tuple[str, dict]
) -> None:
    name: str = mock_values_for_simple_site_level_method_construction[0]
    info: dict = mock_values_for_simple_site_level_method_construction[1]
    slm: SiteLevelMethod = SiteLevelMethod(name, info)
    assert isinstance(slm, SiteLevelMethod)
