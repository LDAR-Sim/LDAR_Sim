"""Test file to unit test crew.py visit_site() functionality"""
import os
import sys
from pathlib import Path
from typing import Any

import pytest
from src.methods.crew import BaseCrew

from testing.unit_testing.test_methods.test_crew.crew_testing_fixtures import (  # noqa: F401
    mock_config_for_component_level_FU_visit_site_testing_fix,
    mock_site_for_component_level_follow_up_visit_site_testing_fix,
    mock_state_for_component_level_FU_visit_site_testing_fix,
    mock_timeseries_for_component_level_FU_visit_site_testing_fix,
    mock_results_for_component_level_FU_visit_site_testing_fix,
    mock_config_for_site_level_FU_visit_site_testing_fix,
    mock_site_for_site_level_FU_visit_site_testing_fix,
    mock_state_for_site_level_FU_visit_site_testing_fix,
    mock_timeseries_for_site_level_FU_visit_site_testing_fix,
    mock_results_for_site_level_FU_visit_site_testing_fix,
    mock_config_for_component_level_FU_visit_site_testing_small_leak_fix,
    mock_site_for_component_level_follow_up_visit_site_testing_small_leak_fix,
    mock_state_for_component_level_FU_visit_site_testing_small_leak_fix,
    mock_timeseries_for_component_level_FU_visit_site_testing_small_leak_fix,
    mock_results_for_component_level_FU_visit_site_testing_small_leak_fix,
    mock_config_for_site_level_FU_visit_site_testing_small_leak_fix,
    mock_site_for_site_level_FU_visit_site_testing_small_leak_fix,
    mock_state_for_site_level_FU_visit_site_testing_small_leak_fix,
    mock_timeseries_for_site_level_FU_visit_site_testing_small_leak_fix,
    mock_results_for_site_level_FU_visit_site_testing_small_leak_fix,
    mock_config_for_site_level_non_FU_visit_site_testing_fix,
    mock_site_for_site_level_non_FU_visit_site_testing_fix,
    mock_state_for_site_level_non_FU_visit_site_testing_fix,
    mock_timeseries_for_site_level_non_FU_visit_site_testing_fix,
    mock_results_for_site_level_non_FU_visit_site_testing_fix,
    mock_config_for_site_level_non_FU_visit_site_testing_small_leak_fix,
    mock_site_for_site_level_non_FU_visit_site_testing_small_leak_fix,
    mock_state_for_site_level_non_FU_visit_site_testing_small_leak_fix,
    mock_timeseries_for_site_level_non_FU_visit_site_testing_small_leak_fix,
    mock_results_for_site_level_non_FU_visit_site_testing_small_leak_fix,
    mock_vw_for_crew_testing_1_fix,
    mock_settings_for_crew_testing_1_fix,
)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        # Test site level follow-up where leak is found
        (
            (
                "mock_site_for_site_level_FU_visit_site_testing",
                "mock_config_for_site_level_FU_visit_site_testing",
                "mock_state_for_site_level_FU_visit_site_testing",
                "mock_timeseries_for_site_level_FU_visit_site_testing",
            ),
            ("mock_results_for_site_level_FU_visit_site_testing"),
        ),
        # Test site level follow-up where leak is missed
        (
            (
                "mock_site_for_site_level_FU_visit_site_testing_small_leak",
                "mock_config_for_site_level_FU_visit_site_testing_small_leak",
                "mock_state_for_site_level_FU_visit_site_testing_small_leak",
                "mock_timeseries_for_site_level_FU_visit_site_testing_small_leak",
            ),
            ("mock_results_for_site_level_FU_visit_site_testing_small_leak"),
        ),
        # Test component level follow-up where leak is found
        (
            (
                "mock_site_for_component_level_FU_visit_site_testing",
                "mock_config_for_component_level_FU_visit_site_testing",
                "mock_state_for_component_level_FU_visit_site_testing",
                "mock_timeseries_for_component_level_FU_visit_site_testing",
            ),
            ("mock_results_for_component_level_FU_visit_site_testing"),
        ),
        # Test component level follow-up where leak is missed
        (
            (
                "mock_site_for_component_level_FU_visit_site_testing_small_leak",
                "mock_config_for_component_level_FU_visit_site_testing_small_leak",
                "mock_state_for_component_level_FU_visit_site_testing_small_leak",
                "mock_timeseries_for_component_level_FU_visit_site_testing_small_leak",
            ),
            ("mock_results_for_component_level_FU_visit_site_testing_small_leak"),
        ),
        # Test site level screening (non follow-up) where leak is found
        (
            (
                "mock_site_for_site_level_non_FU_visit_site_testing",
                "mock_config_for_site_level_non_FU_visit_site_testing",
                "mock_state_for_site_level_non_FU_visit_site_testing",
                "mock_timeseries_for_site_level_non_FU_visit_site_testing",
            ),
            ("mock_results_for_site_level_non_FU_visit_site_testing"),
        ),
        # Test site level screening (non follow-up) where leak is missed
        (
            (
                "mock_site_for_site_level_non_FU_visit_site_testing_small_leak",
                "mock_config_for_site_level_non_FU_visit_site_testing_small_leak",
                "mock_state_for_site_level_non_FU_visit_site_testing_small_leak",
                "mock_timeseries_for_site_level_non_FU_visit_site_testing_small_leak",
            ),
            ("mock_results_for_site_level_non_FU_visit_site_testing_small_leak"),
        ),
    ],
)
def test_053_visit_site_gives_expected_behavior(
    mocker,
    test_input,
    expected,
    request,
    mock_vw_for_crew_testing_1,
    mock_settings_for_crew_testing_1,
) -> None:
    # Add src directory to the path
    sys.path.insert(
        1,
        str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent.parent.parent / "src"),
    )
    crew = BaseCrew(
        request.getfixturevalue(test_input[2]),
        None,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        request.getfixturevalue(test_input[1]),
        request.getfixturevalue(test_input[3]),
        None,
        None,
        None,
    )
    mocker.patch.object(
        BaseCrew, "detect_emissions", return_value=request.getfixturevalue(expected)[0]
    )
    mocker.patch.object(BaseCrew, "gen_site_vis_rec", return_value={})
    crew.candidate_flags = []
    site = request.getfixturevalue(test_input[0])
    crew.visit_site(site)
    result: Any = crew.candidate_flags
    assert result == request.getfixturevalue(expected)[1]
    assert site == request.getfixturevalue(expected)[2]
    assert crew.timeseries == request.getfixturevalue(expected)[3]
