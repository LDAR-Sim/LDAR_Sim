"""Fixtures for testing input manager methods"""

import pytest
from src.constants.general_const import Version_Constants as vc


@pytest.fixture(name="mock_parameter_correct_maj_min_ver")
def mock_parameter_correct_maj_min_ver_fix() -> dict[str, str]:
    return {"version": vc.CURRENT_FULL_VERSION}


@pytest.fixture(name="mock_parameter_incorrect_maj_ver")
def mock_parameter_incorrect_maj_ver_fix() -> dict[str, str]:
    return {"version": "2" + "." + vc.CURRENT_MINOR_VERSION}


@pytest.fixture(name="mock_parameter_incorrect_min_ver")
def mock_parameter_incorrect_min_ver_fix() -> dict[str, str]:
    return {"version": vc.CURRENT_MAJOR_VERSION + "." + "100000"}


@pytest.fixture(name="mock_parameter_maj_only_ver")
def mock_parameter_maj_only_ver_fix() -> dict[str, str]:
    return {"version": vc.CURRENT_MAJOR_VERSION}


@pytest.fixture(name="mock_parameter_sim_settings")
def mock_parameter_sim_settings_fix() -> dict[str, str]:
    return {"parameter_level": "simulation_settings"}


@pytest.fixture(name="mock_parameter_program_level")
def mock_parameter_program_level_fix() -> dict[str, str]:
    return {"parameter_level": "program"}


@pytest.fixture(name="mock_parameter_write_data_make_plots")
def mock_parameter_write_data_make_plots_fix() -> dict[str, bool]:
    return {"make_plots": True, "write_data": True}


@pytest.fixture(name="mock_parameter_write_data_no_plots")
def mock_parameter_write_data_no_plots_fix() -> dict[str, bool]:
    return {
        "write_data": True,
        "make_plots": False,
    }


@pytest.fixture(name="mock_parameter_make_plots_no_data")
def mock_parameter_make_plots_no_data_fix() -> dict[str, bool]:
    return {"make_plots": True, "write_data": False}


@pytest.fixture(name="mock_parameter_no_data_no_plots")
def mock_parameter_no_data_no_plots_fix() -> dict[str, bool]:
    return {"make_plots": False, "write_data": False}
