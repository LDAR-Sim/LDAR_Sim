"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_get_travel_time.py
Purpose: Unit test for testing the get_travel_time method in the Method class

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
