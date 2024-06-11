"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        prog_cost_param_parser.py
Purpose:     Contains function to parse program cost parameters

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


def parse_program_cost_info(programs: dict) -> dict[str, list[float]]:
    program_cost_info = {}
    for program_name, program in programs.items():
        program_cost_info[program_name] = program.get("economics")

    return program_cost_info
