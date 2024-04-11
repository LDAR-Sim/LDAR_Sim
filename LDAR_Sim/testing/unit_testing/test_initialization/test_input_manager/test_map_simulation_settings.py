"""Test for the map_simulation_settings_method"""

from testing.unit_testing.test_initialization.test_input_manager.input_manager_testing_fixtures import (  # Noqa: 401
    mock_parameter_write_data_make_plots_fix,
    mock_parameter_make_plots_no_data_fix,
    mock_parameter_write_data_no_plots_fix,
    mock_parameter_no_data_no_plots_fix,
)

from constants.param_default_const import Sim_Setting_Params as ssp

from file_processing.input_processing.input_manager import InputManager


def test_045_make_plots_write_data(mocker, mock_parameter_write_data_make_plots):
    parameters = mock_parameter_write_data_make_plots

    mocker.patch.object(InputManager, "__init__", lambda self: None)

    input_mngr = InputManager()

    input_mngr.map_simulation_settings(parameters)

    assert parameters[ssp.OUTPUTS][ssp.PLOTS] is True and (
        parameters[ssp.OUTPUTS][ssp.SITES]
        and parameters[ssp.OUTPUTS][ssp.TIMESERIES]
        and parameters[ssp.OUTPUTS][ssp.LEAKS]
        and parameters[ssp.OUTPUTS][ssp.BATCH_REPORTING]
    )


def test_045_write_data_no_plots(mocker, mock_parameter_write_data_no_plots):
    parameters = mock_parameter_write_data_no_plots

    mocker.patch.object(InputManager, "__init__", lambda self: None)

    input_mngr = InputManager()

    input_mngr.map_simulation_settings(parameters)

    assert parameters[ssp.OUTPUTS][ssp.PLOTS] is False and (
        parameters[ssp.OUTPUTS][ssp.SITES]
        and parameters[ssp.OUTPUTS][ssp.TIMESERIES]
        and parameters[ssp.OUTPUTS][ssp.LEAKS]
        and parameters[ssp.OUTPUTS][ssp.BATCH_REPORTING]
    )


def test_045_make_plots_no_data(mocker, mock_parameter_make_plots_no_data):
    parameters = mock_parameter_make_plots_no_data

    mocker.patch.object(InputManager, "__init__", lambda self: None)

    input_mngr = InputManager()

    input_mngr.map_simulation_settings(parameters)

    assert parameters[ssp.OUTPUTS][ssp.PLOTS] is True and (
        not parameters[ssp.OUTPUTS][ssp.SITES]
        and not parameters[ssp.OUTPUTS][ssp.TIMESERIES]
        and not parameters[ssp.OUTPUTS][ssp.LEAKS]
        and not parameters[ssp.OUTPUTS][ssp.BATCH_REPORTING]
    )


def test_045_no_plots_no_write_data(mocker, mock_parameter_no_data_no_plots):
    parameters = mock_parameter_no_data_no_plots

    mocker.patch.object(InputManager, "__init__", lambda self: None)

    input_mngr = InputManager()

    input_mngr.map_simulation_settings(parameters)

    assert parameters[ssp.OUTPUTS][ssp.PLOTS] is False and (
        not parameters[ssp.OUTPUTS][ssp.SITES]
        and not parameters[ssp.OUTPUTS][ssp.TIMESERIES]
        and not parameters[ssp.OUTPUTS][ssp.LEAKS]
        and not parameters[ssp.OUTPUTS][ssp.BATCH_REPORTING]
    )
