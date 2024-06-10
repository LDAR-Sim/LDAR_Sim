"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_initialize_quantification_predictor.py
Purpose:    To test the initialization of the quantification predictor for a default sensor.

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
from sensors.default_sensor import DefaultSensor


def mock_default_sensor_init(self):
    pass


@pytest.mark.parametrize(
    "upper_range, lower_range, expected_sd, expected_centre",
    [
        (0.0, 1.0, 0.5, 0.5),
        (-1.0, 1.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (-1.0, 0.0, 0.5, -0.5),
    ],
)
def test_default_quantification_predictor_constructed_as_expected(
    monkeypatch, upper_range, lower_range, expected_sd, expected_centre
):
    monkeypatch.setattr(DefaultSensor, "__init__", mock_default_sensor_init)
    test_sensor: DefaultSensor = DefaultSensor()
    test_sensor.initialize_quantification_predictor(
        quantification_95_percent_ci_lower_range=lower_range,
        quantification_95_percent_ci_upper_range=upper_range,
        quantification_type="default",
    )
    assert test_sensor._quantification_predictor._quantification_standard_deviation == expected_sd
    assert test_sensor._quantification_predictor._quantification_centre == expected_centre


@pytest.mark.parametrize(
    "upper_range, lower_range",
    [
        (0.0, 1.0),
        (-1.0, 1.0),
        (0.0, 0.0),
        (-1.0, 0.0),
    ],
)
def test_uniform_quantification_predictor_constructed_as_expected(
    monkeypatch,
    upper_range,
    lower_range,
):
    monkeypatch.setattr(DefaultSensor, "__init__", mock_default_sensor_init)
    test_sensor: DefaultSensor = DefaultSensor()
    test_sensor.initialize_quantification_predictor(
        quantification_95_percent_ci_lower_range=lower_range,
        quantification_95_percent_ci_upper_range=upper_range,
        quantification_type="uniform",
    )

    assert test_sensor._quantification_predictor._lower_range == lower_range
    assert test_sensor._quantification_predictor._upper_range == upper_range
