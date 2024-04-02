from datetime import date
from typing import Tuple
import pytest

from src.programs.site_level_method import SiteLevelMethod
from src.virtual_world.infrastructure_const import Infrastructure_Constants
from src.virtual_world.sites import Site


@pytest.fixture(name="mock_simple_site_level_method_for_survey_site_testing")
def mock_simple_site_level_method_for_survey_site_testing_fix(
    mock_values_for_simple_site_level_method_construction: Tuple[str, dict],
) -> Tuple[SiteLevelMethod, dict]:
    name, info = mock_values_for_simple_site_level_method_construction
    slm = SiteLevelMethod(name, info)
    expected_survey_site_res: dict = {}
    return slm, expected_survey_site_res


@pytest.fixture(name="mock_simple_site_for_survey_site_testing")
def mock_simple_site_for_survey_site_testing_fix() -> Site:
    id: str = "test"
    lat: float = 34.56
    lon: float = -44.56
    equipment_groups: int = 1
    prop_params: dict = {
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD: 0,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC: 100,
        "Method_Specific_Params": {
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: {"Test": 1},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER: {},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_MONTHS_PLACEHOLDER: {
                "Test": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                ]
            },
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_YEARS_PLACEHOLDER: {
                "Test": [2020, 2021, 2022, 2023, 2024, 2025]
            },
        },
    }
    infra_inputs: dict = {}
    test_site = Site(
        id=id,
        lat=lat,
        long=lon,
        equipment_groups=equipment_groups,
        propagating_params=prop_params,
        infrastructure_inputs=infra_inputs,
    )
    simulation_start_date: date = date(*[2017, 1, 1])
    simulation_end_date: date = date(*[2017, 1, 5])
    test_site.generate_emissions(
        sim_start_date=simulation_start_date,
        sim_end_date=simulation_end_date,
        sim_number=1,
    )
    activate_date: date = date(*[2017, 1, 1])
    test_site.activate_emissions(activate_date, 1)
    return test_site
