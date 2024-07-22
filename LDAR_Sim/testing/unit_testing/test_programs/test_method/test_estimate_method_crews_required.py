"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_estimate_method_crews_required
Purpose: Unit test for testing the estimation of the number of crews required
for surveys

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

from src.programs.method import Method
from testing.unit_testing.test_programs.test_method.method_testing_fixtures import (  # noqa
    simple_method_values_fix,
    simple_method_values2_fix,
    simple_method_values3_fix,
)
from src.virtual_world.infrastructure import Site


def test_000_return_provided_value(simple_method_values):
    mocker, properties, current_date, state = simple_method_values
    sites = [mocker.Mock(spec=Site) for i in range(5)]
    method = Method("test_method", properties, True, sites, None)

    expected_crews_required = 3
    assert method._crews == expected_crews_required


def test_000_return_estimated_not_followup(simple_method_values2):
    mocker, properties, current_date, state = simple_method_values2
    sites = [mocker.Mock(spec=Site) for i in range(500)]
    method = Method("test_method", properties, True, sites, None)

    expected_crews_required = 3
    assert method._crews == expected_crews_required


def test_000_return_estimate_1_if_followup(simple_method_values3):
    mocker, properties, current_date, state = simple_method_values3
    sites = [mocker.Mock(spec=Site) for i in range(5)]
    method = Method("test_method", properties, True, sites, None)

    expected_crews_required = 1
    assert method._crews == expected_crews_required
