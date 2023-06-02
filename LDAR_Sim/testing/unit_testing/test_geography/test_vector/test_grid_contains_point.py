""" Unit test for testing vector.py"""

import pytest
from src.geography.vector import grid_contains_point


@pytest.mark.parametrize("test_input, expected", [
    ([[0.0, 0.0], [[0.0, 0.0], [0.0, 0.0]]], (True, None)),
    ([[0.0, 0.0], [[1.0, 1.0, 2, 2], [0.0, 0.0, 0.0, 0.0]]], (False, 'Simulation terminated: One or more sites is too ' +
                                                              'far South and is outside the spatial bounds of ' +
                                                              'your grid data!')),
    ([[0.0, 0.0], [[-1.0, -1.0, -2, -2], [0.0, 0.0, 0.0, 0.0]]], (False, 'Simulation terminated: One or more sites is too ' +
                                                                  'far North and is outside the spatial bounds of ' +
                                                                  'your grid data!')),
    ([[0.0, 0.0], [[0.0, 0.0, 0.0, 0.0], [-1.0, -1.0, -2, -2]]], (False, 'Simulation terminated: One or more sites is too ' +
                                                                  'far East and is outside the spatial bounds of ' +
                                                                  'your grid data!')),
    ([[0.0, 0.0], [[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 2, 2]]], (False, 'Simulation terminated: One or more sites is too ' +
                                                              'far West and is outside the spatial bounds of ' +
                                                              'your grid data!'))
])
def test_012_grid_contains_point(test_input, expected):
    """Tests grid cointains point"""
    result = grid_contains_point(test_input[0], test_input[1])
    assert expected == result
