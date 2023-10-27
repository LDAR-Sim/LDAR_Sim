"""Test file to unit test crew.py detect_emissions functionality"""

from typing import Any

import os
from src.methods.crew import BaseCrew
import numpy as np
from pathlib import Path
import sys
from testing.unit_testing.test_methods.test_crew.crew_testing_fixtures import (  # noqa: F401
    mock_site_for_crew_testing_1_fix,
    mock_config_for_crew_testing_1_fix,
    mock_vw_for_crew_testing_1_fix,
    mock_settings_for_crew_testing_1_fix,
    mock_config_for_crew_testing_2_fix,
    mock_vw_for_crew_testing_2_fix,
    mock_site_for_crew_testing_2_fix,
)


def test_051_detect_emissions_simple(
    mock_config_for_crew_testing_1,
    mock_site_for_crew_testing_1,
    mock_vw_for_crew_testing_1,
    mock_settings_for_crew_testing_1,
    mocker,
) -> None:
    np.random.seed(0)  # Setting a seed for reproducibility
    # Add src directory to the path
    sys.path.insert(
        1,
        str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent.parent.parent / "src"),
    )
    # Mock the sensors detect emissions function called inside of crew.detect_emissions
    # to return the arguments it's been passed. This way we can check the behavior of
    # crew.detect emissions without being dependant on sensor.detect_emissions.
    mocker.patch(
        "methods.sensors.default.detect_emissions", autospec=True, side_effect=lambda *args: args
    )
    crew = BaseCrew(
        None,
        None,
        mock_vw_for_crew_testing_1,
        mock_settings_for_crew_testing_1,
        mock_config_for_crew_testing_1,
        None,
        None,
        None,
        None,
    )
    result: Any = crew.detect_emissions(mock_site_for_crew_testing_1)
    expected: tuple[Any] = (
        crew,
        mock_site_for_crew_testing_1,
        mock_site_for_crew_testing_1["active_leaks"],
        [3],
        3,
        3,
        0,
        [3],
    )

    assert result == expected


def test_051_detect_emissions_simple_w_static_vents(
    mock_config_for_crew_testing_2,
    mock_site_for_crew_testing_2,
    mock_vw_for_crew_testing_2,
    mock_settings_for_crew_testing_1,
    mocker,
) -> None:
    np.random.seed(0)  # Setting a seed for reproducibility
    # Add src directory to the path
    sys.path.insert(
        1,
        str(Path(os.path.dirname(os.path.realpath(__file__))).parent.parent.parent.parent / "src"),
    )
    # Mock the sensors detect emissions function called inside of crew.detect_emissions
    # to return the arguments it's been passed. This way we can check the behavior of
    # crew.detect emissions without being dependant on sensor.detect_emissions.
    crew = BaseCrew(
        None,
        None,
        mock_vw_for_crew_testing_2,
        mock_settings_for_crew_testing_1,
        mock_config_for_crew_testing_2,
        None,
        None,
        None,
        None,
    )
    mocker.patch(
        "methods.sensors.default.detect_emissions", autospec=True, side_effect=lambda *args: args
    )
    result: Any = crew.detect_emissions(mock_site_for_crew_testing_2)
    expected: tuple[Any] = (
        crew,
        mock_site_for_crew_testing_2,
        mock_site_for_crew_testing_2["active_leaks"],
        [4],
        4,
        4,
        1,
        [4],
    )

    assert result == expected
