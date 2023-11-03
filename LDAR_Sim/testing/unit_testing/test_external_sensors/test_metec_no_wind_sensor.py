""" Module for testing the external sensor METEC_NO_WIND"""

from src.methods.crew import BaseCrew
import numpy as np
from testing.unit_testing.test_methods.test_crew.crew_testing_fixtures import (  # Noqa: 401
    mock_site_for_crew_testing_1_fix,
    mock_vw_for_crew_testing_1_fix,
    mock_config_for_crew_testing_2_fix,
    mock_vw_for_crew_testing_2_fix,
    mock_site_for_crew_testing_2_fix,
    mock_settings_for_crew_testing_1_fix,
)
from testing.unit_testing.test_external_sensors.external_sensor_testing_fixtures import (  # Noqa: 401
    mock_config_for_sensor_testing_1_fix,
    mock_site_dict_for_sensor_return_1_fix,
    mock_config_for_sensor_testing_2_fix,
    mock_site_dict_for_sensor_return_2_fix,
    mock_site_for_sensor_testing_2_fix,
    mock_state_for_sensor_testing_1_fix,
    mock_prog_param_for_testing_1_fix,
)
from external_sensors.METEC_NO_WIND import detect_emissions


def test_091_detect_emissions_simple(
    mock_config_for_sensor_testing_1,
    mock_site_for_crew_testing_1,
    mock_vw_for_crew_testing_1,
    mock_settings_for_crew_testing_1,
    mock_site_dict_for_sensor_return_1,
) -> None:
    """
    Simple test for checking METEC_NO_WIND for successful detection

    """
    np.random.seed(0)  # Setting a seed for reproducibility

    crew = BaseCrew(
        None,
        None,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        mock_config_for_sensor_testing_1,
        None,
        None,
        None,
        None,
    )

    result: dict = detect_emissions(
        crew,
        mock_site_for_crew_testing_1,
        mock_site_for_crew_testing_1["active_leaks"],
        [3],
        3,
        3,
        0,
        [3],
    )
    expected: dict = mock_site_dict_for_sensor_return_1
    assert result == expected


def test_092_detect_emissions_simple_fail(
    mock_config_for_sensor_testing_2,
    mock_site_for_crew_testing_1,
    mock_vw_for_crew_testing_1,
    mock_settings_for_crew_testing_1,
    mock_site_dict_for_sensor_return_2,
    mock_site_for_sensor_testing_2,
    mock_state_for_sensor_testing_1,
    mock_prog_param_for_testing_1,
) -> None:
    """
    Simple test for checking METEC_NO_WIND for successful detection

    """
    np.random.seed(0)  # Setting a seed for reproducibility

    crew = BaseCrew(
        mock_state_for_sensor_testing_1,
        mock_prog_param_for_testing_1,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        mock_config_for_sensor_testing_2,
        mock_state_for_sensor_testing_1,
        None,
        None,
        None,
    )

    result: dict = detect_emissions(
        crew,
        mock_site_for_sensor_testing_2,
        mock_site_for_crew_testing_1["active_leaks"],
        [3],
        3,
        3,
        0,
        [3],
    )
    expected: dict = mock_site_dict_for_sensor_return_2
    assert result == expected
