""" Fixtures for testing leaks"""

import pytest
from datetime import datetime
from typing import Any, Dict


@pytest.fixture(name="mock_program")
def mock_program_fix():
    return {
        'subtype_file': None,
        'NRd': 10,
        'n_init_leaks': None,
        'n_init_days': None,
        'start_date': (2022, 1, 1),
        'emissions': {
            'LPR': 0.5,
            'leak_file': None,
        },
        'leak_rate_source': 'sample',
        'empirical_leak_rates': [1],

    }


@pytest.fixture(name="mock_program_2")
def mock_program_2_fix():
    return {
        'subtype_file': None,
        'NRd': 10,
        'n_init_leaks': 1,
        'n_init_days': 10,
        'start_date': (2022, 1, 1),
        'emissions': {
            'LPR': 0.5,
            'leak_file': None,
        },
        'leak_rate_source': 'sample',
        'empirical_leak_rates': [1],
    }


@pytest.fixture(name="mock_site_for_leak_test")
def mock_site_for_leak_test_fix() -> Dict[str, Any]:
    return {
        'facility_ID': 'test',
        'equipment_groups': 1,
        'empirical_leak_rates': [1],
        'lat': 52.0,
        'lon': -114.0,
        'leak_rate_source': 'sample',
    }


@pytest.fixture(name="mock_site_return_test")
def mock_site_return_test_fix() -> list[Dict[str, Any]]:
    return [{
        'leak_ID': 'test_0000000001',
        'facility_ID': 'test',
        'equipment_group': 0,
        'rate': 1,
        'lat': 52.0,
        'lon': -114.0,
        'status': 'active',
        'days_active': 0,
        'volume': None,
        'estimated_volume': None,
        'estimated_volume_b': None,
        'measured_rate': None,
        'tagged': False,
        'component': 'unknown',
        'date_began': datetime(2022, 1, 1, 0, 0),
        'day_ts_began': 0,
        'estimated_date_began': None,
        'date_tagged': None,
        'tagged_by_company': None,
        'tagged_by_crew': None,
        'init_detect_by': None,
        'init_detect_date': None,
        'requires_shutdown': False,
        'date_repaired': None,
        'repair_delay': None,
    }]
