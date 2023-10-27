"""Test file to unit test attribution.py update_tag functionality"""
from src.utils.attribution import update_tag
from testing.unit_testing.test_utils.test_attribution.attribution_testing_fixtures import (  # Noqa: 401
    mock_leak_for_update_tag_testing_1_fix,
    mock_leak_for_update_tag_testing_2_fix,
    mock_company_for_update_tag_testing_1_fix,
    mock_TimeCounter_for_update_tag_testing_1_fix,
    mock_timeseries_for_update_tag_testing_1_fix,
    mock_site_for_update_tag_testing_1_fix,
)


def test_072_update_tag_nat_repair_prev_tagged_by_other_company(
    mock_leak_for_update_tag_testing_1,
    mock_timeseries_for_update_tag_testing_1,
    mock_TimeCounter_for_update_tag_testing_1,
    mock_company_for_update_tag_testing_1,
):
    update_tag(
        mock_leak_for_update_tag_testing_1,
        None,
        None,
        mock_timeseries_for_update_tag_testing_1,
        mock_TimeCounter_for_update_tag_testing_1,
        mock_company_for_update_tag_testing_1,
    )
    assert (
        mock_timeseries_for_update_tag_testing_1["natural_n_tags"][
            mock_TimeCounter_for_update_tag_testing_1.current_timestep
        ]
        == 1
    )


def test_072_update_tag_nat_repair_no_prev_tag(
    mock_leak_for_update_tag_testing_2,
    mock_site_for_update_tag_testing_1,
    mock_timeseries_for_update_tag_testing_1,
    mock_TimeCounter_for_update_tag_testing_1,
    mock_company_for_update_tag_testing_1,
):
    update_tag(
        mock_leak_for_update_tag_testing_2,
        None,
        mock_site_for_update_tag_testing_1,
        mock_timeseries_for_update_tag_testing_1,
        mock_TimeCounter_for_update_tag_testing_1,
        mock_company_for_update_tag_testing_1,
    )
    assert (
        mock_timeseries_for_update_tag_testing_1["natural_n_tags"][
            mock_TimeCounter_for_update_tag_testing_1.current_timestep
        ]
        == 1
    )
