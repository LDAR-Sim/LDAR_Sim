"""File containing fixtures to facilitate testing crew methods"""
from typing import Any

import pytest


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
