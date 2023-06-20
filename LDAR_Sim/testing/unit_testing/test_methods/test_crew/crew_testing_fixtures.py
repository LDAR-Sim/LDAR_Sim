"""File containing fixtures to facilitate testing crew methods"""
import datetime
from typing import Any

import pytest
from src.time_counter import TimeCounter


@pytest.fixture(name="mock_config_for_crew_testing_1")
def mock_config_for_crew_testing_1_fix() -> 'dict[str, Any]':
    return {
        'scheduling': {
            'LDAR_crew_init_location': [-114.062, 51.044],
            'route_planning': False
        },
        'deployment_type': 'mobile',
        'label': 'M_test',
        'coverage': {
            'spatial': 1.0,
            'temporal': 1.0,
        },
        'sensor': {
            'mod_loc': None,
            'type': 'default',
            'MDL': [1.0],
            'QE': 0
        },
        'measurement_scale': 'site'
    }


@pytest.fixture(name="mock_site_for_crew_testing_1")
def mock_site_for_crew_testing_1_fix() -> 'dict[str, Any]':
    return {
        'equipment_groups': 1,
        'active_leaks': [
            {
                'leak_ID': 1,
                'rate': 3,
                'equipment_group': 1
            }
        ]
    }


@pytest.fixture(name="mock_params_for_crew_testing_1")
def mock_params_for_crew_testing_1_fix() -> 'dict[str, Any]':
    return {
        'emissions': {
            'consider_venting': False
        }
    }


@pytest.fixture(name="mock_state_for_crew_testing_1")
def mock_state_for_crew_testing_1_fix(mocker) -> 'dict[str, Any]':
    # Create a mock object to replace the TimeCounter object
    mock_tc = mocker.Mock(TimeCounter)

    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    return {
        't': mock_tc
    }


@pytest.fixture(name="mock_config_for_crew_testing_2")
def mock_config_for_crew_testing_2_fix() -> 'dict[str, Any]':
    return {
        'scheduling': {
            'LDAR_crew_init_location': [-114.062, 51.044],
            'route_planning': False
        },
        'deployment_type': 'mobile',
        'label': 'M_test',
        'coverage': {
            'spatial': 1.0,
            'temporal': 1.0,
        },
        'sensor': {
            'mod_loc': None,
            'type': 'default',
            'MDL': [1.0],
            'QE': 0
        },
        'measurement_scale': 'site'
    }


@pytest.fixture(name="mock_site_for_crew_testing_2")
def mock_site_for_crew_testing_2_fix() -> 'dict[str, Any]':
    return {
        'equipment_groups': 1,
        'active_leaks': [
            {
                'leak_ID': 1,
                'rate': 3,
                'equipment_group': 1
            }
        ]
    }


@pytest.fixture(name="mock_params_for_crew_testing_2")
def mock_params_for_crew_testing_2_fix() -> 'dict[str, Any]':
    return {
        'emissions': {
            'consider_venting': True
        }
    }


@pytest.fixture(name="mock_state_for_crew_testing_2")
def mock_state_for_crew_testing_2_fix() -> 'dict[str,Any]':
    return {
        'empirical_vents': [1]
    }


@pytest.fixture(name="mock_config_for_site_level_FU_visit_site_testing")
def mock_config_for_site_level_FU_visit_site_testing_fix() -> 'dict[str, Any]':
    return {
        'scheduling': {
            'LDAR_crew_init_location': [-114.062, 51.044],
            'route_planning': False
        },
        'deployment_type': 'mobile',
        'label': 'M_sl_FU',
        'coverage': {
            'spatial': 1.0,
            'temporal': 1.0,
        },
        'sensor': {
            'mod_loc': None,
            'type': 'default',
            'MDL': [1.0],
            'QE': 0
        },
        'measurement_scale': 'site',
        'is_follow_up': True
    }


@pytest.fixture(name="mock_timeseries_for_site_level_FU_visit_site_testing")
def mock_timeseries_for_site_level_FU_visit_site_testing_fix() -> 'dict[str, Any]':
    return {
        'M_sl_FU_sites_vis_w_leaks': [0, 0],
        'M_sl_FU_sites_visited': [0, 0],
    }


@pytest.fixture(name="mock_state_for_site_level_FU_visit_site_testing")
def mock_state_for_site_level_FU_visit_site_testing_fix(mocker) -> 'dict[str, Any]':
    # Create a mock object to replace the TimeCounter object
    mock_tc = mocker.Mock(TimeCounter)

    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = 1
    return {
        'site_visits': {'M_sl_FU': []},
        't': mock_tc
    }


@pytest.fixture(name="mock_site_for_site_level_FU_visit_site_testing")
def mock_site_for_site_level_FU_visit_site_testing_fix() -> tuple[dict]:
    return {
        'equipment_groups': 1,
        'facility_ID': 1,
        'subtype_code': 1,
        'active_leaks': [
            {
                'leak_ID': 1,
                'rate': 3,
                'equipment_group': 1,
                'M_test_sp_covered': 1
            }
        ],
        'M_sl_FU_surveys_conducted': 0,
        'M_sl_FU_surveys_done_this_year': 0,
        'M_sl_FU_t_since_last_LDAR': 0,
        'currently_flagged': True
    }


@pytest.fixture(name="mock_results_for_site_level_FU_visit_site_testing")
def mock_results_for_site_level_FU_visit_site_testing_fix() -> tuple[dict]:
    return (
        {
            'found_leak': True
        },
        [{
            'found_leak': True,
        }],
        {
            'equipment_groups': 1,
            'facility_ID': 1,
            'subtype_code': 1,
            'active_leaks': [
                {
                    'leak_ID': 1,
                    'rate': 3,
                    'equipment_group': 1,
                    'M_test_sp_covered': 1
                }
            ],
            'M_sl_FU_surveys_conducted': 1,
            'M_sl_FU_surveys_done_this_year': 1,
            'M_sl_FU_t_since_last_LDAR': 0,
            'historic_t_since_LDAR': 0,
            'currently_flagged': False
        },
        {
            'M_sl_FU_sites_vis_w_leaks': [0, 1],
            'M_sl_FU_sites_visited': [0, 1],
        }

    )


@pytest.fixture(name="mock_config_for_component_level_FU_visit_site_testing")
def mock_config_for_component_level_FU_visit_site_testing_fix() -> 'dict[str, Any]':
    return {
        'scheduling': {
            'LDAR_crew_init_location': [-114.062, 51.044],
            'route_planning': False
        },
        'deployment_type': 'mobile',
        'label': 'M_cl_FU',
        'coverage': {
            'spatial': 1.0,
            'temporal': 1.0,
        },
        'sensor': {
            'mod_loc': None,
            'type': 'default',
            'MDL': [1.0],
            'QE': 0
        },
        'measurement_scale': 'component',
        'is_follow_up': True
    }


@pytest.fixture(name="mock_timeseries_for_component_level_FU_visit_site_testing")
def mock_timeseries_for_component_level_FU_visit_site_testing_fix() -> 'dict[str, Any]':
    return {
        'M_cl_FU_sites_vis_w_leaks': [0, 0],
        'M_cl_FU_sites_visited': [0, 0],
    }


@pytest.fixture(name="mock_state_for_component_level_FU_visit_site_testing")
def mock_state_for_component_level_FU_visit_site_testing_fix(mocker) -> 'dict[str, Any]':
    # Create a mock object to replace the TimeCounter object
    mock_tc = mocker.Mock(TimeCounter)

    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = 1
    return {
        'site_visits': {'M_cl_FU': []},
        't': mock_tc
    }


@pytest.fixture(name="mock_site_for_component_level_FU_visit_site_testing")
def mock_site_for_component_level_follow_up_visit_site_testing_fix() -> tuple[dict]:
    return {
        'equipment_groups': 1,
        'facility_ID': 1,
        'subtype_code': 1,
        'active_leaks': [
            {
                'leak_ID': 1,
                'rate': 3,
                'equipment_group': 1,
                'M_test_sp_covered': 1
            }
        ],
        'M_cl_FU_surveys_conducted': 0,
        'M_cl_FU_surveys_done_this_year': 0,
        'M_cl_FU_t_since_last_LDAR': 0,
        'currently_flagged': True
    }


@pytest.fixture(name="mock_results_for_component_level_FU_visit_site_testing")
def mock_results_for_component_level_FU_visit_site_testing_fix() -> tuple[dict]:
    return (
        {
            'found_leak': True
        },
        [],
        {
            'equipment_groups': 1,
            'facility_ID': 1,
            'subtype_code': 1,
            'active_leaks': [
                {
                    'leak_ID': 1,
                    'rate': 3,
                    'equipment_group': 1,
                    'M_test_sp_covered': 1
                }
            ],
            'M_cl_FU_surveys_conducted': 1,
            'M_cl_FU_surveys_done_this_year': 1,
            'M_cl_FU_t_since_last_LDAR': 0,
            'historic_t_since_LDAR': 0,
            'currently_flagged': False,
            'last_component_survey': 1
        },
        {
            'M_cl_FU_sites_vis_w_leaks': [0, 1],
            'M_cl_FU_sites_visited': [0, 1],
        }

    )


@pytest.fixture(name="mock_config_for_site_level_FU_visit_site_testing_small_leak")
def mock_config_for_site_level_FU_visit_site_testing_small_leak_fix() -> 'dict[str, Any]':
    return {
        'scheduling': {
            'LDAR_crew_init_location': [-114.062, 51.044],
            'route_planning': False
        },
        'deployment_type': 'mobile',
        'label': 'M_sl_FU',
        'coverage': {
            'spatial': 1.0,
            'temporal': 1.0,
        },
        'sensor': {
            'mod_loc': None,
            'type': 'default',
            'MDL': [1.0],
            'QE': 0
        },
        'measurement_scale': 'site',
        'is_follow_up': True
    }


@pytest.fixture(name="mock_timeseries_for_site_level_FU_visit_site_testing_small_leak")
def mock_timeseries_for_site_level_FU_visit_site_testing_small_leak_fix() -> 'dict[str, Any]':
    return {
        'M_sl_FU_sites_vis_w_leaks': [0, 0],
        'M_sl_FU_sites_visited': [0, 0],
    }


@pytest.fixture(name="mock_state_for_site_level_FU_visit_site_testing_small_leak")
def mock_state_for_site_level_FU_visit_site_testing_small_leak_fix(mocker) -> 'dict[str, Any]':
    # Create a mock object to replace the TimeCounter object
    mock_tc = mocker.Mock(TimeCounter)

    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = 1
    return {
        'site_visits': {'M_sl_FU': []},
        't': mock_tc
    }


@pytest.fixture(name="mock_site_for_site_level_FU_visit_site_testing_small_leak")
def mock_site_for_site_level_FU_visit_site_testing_small_leak_fix() -> tuple[dict]:
    return {
        'equipment_groups': 1,
        'facility_ID': 1,
        'subtype_code': 1,
        'active_leaks': [
            {
                'leak_ID': 1,
                'rate': 0.5,
                'equipment_group': 1,
                'M_test_sp_covered': 1
            }
        ],
        'M_sl_FU_surveys_conducted': 0,
        'M_sl_FU_surveys_done_this_year': 0,
        'M_sl_FU_t_since_last_LDAR': 0,
        'currently_flagged': True
    }


@pytest.fixture(name="mock_results_for_site_level_FU_visit_site_testing_small_leak")
def mock_results_for_site_level_FU_visit_site_testing_small_leak_fix() -> tuple[dict]:
    return (
        {
            'found_leak': False
        },
        [],
        {
            'equipment_groups': 1,
            'facility_ID': 1,
            'subtype_code': 1,
            'active_leaks': [
                {
                    'leak_ID': 1,
                    'rate': 0.5,
                    'equipment_group': 1,
                    'M_test_sp_covered': 1
                }
            ],
            'M_sl_FU_surveys_conducted': 1,
            'M_sl_FU_surveys_done_this_year': 1,
            'M_sl_FU_t_since_last_LDAR': 0,
            'historic_t_since_LDAR': 0,
            'currently_flagged': False
        },
        {
            'M_sl_FU_sites_vis_w_leaks': [0, 0],
            'M_sl_FU_sites_visited': [0, 1],
        }

    )


@pytest.fixture(name="mock_config_for_component_level_FU_visit_site_testing_small_leak")
def mock_config_for_component_level_FU_visit_site_testing_small_leak_fix() -> 'dict[str, Any]':
    return {
        'scheduling': {
            'LDAR_crew_init_location': [-114.062, 51.044],
            'route_planning': False
        },
        'deployment_type': 'mobile',
        'label': 'M_cl_FU',
        'coverage': {
            'spatial': 1.0,
            'temporal': 1.0,
        },
        'sensor': {
            'mod_loc': None,
            'type': 'default',
            'MDL': [1.0],
            'QE': 0
        },
        'measurement_scale': 'component',
        'is_follow_up': True
    }


@pytest.fixture(name="mock_timeseries_for_component_level_FU_visit_site_testing_small_leak")
def mock_timeseries_for_component_level_FU_visit_site_testing_small_leak_fix() -> 'dict[str, Any]':
    return {
        'M_cl_FU_sites_vis_w_leaks': [0, 0],
        'M_cl_FU_sites_visited': [0, 0],
    }


@pytest.fixture(name="mock_state_for_component_level_FU_visit_site_testing_small_leak")
def mock_state_for_component_level_FU_visit_site_testing_small_leak_fix(mocker) -> 'dict[str, Any]':
    # Create a mock object to replace the TimeCounter object
    mock_tc = mocker.Mock(TimeCounter)

    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = 1
    return {
        'site_visits': {'M_cl_FU': []},
        't': mock_tc
    }


@pytest.fixture(name="mock_site_for_component_level_FU_visit_site_testing_small_leak")
def mock_site_for_component_level_follow_up_visit_site_testing_small_leak_fix() -> tuple[dict]:
    return {
        'equipment_groups': 1,
        'facility_ID': 1,
        'subtype_code': 1,
        'active_leaks': [
            {
                'leak_ID': 1,
                'rate': 0.5,
                'equipment_group': 1,
                'M_test_sp_covered': 1
            }
        ],
        'M_cl_FU_surveys_conducted': 0,
        'M_cl_FU_surveys_done_this_year': 0,
        'M_cl_FU_t_since_last_LDAR': 0,
        'currently_flagged': True
    }


@pytest.fixture(name="mock_results_for_component_level_FU_visit_site_testing_small_leak")
def mock_results_for_component_level_FU_visit_site_testing_small_leak_fix() -> tuple[dict]:
    return (
        {
            'found_leak': False
        },
        [],
        {
            'equipment_groups': 1,
            'facility_ID': 1,
            'subtype_code': 1,
            'active_leaks': [
                {
                    'leak_ID': 1,
                    'rate': 0.5,
                    'equipment_group': 1,
                    'M_test_sp_covered': 1
                }
            ],
            'M_cl_FU_surveys_conducted': 1,
            'M_cl_FU_surveys_done_this_year': 1,
            'M_cl_FU_t_since_last_LDAR': 0,
            'historic_t_since_LDAR': 0,
            'currently_flagged': False,
            'last_component_survey': 1
        },
        {
            'M_cl_FU_sites_vis_w_leaks': [0, 0],
            'M_cl_FU_sites_visited': [0, 1],
        }

    )


@pytest.fixture(name="mock_config_for_site_level_non_FU_visit_site_testing")
def mock_config_for_site_level_non_FU_visit_site_testing_fix() -> 'dict[str, Any]':
    return {
        'scheduling': {
            'LDAR_crew_init_location': [-114.062, 51.044],
            'route_planning': False
        },
        'deployment_type': 'mobile',
        'label': 'M_sl_FU',
        'coverage': {
            'spatial': 1.0,
            'temporal': 1.0,
        },
        'sensor': {
            'mod_loc': None,
            'type': 'default',
            'MDL': [1.0],
            'QE': 0
        },
        'measurement_scale': 'site',
        'is_follow_up': False
    }


@pytest.fixture(name="mock_timeseries_for_site_level_non_FU_visit_site_testing")
def mock_timeseries_for_site_level_non_FU_visit_site_testing_fix() -> 'dict[str, Any]':
    return {
        'M_sl_FU_sites_vis_w_leaks': [0, 0],
        'M_sl_FU_sites_visited': [0, 0],
    }


@pytest.fixture(name="mock_state_for_site_level_non_FU_visit_site_testing")
def mock_state_for_site_level_non_FU_visit_site_testing_fix(mocker) -> 'dict[str, Any]':
    # Create a mock object to replace the TimeCounter object
    mock_tc = mocker.Mock(TimeCounter)

    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = 1
    return {
        'site_visits': {'M_sl_FU': []},
        't': mock_tc
    }


@pytest.fixture(name="mock_site_for_site_level_non_FU_visit_site_testing")
def mock_site_for_site_level_non_FU_visit_site_testing_fix() -> tuple[dict]:
    return {
        'equipment_groups': 1,
        'facility_ID': 1,
        'subtype_code': 1,
        'active_leaks': [
            {
                'leak_ID': 1,
                'rate': 3,
                'equipment_group': 1,
                'M_test_sp_covered': 1
            }
        ],
        'M_sl_FU_surveys_conducted': 0,
        'M_sl_FU_surveys_done_this_year': 0,
        'M_sl_FU_t_since_last_LDAR': 0,
        'currently_flagged': False
    }


@pytest.fixture(name="mock_results_for_site_level_non_FU_visit_site_testing")
def mock_results_for_site_level_non_FU_visit_site_testing_fix() -> tuple[dict]:
    return (
        {
            'found_leak': True
        },
        [{
            'found_leak': True,
        }],
        {
            'equipment_groups': 1,
            'facility_ID': 1,
            'subtype_code': 1,
            'active_leaks': [
                {
                    'leak_ID': 1,
                    'rate': 3,
                    'equipment_group': 1,
                    'M_test_sp_covered': 1
                }
            ],
            'M_sl_FU_surveys_conducted': 1,
            'M_sl_FU_surveys_done_this_year': 1,
            'M_sl_FU_t_since_last_LDAR': 0,
            'historic_t_since_LDAR': 0,
            'currently_flagged': False
        },
        {
            'M_sl_FU_sites_vis_w_leaks': [0, 1],
            'M_sl_FU_sites_visited': [0, 1],
        }

    )


@pytest.fixture(name="mock_config_for_site_level_non_FU_visit_site_testing_small_leak")
def mock_config_for_site_level_non_FU_visit_site_testing_small_leak_fix() -> 'dict[str, Any]':
    return {
        'scheduling': {
            'LDAR_crew_init_location': [-114.062, 51.044],
            'route_planning': False
        },
        'deployment_type': 'mobile',
        'label': 'M_cl_FU',
        'coverage': {
            'spatial': 1.0,
            'temporal': 1.0,
        },
        'sensor': {
            'mod_loc': None,
            'type': 'default',
            'MDL': [1.0],
            'QE': 0
        },
        'measurement_scale': 'component',
        'is_follow_up': False
    }


@pytest.fixture(name="mock_timeseries_for_site_level_non_FU_visit_site_testing_small_leak")
def mock_timeseries_for_site_level_non_FU_visit_site_testing_small_leak_fix() -> 'dict[str, Any]':
    return {
        'M_cl_FU_sites_vis_w_leaks': [0, 0],
        'M_cl_FU_sites_visited': [0, 0],
    }


@pytest.fixture(name="mock_state_for_site_level_non_FU_visit_site_testing_small_leak")
def mock_state_for_site_level_non_FU_visit_site_testing_small_leak_fix(mocker) -> 'dict[str, Any]':
    # Create a mock object to replace the TimeCounter object
    mock_tc = mocker.Mock(TimeCounter)

    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = 1
    return {
        'site_visits': {'M_cl_FU': []},
        't': mock_tc
    }


@pytest.fixture(name="mock_site_for_site_level_non_FU_visit_site_testing_small_leak")
def mock_site_for_site_level_non_FU_visit_site_testing_small_leak_fix() -> tuple[dict]:
    return {
        'equipment_groups': 1,
        'facility_ID': 1,
        'subtype_code': 1,
        'active_leaks': [
            {
                'leak_ID': 1,
                'rate': 0.5,
                'equipment_group': 1,
                'M_test_sp_covered': 1
            }
        ],
        'M_cl_FU_surveys_conducted': 0,
        'M_cl_FU_surveys_done_this_year': 0,
        'M_cl_FU_t_since_last_LDAR': 0,
        'currently_flagged': False
    }


@pytest.fixture(name="mock_results_for_site_level_non_FU_visit_site_testing_small_leak")
def mock_results_for_site_level_non_FU_visit_site_testing_small_leak_fix() -> tuple[dict]:
    return (
        {
            'found_leak': False
        },
        [],
        {
            'equipment_groups': 1,
            'facility_ID': 1,
            'subtype_code': 1,
            'active_leaks': [
                {
                    'leak_ID': 1,
                    'rate': 0.5,
                    'equipment_group': 1,
                    'M_test_sp_covered': 1
                }
            ],
            'M_cl_FU_surveys_conducted': 1,
            'M_cl_FU_surveys_done_this_year': 1,
            'M_cl_FU_t_since_last_LDAR': 0,
            'historic_t_since_LDAR': 0,
            'currently_flagged': False,
            'last_component_survey': 1
        },
        {
            'M_cl_FU_sites_vis_w_leaks': [0, 0],
            'M_cl_FU_sites_visited': [0, 1],
        }

    )
