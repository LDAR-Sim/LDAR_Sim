"""Module to test handle_parameter_version"""

import pytest
from file_processing.input_processing.input_manager import InputManager
from initialization.versioning import (
    LEGACY_PARAMETER_WARNING,
    MAJOR_VERSION_ONLY_WARNING,
    MINOR_VERSION_MISMATCH_WARNING,
)
from testing.unit_testing.test_initialization.test_input_manager.input_manager_testing_fixtures import (  # Noqa: 401
    mock_parameter_correct_maj_min_ver_fix,
    mock_parameter_incorrect_maj_ver_fix,
    mock_parameter_incorrect_min_ver_fix,
    mock_parameter_maj_only_ver_fix,
)


def test_043_test_correct_parameter_version(mocker, capsys, mock_parameter_correct_maj_min_ver):
    mock_old_params = False

    def mock_init(self, *args, **kwargs):
        self.old_params = mock_old_params

    mocker.patch.object(InputManager, "__init__", mock_init)
    input_mngr = InputManager()
    input_mngr.handle_parameter_versioning(mock_parameter_correct_maj_min_ver)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_043_test_incorrect_minor_parameter_version(
    mocker, capsys, mock_parameter_incorrect_min_ver
):
    mock_old_params = False

    def mock_init(self, *args, **kwargs):
        self.old_params = mock_old_params

    mocker.patch.object(InputManager, "__init__", mock_init)
    input_mngr = InputManager()
    input_mngr.handle_parameter_versioning(mock_parameter_incorrect_min_ver)
    captured = capsys.readouterr()
    expected_print_str = MINOR_VERSION_MISMATCH_WARNING + "\n"
    assert captured.out == expected_print_str and input_mngr.old_params is True


def test_043_test_incorrect_major_parameter_version(
    mocker, capsys, mock_parameter_incorrect_maj_ver
):
    mock_old_params = False

    def mock_init(self, *args, **kwargs):
        self.old_params = mock_old_params

    mocker.patch.object(InputManager, "__init__", mock_init)
    input_mngr = InputManager()

    with pytest.raises(SystemExit) as exc_info:
        input_mngr.handle_parameter_versioning(mock_parameter_incorrect_maj_ver)
    captured = capsys.readouterr()
    expected_print_str = LEGACY_PARAMETER_WARNING + "\n"
    assert exc_info.type == SystemExit and captured.out == expected_print_str


def test_043_test_only_major_parameter_version(mocker, capsys, mock_parameter_maj_only_ver):
    mock_old_params = False

    def mock_init(self, *args, **kwargs):
        self.old_params = mock_old_params

    mocker.patch.object(InputManager, "__init__", mock_init)
    input_mngr = InputManager()

    with pytest.raises(SystemExit) as exc_info:
        input_mngr.handle_parameter_versioning(mock_parameter_maj_only_ver)
    captured = capsys.readouterr()
    expected_print_str = MAJOR_VERSION_ONLY_WARNING + "\n"
    assert exc_info.type == SystemExit and captured.out == expected_print_str
