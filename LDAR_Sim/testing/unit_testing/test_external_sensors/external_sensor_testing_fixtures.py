"""File containing fixtures to facilitate testing external sensors"""
import datetime
from typing import Any, Dict

import pytest
import numpy as np
from src.time_counter import TimeCounter
from src.weather.weather_lookup_hourly import WeatherLookup


@pytest.fixture(name="mock_config_for_sensor_testing_1")
def mock_config_for_sensor_testing_1_fix() -> "dict[str, Any]":
    return {
        "scheduling": {"LDAR_crew_init_location": [-114.062, 51.044], "route_planning": False},
        "deployment_type": "mobile",
        "label": "M_test",
        "coverage": {
            "spatial": 1.0,
            "temporal": 1.0,
        },
        "sensor": {
            "mod_loc": "external_sensors.METEC_NO_WIND",
            "type": "default",
            "MDL": [10.0, 1.0, 0],
            "QE": 0,
        },
        "measurement_scale": "site",
    }


@pytest.fixture(name="mock_site_dict_for_sensor_return_1")
def mock_site_dict_for_sensor_return_1_fix() -> Dict[str, Any]:
    return {
        "site": {
            "equipment_groups": 1,
            "active_leaks": [{"leak_ID": 1, "rate": 3, "equipment_group": 1}],
        },
        "leaks_present": [{"leak_ID": 1, "rate": 3, "equipment_group": 1}],
        "site_true_rate": 3,
        "site_measured_rate": 3.0,
        "equip_measured_rates": [],
        "vent_rate": 0,
        "found_leak": True,
    }


@pytest.fixture(name="mock_config_for_sensor_testing_2")
def mock_config_for_sensor_testing_2_fix() -> "dict[str, Any]":
    return {
        "scheduling": {"LDAR_crew_init_location": [-114.062, 51.044], "route_planning": False},
        "deployment_type": "mobile",
        "label": "M_test",
        "coverage": {
            "spatial": 1.0,
            "temporal": 1.0,
        },
        "sensor": {
            "mod_loc": "external_sensors.METEC_NO_WIND",
            "type": "default",
            "MDL": [15.0, 1.0, 0],
            "QE": 0,
        },
        "measurement_scale": "site",
    }


@pytest.fixture(name="mock_config_for_sensor_testing_3")
def mock_config_for_sensor_testing_3_fix() -> "dict[str, Any]":
    return {
        "scheduling": {"LDAR_crew_init_location": [-114.062, 51.044], "route_planning": False},
        "deployment_type": "mobile",
        "label": "M_test",
        "coverage": {
            "spatial": 1.0,
            "temporal": 1.0,
        },
        "sensor": {
            "mod_loc": "external_sensors.METEC_WIND",
            "type": "default",
            "MDL": [15.0, 1.0, 0],
            "QE": 0,
        },
        "measurement_scale": "site",
    }


@pytest.fixture(name="mock_site_dict_for_sensor_return_1")
def mock_site_dict_for_sensor_return_1_fix() -> Dict[str, Any]:
    return {
        "site": {
            "equipment_groups": 1,
            "active_leaks": [{"leak_ID": 1, "rate": 3, "equipment_group": 1}],
        },
        "leaks_present": [{"leak_ID": 1, "rate": 3, "equipment_group": 1}],
        "site_true_rate": 3,
        "site_measured_rate": 3.0,
        "equip_measured_rates": [],
        "vent_rate": 0,
        "found_leak": True,
    }


@pytest.fixture(name="mock_config_for_sensor_testing_2")
def mock_config_for_sensor_testing_2_fix() -> "dict[str, Any]":
    return {
        "scheduling": {"LDAR_crew_init_location": [-114.062, 51.044], "route_planning": False},
        "deployment_type": "mobile",
        "label": "M_test",
        "coverage": {
            "spatial": 1.0,
            "temporal": 1.0,
        },
        "sensor": {
            "mod_loc": "external_sensors.METEC_NO_WIND",
            "type": "default",
            "MDL": [15.0, 1.0, 0],
            "QE": 0,
        },
        "measurement_scale": "site",
    }


@pytest.fixture(name="mock_config_for_sensor_testing_3")
def mock_config_for_sensor_testing_3_fix() -> "dict[str, Any]":
    return {
        "scheduling": {"LDAR_crew_init_location": [-114.062, 51.044], "route_planning": False},
        "deployment_type": "mobile",
        "label": "M_test",
        "coverage": {
            "spatial": 1.0,
            "temporal": 1.0,
        },
        "sensor": {
            "mod_loc": "external_sensors.METEC_WIND",
            "type": "default",
            "MDL": [15.0, 1.0, 0],
            "QE": 0,
        },
        "measurement_scale": "site",
    }


@pytest.fixture(name="mock_config_for_sensor_testing_4")
def mock_config_for_sensor_testing_4_fix() -> "dict[str, Any]":
    return {
        "scheduling": {"LDAR_crew_init_location": [-114.062, 51.044], "route_planning": False},
        "deployment_type": "mobile",
        "label": "M_test",
        "coverage": {
            "spatial": 1.0,
            "temporal": 1.0,
        },
        "sensor": {
            "mod_loc": "external_sensors.METEC_WIND",
            "type": "default",
            "MDL": [1.0, 1.0, 0],
            "QE": 0,
        },
        "measurement_scale": "site",
    }


@pytest.fixture(name="mock_site_dict_for_sensor_return_2")
def mock_site_dict_for_sensor_return_2_fix() -> Dict[str, Any]:
    return {
        "site": {
            "equipment_groups": 1,
            "active_leaks": [{"leak_ID": 1, "rate": 3, "equipment_group": 1}],
            "M_test_missed_leaks": 1,
        },
        "leaks_present": [{"leak_ID": 1, "rate": 3, "equipment_group": 1}],
        "site_true_rate": 3,
        "site_measured_rate": 0,
        "equip_measured_rates": [],
        "vent_rate": 0,
        "found_leak": False,
    }


@pytest.fixture(name="mock_site_for_sensor_testing_2")
def mock_site_for_sensor_testing_2_fix() -> "dict[str, Any]":
    return {
        "equipment_groups": 1,
        "active_leaks": [{"leak_ID": 1, "rate": 3, "equipment_group": 1}],
        "M_test_missed_leaks": 0,
    }


@pytest.fixture(name="mock_state_for_sensor_testing_1")
def mock_state_for_sensor_testing_1_fix(mocker) -> "dict[str, Any]":
    # Create a mock object to replace the TimeCounter object
    mock_tc = mocker.Mock(TimeCounter)

    mock_tc.current_date = datetime.datetime(2017, 1, 1, 8, 0)
    mock_tc.current_timestep = datetime.datetime(2017, 1, 1, 8, 0)

    mock_weather = mocker.Mock(WeatherLookup)
    mock_weather.get_hourly_weather.return_value = {"winds": np.array([1.0])}

    return {
        "t": mock_tc,
        "M_test_missed_leaks": {datetime.datetime(2017, 1, 1, 8, 0): 0},
        "weather": mock_weather,
    }
