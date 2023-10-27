"""Tests for the map parameters method"""

from initialization.input_manager import InputManager
from testing.unit_testing.test_initialization.test_input_manager.input_manager_testing_fixtures import (  # Noqa: 401
    mock_parameter_program_level_fix,
    mock_parameter_sim_settings_fix,
)


def test_044_map_params_sim_settings(mocker, mock_parameter_sim_settings):
    mock_old_params = False
    mock_sim_settings_bool = True

    def mock_init(self, *args, **kwargs):
        self.old_params = mock_old_params

    def mock_map_sim_setting(self, *args, **kwargs):
        self.mock_sim_settings_called = mock_sim_settings_bool

    mocker.patch.object(InputManager, "__init__", mock_init)
    mocker.patch.object(InputManager, "handle_parameter_versioning", autospec=True)
    mocker.patch.object(InputManager, "map_simulation_settings", mock_map_sim_setting)
    input_mngr = InputManager()
    input_mngr.map_parameters(mock_parameter_sim_settings)
    assert input_mngr.mock_sim_settings_called is True


def test_044_map_params_prog_level(mocker, mock_parameter_program_level):
    mock_old_params = False
    mock_sim_settings_bool = True

    def mock_init(self, *args, **kwargs):
        self.old_params = mock_old_params

    def mock_map_sim_setting(self, *args, **kwargs):
        self.mock_sim_settings_called = mock_sim_settings_bool

    mocker.patch.object(InputManager, "__init__", mock_init)
    mocker.patch.object(InputManager, "handle_parameter_versioning", autospec=True)
    mocker.patch.object(InputManager, "map_simulation_settings", mock_map_sim_setting)
    input_mngr = InputManager()
    input_mngr.map_parameters(mock_parameter_program_level)
    assert not hasattr(input_mngr, "mock_sim_settings_bool")
