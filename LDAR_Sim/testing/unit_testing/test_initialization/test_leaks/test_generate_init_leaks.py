"""
Module to test generate_initial_leaks
"""

from src.initialization.leaks import generate_initial_leaks
from testing.unit_testing.test_initialization.test_leaks.leak_testing_fixtures import (
    mock_site_for_leak_test_fix,
    mock_site_w_leak_test_fix,
    mock_program_fix,
    mock_program_2_fix,
)


def test_042_initialize_leaks(mock_site_for_leak_test, mock_program, mock_site_w_leak_test, mocker):
    mocker.patch('src.initialization.leaks.random.binomial', return_value=1)
    mocker.patch('src.initialization.leaks.random.randint', return_value=0)

    # Call the function under test
    result = generate_initial_leaks(mock_program, mock_site_for_leak_test)

    # Assert the expected result
    assert result == mock_site_w_leak_test


def test_042_initialize_leaks_2(mock_site_for_leak_test, mock_program_2, mock_site_w_leak_test, mocker):
    mocker.patch('src.initialization.leaks.random.binomial', return_value=1)
    mocker.patch('src.initialization.leaks.random.randint', return_value=0)

    # Call the function under test
    result = generate_initial_leaks(mock_program_2, mock_site_for_leak_test)

    # Assert the expected result
    assert result == mock_site_w_leak_test
