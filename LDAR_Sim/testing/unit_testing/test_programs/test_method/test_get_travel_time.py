import random
from typing import Any

import pytest
from programs.method import Method


def mock_method_init(self, travel_times: Any):
    self._travel_times = travel_times


@pytest.mark.parametrize(
    "travel_times, expected_travel_time",
    [
        (10, 10),
        (10.2, 10),
        ([10, 10], 10),
        ([10.3, 10.4], 10),
        ([10.6, 10.7, 10.8], 11),
    ],
)
def test_get_travel_time_always_int_for_valid_travel_times(
    monkeypatch, travel_times: Any, expected_travel_time: int
):
    monkeypatch.setattr(Method, "__init__", mock_method_init)

    random.seed(0)

    test_method: Method = Method(travel_times)

    travel_time: int = test_method._get_travel_time()
    assert isinstance(travel_time, int)
    assert travel_time == expected_travel_time
