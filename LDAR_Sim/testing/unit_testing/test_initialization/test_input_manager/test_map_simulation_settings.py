"""Test for the map_simulation_settings_method"""

from testing.unit_testing.test_initialization.test_input_manager.input_manager_testing_fixtures import (  # Noqa: 401
    mock_parameter_write_data_make_plots_fix,
    mock_parameter_make_plots_no_data_fix,
    mock_parameter_write_data_no_plots_fix,
    mock_parameter_no_data_no_plots_fix
)

from config.output_flag_mapping import OUTPUTS, SITES, TIMESERIES, LEAKS, PLOTS, BATCH_REPORTING

from initialization.input_manager import InputManager


def test_045_make_plots_write_data(
        mocker,
        mock_parameter_write_data_make_plots
):
    parameters = mock_parameter_write_data_make_plots

    mocker.patch.object(InputManager, '__init__', lambda self: None)

    input_mngr = InputManager()

    input_mngr.map_simulation_settings(parameters)

    assert (
        parameters[OUTPUTS][PLOTS] is True and
        (
            parameters[OUTPUTS][SITES] and
            parameters[OUTPUTS][TIMESERIES] and
            parameters[OUTPUTS][LEAKS] and
            parameters[OUTPUTS][BATCH_REPORTING]
        )
    )


def test_045_write_data_no_plots(
        mocker,
        mock_parameter_write_data_no_plots
):
    parameters = mock_parameter_write_data_no_plots

    mocker.patch.object(InputManager, '__init__', lambda self: None)

    input_mngr = InputManager()

    input_mngr.map_simulation_settings(parameters)

    assert (
        parameters[OUTPUTS][PLOTS] is False and
        (
            parameters[OUTPUTS][SITES] and
            parameters[OUTPUTS][TIMESERIES] and
            parameters[OUTPUTS][LEAKS] and
            parameters[OUTPUTS][BATCH_REPORTING]
        )
    )


def test_045_make_plots_no_data(
        mocker,
        mock_parameter_make_plots_no_data
):
    parameters = mock_parameter_make_plots_no_data

    mocker.patch.object(InputManager, '__init__', lambda self: None)

    input_mngr = InputManager()

    input_mngr.map_simulation_settings(parameters)

    assert (
        parameters[OUTPUTS][PLOTS] is True and
        (
            not parameters[OUTPUTS][SITES] and
            not parameters[OUTPUTS][TIMESERIES] and
            not parameters[OUTPUTS][LEAKS] and
            not parameters[OUTPUTS][BATCH_REPORTING]
        )
    )


def test_045_no_plots_no_write_data(
        mocker,
        mock_parameter_no_data_no_plots
):
    parameters = mock_parameter_no_data_no_plots

    mocker.patch.object(InputManager, '__init__', lambda self: None)

    input_mngr = InputManager()

    input_mngr.map_simulation_settings(parameters)

    assert (
        parameters[OUTPUTS][PLOTS] is False and
        (
            not parameters[OUTPUTS][SITES] and
            not parameters[OUTPUTS][TIMESERIES] and
            not parameters[OUTPUTS][LEAKS] and
            not parameters[OUTPUTS][BATCH_REPORTING]
        )
    )
