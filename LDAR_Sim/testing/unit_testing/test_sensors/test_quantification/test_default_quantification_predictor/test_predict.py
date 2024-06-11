import pytest
from sensors.quantification.default_quantification_predictor import DefaultQuantificationPredictor
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
def test_default_predict_gives_expected_output(
    monkeypatch, lower_range, upper_range, shift, true_rate, expected_measured_rate
):
    def mock_numpy_random_normal(loc: float, scale: float) -> float:
        return shift

    monkeypatch.setattr(numpy.random, "normal", mock_numpy_random_normal)

    test_quantification_predictor: DefaultQuantificationPredictor = DefaultQuantificationPredictor(
        lower_range, upper_range
    )
    measured_rate: float = test_quantification_predictor.predict(true_rate)

    assert measured_rate == expected_measured_rate
