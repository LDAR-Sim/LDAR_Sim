"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_predict.py
Purpose:    To test the predict method of the UniformQuantificationPredictor class.

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

import pytest
from sensors.quantification.uniform_quantification_predictor import UniformQuantificationPredictor
import numpy.random


@pytest.mark.parametrize(
    "lower_range, upper_range, shift, true_rate, expected_measured_rate",
    [
        (0.0, 0.0, 0.0, 100.0, 100.0),
        (
            0.0,
            100.0,
            60.0,
            100.0,
            160.0,
        ),
        (-100.0, 0.0, -20.0, 100.0, 80.0),
        (-100.0, 100.0, -5.0, 100.0, 95.0),
    ],
)
def test_uniform_predict_gives_expected_output(
    monkeypatch, lower_range, upper_range, shift, true_rate, expected_measured_rate
):
    def mock_numpy_random_normal(loc: float, scale: float) -> float:
        return shift

    monkeypatch.setattr(numpy.random, "uniform", mock_numpy_random_normal)

    test_quantification_predictor: UniformQuantificationPredictor = UniformQuantificationPredictor(
        lower_range, upper_range
    )
    measured_rate: float = test_quantification_predictor.predict(true_rate)

    assert measured_rate == expected_measured_rate
