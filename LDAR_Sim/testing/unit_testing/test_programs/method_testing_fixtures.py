from typing import Tuple
import pytest
from programs.method import Method

from programs.site_level_method import SiteLevelMethod
from virtual_world.sites import Site
from sensors.sensor_constant_mapping import SENS_TYPE, SENS_MDL


@pytest.fixture(name="mock_values_for_simple_site_level_method_construction")
def mock_values_for_simple_site_level_method_construction_fix() -> Tuple[str, dict]:
    name = "Test"
    method_info: dict = {Method.DETEC_ACCESSOR: {SENS_TYPE: "default", SENS_MDL: 1.0}}
    return name, method_info


@pytest.fixture(name="mock_simple_site_level_method_for_survey_site_testing")
def mock_simple_site_level_method_for_survey_site_testing_fix() -> Tuple[SiteLevelMethod, dict]:
    slm = SiteLevelMethod()
    expected_survey_site_res = {}
    return slm, expected_survey_site_res


@pytest.fixture(name="mock_simple_site_survey_site_testing")
def mock_simple_site_for_survey_site_testing_fix() -> Site:
    site = Site()
    return site
