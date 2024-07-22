"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_predict.py
Purpose:    To test the predict method of the SamplingQuantificationPredictor class.

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

import numpy as np
import pytest
from sensors.quantification.sampling_quantification_predictor import SamplingQuantificationPredictor
import numpy.random


@pytest.mark.parametrize(
    "shift, true_rate, expected_measured_rate",
    [
        (0.0, 100.0, 100.0),
        (
            60.0,
            100.0,
            160.0,
        ),
        (-20.0, 100.0, 80.0),
        (-5.0, 100.0, 95.0),
        (-150.0, 100.0, 0.0),
    ],
)
def test_predict_correctly_applies_shift(monkeypatch, shift, true_rate, expected_measured_rate):

    def mock_SamplingQuantificationPredictor_init(self, quantification_file, quantification_column):
        self._quantification_errors = numpy.array([shift])

    monkeypatch.setattr(
        SamplingQuantificationPredictor,
        "__init__",
        mock_SamplingQuantificationPredictor_init,
    )

    test_quantification_predictor: SamplingQuantificationPredictor = (
        SamplingQuantificationPredictor("test_file", "test_column")
    )
    measured_rate: float = test_quantification_predictor.predict(true_rate)

    assert measured_rate == expected_measured_rate


def test_predict_correctly_samples_from_possible_errors(monkeypatch):
    np.random.seed(0)
    quantification_errors: list[float] = [-75, -50, 0, 50, 75]

    def mock_SamplingQuantificationPredictor_init(self, quantification_file, quantification_column):
        self._quantification_errors = numpy.array(quantification_errors)

    monkeypatch.setattr(
        SamplingQuantificationPredictor,
        "__init__",
        mock_SamplingQuantificationPredictor_init,
    )

    test_rate: float = 100.0

    test_quantification_predictor: SamplingQuantificationPredictor = (
        SamplingQuantificationPredictor("test_file", "test_column")
    )

    possible_quantified_rates: list[float] = [25, 50, 100, 150, 175]

    quantified_rates: list[float] = []

    for _ in range(1000):

        measured_rate: float = test_quantification_predictor.predict(test_rate)

        quantified_rates.append(measured_rate)

        assert measured_rate in possible_quantified_rates

    assert np.mean(quantified_rates) == pytest.approx(test_rate, rel=0.1)
