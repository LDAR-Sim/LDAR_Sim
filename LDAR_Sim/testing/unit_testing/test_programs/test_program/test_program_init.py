"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_program_init.py
Purpose: To unit test program initialization

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

from datetime import date
from programs.program import Program  # replace with the actual module name
from constants.param_default_const import Program_Params, Duration_Method


def test_000_simple_program_init(mocker):
    # Define the inputs
    name = "Test Program"
    weather = "Sunny"
    daylight = "Day"
    methods = {"method1": {}, "method2": {}}
    sites = ["Site1", "Site2"]
    sim_start_date = date(2022, 1, 1)
    sim_end_date = date(2022, 12, 31)
    consider_weather = True
    prog_params = {
        Program_Params.DURATION_ESTIMATE: {
            Program_Params.DURATION_FACTOR: 1.0,
            Program_Params.DURATION_METHOD: Duration_Method.COMPONENT,
        }
    }

    # Mock _init_methods_and_schedules
    mocker.patch.object(Program, "_init_methods_and_schedules", return_value=None)

    # Create an instance of Program
    program = Program(
        name,
        weather,
        daylight,
        methods,
        sites,
        sim_start_date,
        sim_end_date,
        consider_weather,
        prog_params,
    )

    # Assert that the properties are as expected
    assert program.name == name
    assert program.weather == weather
    assert program.daylight == daylight
    assert program.method_names == list(methods.keys())
    assert program._current_date == sim_start_date
    assert program.duration_factor == 1.0
    assert program.duration_method == Duration_Method.COMPONENT
