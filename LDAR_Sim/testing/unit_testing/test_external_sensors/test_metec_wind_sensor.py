""" Module for testing the external sensor METEC_WIND"""

from src.methods.crew import BaseCrew
import numpy as np
from testing.unit_testing.test_methods.test_crew.crew_testing_fixtures import (  # Noqa: 401
    mock_site_for_crew_testing_1_fix,
    mock_vw_for_crew_testing_1_fix,
    mock_config_for_crew_testing_2_fix,
    mock_vw_for_crew_testing_2_fix,
    mock_site_for_crew_testing_2_fix,
    mock_settings_for_crew_testing_1_fix,
    mock_site_for_crew_testing_3_fix,
)
from testing.unit_testing.test_external_sensors.external_sensor_testing_fixtures import (  # Noqa: 401
    mock_config_for_sensor_testing_4_fix,
    mock_config_for_sensor_testing_5_fix,
    mock_config_for_sensor_testing_6_fix,
    mock_config_for_sensor_testing_7_fix,
    mock_site_dict_for_sensor_return_1_fix,
    mock_site_dict_for_sensor_return_4_fix,
    mock_config_for_sensor_testing_3_fix,
    mock_site_dict_for_sensor_return_2_fix,
    mock_site_for_sensor_testing_2_fix,
    mock_state_for_sensor_testing_1_fix,
)
from external_sensors.METEC_WIND import detect_emissions


def test_093_detect_emissions_simple(
    mock_config_for_sensor_testing_4,
    mock_site_for_crew_testing_1,
    mock_vw_for_crew_testing_1,
    mock_settings_for_crew_testing_1,
    mock_site_dict_for_sensor_return_1,
    mock_state_for_sensor_testing_1,
) -> None:
    """
    Simple test for checking METEC_WIND for successful detection

    """
    np.random.seed(0)  # Setting a seed for reproducibility

    crew = BaseCrew(
        mock_state_for_sensor_testing_1,
        None,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        mock_config_for_sensor_testing_4,
        mock_state_for_sensor_testing_1,
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


def test_093_detect_emissions_simple_fail(
    mock_config_for_sensor_testing_3,
    mock_site_for_crew_testing_1,
    mock_vw_for_crew_testing_1,
    mock_settings_for_crew_testing_1,
    mock_site_dict_for_sensor_return_2,
    mock_site_for_sensor_testing_2,
    mock_state_for_sensor_testing_1,
) -> None:
    """
    Simple test for checking METEC_WIND for successful detection

    """
    np.random.seed(0)  # Setting a seed for reproducibility

    crew = BaseCrew(
        mock_state_for_sensor_testing_1,
        None,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        mock_config_for_sensor_testing_3,
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


def test_093_detect_emissions_cutoff_fail(
    mock_config_for_sensor_testing_6,
    mock_site_for_crew_testing_1,
    mock_vw_for_crew_testing_1,
    mock_settings_for_crew_testing_1,
    mock_site_dict_for_sensor_return_2,
    mock_site_for_sensor_testing_2,
    mock_state_for_sensor_testing_1,
) -> None:
    """
    Simple test for checking METEC_WIND for successful detection

    """
    np.random.seed(0)  # Setting a seed for reproducibility

    crew = BaseCrew(
        mock_state_for_sensor_testing_1,
        None,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        mock_config_for_sensor_testing_6,
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


def test_093_detect_emissions_simple_equip(
    mock_config_for_sensor_testing_7,
    mock_site_for_crew_testing_1,
    mock_vw_for_crew_testing_1,
    mock_settings_for_crew_testing_1,
    mock_site_dict_for_sensor_return_4,
    mock_state_for_sensor_testing_1,
) -> None:
    """
    Simple test for checking METEC_WIND for successful detection

    """
    np.random.seed(0)  # Setting a seed for reproducibility

    crew = BaseCrew(
        mock_state_for_sensor_testing_1,
        None,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        mock_config_for_sensor_testing_7,
        mock_state_for_sensor_testing_1,
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
    expected: dict = mock_site_dict_for_sensor_return_4
    assert result == expected


# def test_093_detect_emissions_simple_component(
#     mock_config_for_sensor_testing_5,
#     mock_site_for_crew_testing_3,
#     mock_vw_for_crew_testing_1,
#     mock_settings_for_crew_testing_1,
#     mock_site_dict_for_sensor_return_4,
#     mock_state_for_sensor_testing_1,
# ) -> None:
#     """
#     Simple test for checking METEC_WIND for successful detection

#     """
#     np.random.seed(0)  # Setting a seed for reproducibility

#     crew = BaseCrew(
#         mock_state_for_sensor_testing_1,
#         None,
#         mock_vw_for_crew_testing_1,
#         mock_settings_for_crew_testing_1,
#         mock_config_for_sensor_testing_5,
#         mock_state_for_sensor_testing_1,
#         None,
#         None,
#         None,
#     )

#     result: dict = detect_emissions(
#         crew,
#         mock_site_for_crew_testing_3,
#         mock_site_for_crew_testing_3["active_leaks"],
#         [3],
#         3,
#         3,
#         0,
#         [3],
#     )
#     expected: dict = mock_site_dict_for_sensor_return_4
#     assert result == expected
