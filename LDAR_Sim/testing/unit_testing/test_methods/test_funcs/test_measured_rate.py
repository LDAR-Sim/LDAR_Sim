"""Test file to unit test funcs.py measured_rate functionality"""

import pytest
import numpy as np
from src.methods.funcs import measured_rate


@pytest.mark.parametrize("test_input, expected", [
    ([5, 0], 5),
    ([10, 0.5], 18.8),
    ([8, 0.3], 12.2),
])
def test_052_measured_rate(test_input, expected):
    np.random.seed(0)  # Setting a seed for reproducibility
    result = measured_rate(test_input[0], test_input[1])
    assert np.isclose(
        result, expected, rtol=1e-2), f"Test case failed: Expected {expected}, but got {result}"
