"""Test file to unit test crew.py gen_site_vis_rec functionality"""

import os
import sys
from pathlib import Path

import pytest
from src.methods.crew import BaseCrew

from testing.unit_testing.test_methods.test_crew.crew_testing_fixtures import (  # noqa: F401
    mock_config_for_crew_testing_1_fix,
    mock_vw_for_crew_testing_1_fix,
    mock_state_for_crew_testing_1_fix,
    mock_settings_for_crew_testing_1_fix
    )


@pytest.mark.parametrize("test_input, expected", [
    (
        (
            {'site_true_rate': 3,
             'site_measured_rate': 3,
             'vent_rate': 0,
             'found_leak': True,
             'leaks_present': [
                 {
                     'leak_ID': 1,
                     'rate': 3,
                     'equipment_group': 1
                 }
             ]
             },
            {'equipment_groups': 1,
             'facility_ID': 1,
             'subtype_code': 1,
             'active_leaks': [
                 {
                     'leak_ID': 1,
                     'rate': 3,
                     'equipment_group': 1,
                     'M_test_sp_covered': 1
                 }
             ]
             },
            1
        ),
        {
            'site_vis_date': "2017-01-01",
            'site_visited': 1,
            'site_subtype_code': 1,
            'leaks_at_site': [
                {
                    'M_test_sp_covered': 1,
                    'M_test_survey_tp_covered': 1,
                    'leak_ID': 1,
                    'rate': 3
                }
            ],
            'site_true_rate': 3,
            'site_measured_rate': 3,
            'site_vent_rate': 0,
            'found_leak': True,
            'crew_ID': 1
        }
    ),
    (
        (
            {'site_true_rate': 4,
             'site_measured_rate': 3,
             'vent_rate': 1,
             'found_leak': True,
             'leaks_present': [
                 {
                     'leak_ID': 1,
                     'rate': 3,
                     'equipment_group': 1
                 }
             ]
             },
            {'equipment_groups': 1,
             'facility_ID': 2,
             'subtype_code': 2,
             'active_leaks': [
                 {
                     'leak_ID': 1,
                     'rate': 3,
                     'equipment_group': 1,
                     'M_test_sp_covered': 1
                 }
             ]
             },
            2
        ),
        {
            'site_vis_date': "2017-01-01",
            'site_visited': 2,
            'site_subtype_code': 2,
            'leaks_at_site': [
                {
                    'M_test_sp_covered': 1,
                    'M_test_survey_tp_covered': 1,
                    'leak_ID': 1,
                    'rate': 3
                }
            ],
            'site_true_rate': 4,
            'site_measured_rate': 3,
            'site_vent_rate': 1,
            'found_leak': True,
            'crew_ID': 2
        }
    ),
    (
        (
            {'site_true_rate': 0,
             'site_measured_rate': 0,
             'vent_rate': 0,
             'found_leak': False,
             'leaks_present': []
             },
            {'equipment_groups': 1,
             'facility_ID': 3,
             'subtype_code': 3,
             'active_leaks': []
             },
            3
        ),
        {
            'site_vis_date': "2017-01-01",
            'site_visited': 3,
            'site_subtype_code': 3,
            'leaks_at_site': [],
            'site_true_rate': 0,
            'site_measured_rate': 0,
            'site_vent_rate': 0,
            'found_leak': False,
            'crew_ID': 3
        }
    )
]
)
def test_052_gen_site_vis_rec_returns_expected_vals(
    mocker,
    test_input,
    expected,
    mock_vw_for_crew_testing_1,
    mock_config_for_crew_testing_1,
    mock_state_for_crew_testing_1,
    mock_settings_for_crew_testing_1
):
    # Add src directory to the path
    sys.path.insert(1, str(Path(os.path.dirname(os.path.realpath(__file__))
                                ).parent.parent.parent.parent / "src"))

    crew = BaseCrew(
        mock_state_for_crew_testing_1,
        None,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        mock_config_for_crew_testing_1,
        None,
        None,
        test_input[2],
        None
    )
    result = crew.gen_site_vis_rec(test_input[0], test_input[1])
    assert result == expected
