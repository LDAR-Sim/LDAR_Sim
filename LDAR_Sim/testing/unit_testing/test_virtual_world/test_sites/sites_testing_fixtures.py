import pytest
from typing import Tuple

from virtual_world.infrastructure_const import Infrastructure_Constants
from virtual_world.sites import Site
from datetime import date


@pytest.fixture(name="mock_values_for_simple_site_construction")
def mock_values_for_simple_site_construction_fix() -> Tuple[str, float, float, int, dict, dict]:
    id: str = "test"
    lat: float = 34.56
    lon: float = -44.56
    equipment_groups: int = 1
    prop_params: dict = {
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS: None,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD: 0,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC: 100,
        "Method_Specific_Params": {
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_MONTHS_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_YEARS_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER: {},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER: {},
        },
    }
    infra_inputs: dict = {}
    return (id, lat, lon, equipment_groups, prop_params, infra_inputs)


@pytest.fixture(name="mock_site_for_simple_generate_emissions")
def mock_site_for_simple_generate_emissions_fix() -> Tuple[Site, date, date]:
    id: str = "test"
    lat: float = 34.56
    lon: float = -44.56
    equipment_groups: int = 1
    prop_params: dict = {
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS: None,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD: 0,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC: 100,
        "Method_Specific_Params": {
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_MONTHS_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_YEARS_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER: {},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER: {},
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
    simulation_start_date = date(*[2017, 1, 1])
    simulation_end_date = date(*[2017, 1, 5])
    return test_site, simulation_start_date, simulation_end_date


@pytest.fixture(name="mock_site_for_simple_activate_emissions")
def mock_site_for_simple_activate_emissions_fix() -> Tuple[Site, date, int]:
    id: str = "test"
    lat: float = 34.56
    lon: float = -44.56
    equipment_groups: int = 1
    prop_params: dict = {
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS: None,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD: 0,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC: 100,
        "Method_Specific_Params": {
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_MONTHS_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_YEARS_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER: {},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER: {},
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
        sim_start_date=simulation_start_date, sim_end_date=simulation_end_date, sim_number=1
    )
    activate_date: date = date(*[2017, 1, 1])
    return test_site, activate_date, 1


@pytest.fixture(name="mock_site_for_simple_get_detectable_emissions")
def mock_site_for_simple_get_detectable_emissions_fix() -> Tuple[Site, str]:
    id: str = "test"
    lat: float = 34.56
    lon: float = -44.56
    equipment_groups: int = 1
    prop_params: dict = {
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS: None,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED: 1,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD: 0,
        Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC: 100,
        "Method_Specific_Params": {
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_MONTHS_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_YEARS_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
            Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: {"test": 1},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER: {},
            Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER: {},
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
    test_method: str = "test"
    simulation_start_date: date = date(*[2017, 1, 1])
    simulation_end_date: date = date(*[2017, 1, 5])
    test_site.generate_emissions(
        sim_start_date=simulation_start_date, sim_end_date=simulation_end_date, sim_number=1
    )
    activate_date: date = date(*[2017, 1, 1])
    test_site.activate_emissions(activate_date, 1)
    return test_site, test_method