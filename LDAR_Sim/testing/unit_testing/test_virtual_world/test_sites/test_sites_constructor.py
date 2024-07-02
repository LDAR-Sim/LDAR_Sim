from typing import Tuple
from constants.infrastructure_const import Infrastructure_Constants
from constants.param_default_const import Common_Params as cp
from src.virtual_world.sites import Site
from virtual_world.equipment_groups import Equipment_Group
from testing.unit_testing.test_virtual_world.test_sites.sites_testing_fixtures import (  # noqa
    mock_values_for_simple_site_construction_fix,
)


def get_mock_propagating_params_and_expected_equipment_split(
    equipment_count: int,
) -> Tuple[dict, dict]:
    # Set site level values for propagating parameters that need to be split among equipment groups
    rep_emis_epr: float = 1.0
    non_rep_emis_epr: float = 1.0
    survey_cost_placeholder: dict = {"test": 1.0}
    survey_time_placeholder: dict = {"test": 1.0}
    # Calculate the expected values for those parameters at the equipment group level
    rep_emis_epr_equip: float = rep_emis_epr / equipment_count
    non_rep_emis_epr_equip = non_rep_emis_epr / equipment_count
    survey_cost_placeholder_equip: dict = {"test": 1.0 / equipment_count}
    survey_time_placeholder_equip: dict = {"test": 1.0 / equipment_count}
    return (
        {
            Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ERS: {"test": [1]},
            Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: 1,
            Infrastructure_Constants.Sites_File_Constants.REP_EMIS_ED: 1,
            Infrastructure_Constants.Sites_File_Constants.REP_EMIS_MULTI: True,
            Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_MULTI: True,
            Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_EPR: non_rep_emis_epr,
            Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_ERS: None,
            Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RD: {cp.VAL: 0},
            Infrastructure_Constants.Sites_File_Constants.REP_EMIS_RC: {cp.VAL: 100},
            cp.METH_SPECIFIC: {
                Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
                Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: {},
                Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_MONTHS_PLACEHOLDER: {},
                Infrastructure_Constants.Sites_File_Constants.DEPLOYMENT_YEARS_PLACEHOLDER: {},
                Infrastructure_Constants.Sites_File_Constants.SURVEY_FREQUENCY_PLACEHOLDER: {},
                Infrastructure_Constants.Sites_File_Constants.SITE_DEPLOYMENT_PLACEHOLDER: {},
                (
                    Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER
                ): survey_time_placeholder,
                (
                    Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER
                ): survey_cost_placeholder,
            },
        },
        {
            Infrastructure_Constants.Sites_File_Constants.REP_EMIS_EPR: rep_emis_epr_equip,
            Infrastructure_Constants.Sites_File_Constants.NON_REP_EMIS_EPR: non_rep_emis_epr_equip,
            cp.METH_SPECIFIC: {
                (
                    Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_TIME_PLACEHOLDER
                ): survey_time_placeholder_equip,
                (
                    Infrastructure_Constants.Equipment_Group_File_Constants.SURVEY_COST_PLACEHOLDER
                ): survey_cost_placeholder_equip,
                Infrastructure_Constants.Sites_File_Constants.SPATIAL_PLACEHOLDER: {},
            },
        },
    )


def mock_equipment_group_init(self, id, infrastructure_inputs, prop_params, info):
    self.propagating_params = prop_params


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


def test_000_site_properties_properly_split_among_equipment_groups(
    monkeypatch, mock_values_for_simple_site_construction: Tuple[str, float, float, int, dict, dict]
):
    monkeypatch.setattr(Equipment_Group, "__init__", mock_equipment_group_init)

    id, lat, lon, start_date, _, _, site_info, method = mock_values_for_simple_site_construction
    equipment_groups: int = 3
    prop_params, split_params = get_mock_propagating_params_and_expected_equipment_split(
        equipment_groups
    )

    test_site = Site(
        id=id,
        lat=lat,
        long=lon,
        start_date=start_date,
        equipment_groups=equipment_groups,
        propagating_params=prop_params,
        infrastructure_inputs=site_info,
        methods=method,
    )

    for equip_group in test_site.equipment_groups:
        for key, param in split_params.items():
            assert equip_group.propagating_params[key] == param
