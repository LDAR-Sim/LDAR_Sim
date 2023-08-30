""" Fixures for testing ldar_sim.py functionality"""

import pytest
from src.time_counter import TimeCounter
from src.weather.weather_lookup_hourly import WeatherLookup

import datetime


@pytest.fixture(name="mock_state_for_ldar_sim_testing_1")
def mock_state_for_ldar_sim_testing_1_fix(mocker):
    mock_tc = mocker.Mock(TimeCounter)
    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = 1
    mock_weather = mocker.Mock(WeatherLookup)
    mock_weather.latitude = [55.05]
    mock_weather.longitude = [-119.99]
    return {
        'campaigns': None,
        'sites': [
            {
                "active_leaks": {
                    'tagged': True,
                },
                'subtype_code': None,
                'facility_ID': 0,
                'lat': 55.05,
                'lon': -119.99
            }
        ],
        't': mock_tc,
        'weather': mock_weather,
        'site_visits': {
            "OGI": []
        }
    }


@pytest.fixture(name="mock_vw_for_ldar_sim_testing_1")
def mock_vw_for_ldar_sim_testing_1_fix():
    return {
        'emissions': {
            'leak_file': None,
            'max_leak_rate': 100000
        },
        'subtype_file': None,
        'pregenerate_leaks': True,
        'initial_leaks': [
            [
                {
                    'tagged': True,
                    'tagged_by_company': "natural",
                    'day_ts_began': -1,
                    "rate": 1
                }
            ]
        ],
        'timesteps': 2
    }


@pytest.fixture(name="mock_program_params_for_ldar_sim_testing_1")
def mock_program_params_for_ldar_sim_testing_1_fix():
    return {
        'economics': {
            'repair_costs': {
                'file': None,
                'vals': [200.0]
            }
        },
        'methods': {}

    }


@pytest.fixture(name="mock_timeseries_for_ldar_sim_testing_1")
def mock_timeseries_for_ldar_sim_testing_1_fix():
    return {
        'total_daily_cost': []
    }


@pytest.fixture(name="mock_vw_for_ldar_sim_testing_2")
def mock_vw_for_ldar_sim_testing_2_fix():
    return {
        'emissions': {
            'leak_file': None,
            'max_leak_rate': 100000,
            'consider_venting': False
        },
        'subtype_file': None,
        'pregenerate_leaks': True,
        'initial_leaks': [
            [
                {
                    'tagged': True,
                    'tagged_by_company': "OGI",
                    'day_ts_began': -1,
                    "rate": 1,
                    "estimated_date_began": 0
                }
            ]
        ],
        'timesteps': 2,
        'consider_weather': False
    }


@pytest.fixture(name="mock_state_for_ldar_sim_testing_2")
def mock_state_for_ldar_sim_testing_2_fix(mocker):
    mock_tc = mocker.Mock(TimeCounter)
    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = 1
    mock_tc.start_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_weather = mocker.Mock(WeatherLookup)
    mock_weather.latitude = [55.05]
    mock_weather.longitude = [-119.99]
    return {
        'campaigns': None,
        'sites': [
            {
                "active_leaks": {
                    'tagged': True,
                    "estimated_date_began": 0
                },
                'subtype_code': None,
                'facility_ID': 0,
                'lat': 55.05,
                'lon': -119.99,
                'repair_delay': 0
            }
        ],
        't': mock_tc,
        'weather': mock_weather,
        'site_visits': {
            "OGI": []
        },
        'methods': []
    }


@pytest.fixture(name="mock_sim_settings_for_ldar_sim_testing_2")
def mock_sim_settings_for_ldar_sim_testing_2_fix():
    return {
        "input_directory": None
    }


@pytest.fixture(name="mock_program_params_for_ldar_sim_testing_2")
def mock_program_params_for_ldar_sim_testing_2_fix():
    return {
        'economics': {
            'repair_costs': {
                'file': None,
                'vals': [200.0]
            },
            'verification_cost': 100
        },
        'methods': {
            "OGI": {
                "reporting_delay": 0,
                'RS': 1,
                'scheduling': {
                    'min_time_bt_surveys': None,
                    'deployment_months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    'route_planning': False,
                    'deployment_years': [2017],
                    'LDAR_crew_init_location': []
                },
                'is_follow_up': False,
                'deployment_type': 'mobile',
                'measurement_scale': 'component',
                'time': 60,
                'n_crews': 1,
                'label': "OGI",
                'max_workday': 8,
                't_bw_sites': {
                    'file': None
                },
                'consider_daylight': True,
                'cost': {
                    'upfront': 0
                }
            }
        }

    }
