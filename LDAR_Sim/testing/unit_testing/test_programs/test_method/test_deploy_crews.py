"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_deploy_crews
Purpose: Unit test for testing the deployment of crews

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
from src.virtual_world.sites import Site
from testing.unit_testing.test_programs.test_method.method_testing_fixtures import (
    deploy_crews_testing_fix,
)


def test_000_simple_deployment_of_crews(deploy_crews_testing):
    (sites, properties, state, workplan) = deploy_crews_testing
    method = Method("test_method", properties, True, sites)
    method.deploy_crews(workplan, state)
    assert 0 == 0
