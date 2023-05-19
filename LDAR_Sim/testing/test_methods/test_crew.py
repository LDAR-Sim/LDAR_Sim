"""Test file to unit test crew functionality"""

from typing import Any

import pytest
import os
from src.methods.crew import BaseCrew
import numpy as np
from pathlib import Path
import sys


@pytest.fixture
def mock_config_for_crew_testing_1() -> 'dict[str, Any]':
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


@pytest.fixture()
def mock_site_for_crew_testing_1() -> 'dict[str, Any]':
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


@pytest.fixture()
def mock_params_for_crew_testing_1() -> 'dict[str, Any]':
    return {
        'emissions': {
            'consider_venting': False
        }
    }


@pytest.fixture()
def expected_detect_emissions_for_mock_set_1() -> 'dict[str,Any]':
    return {
        'equip_measured_rates': []
    }


def test_004_detect_emissions_simple(mock_config_for_crew_testing_1,
                                     mock_site_for_crew_testing_1,
                                     mock_params_for_crew_testing_1,
                                     mocker) -> None:
    np.random.seed(0)  # Setting a seed for reproducibility
    sys.path.insert(1, str(Path(os.path.dirname(os.path.realpath(__file__))
                                ).parent.parent / "src"))  # Add src directory to the path
    mocker.patch('methods.sensors.default.detect_emissions',
                 autospec=True, side_effect=lambda *args: args)
    crew = BaseCrew(None, mock_params_for_crew_testing_1,
                    mock_config_for_crew_testing_1, None, None, None, None)
    result: Any = crew.detect_emissions(mock_site_for_crew_testing_1)
    expected: tuple[Any] = (
        crew, mock_site_for_crew_testing_1,
        mock_site_for_crew_testing_1['active_leaks'],
        [3], 3, 3, 0, [3])

    assert result == expected
