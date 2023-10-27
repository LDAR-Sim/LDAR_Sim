# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        initialization.checks
# Purpose:     Checks for missing parameter files
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.

# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------


def for_program(trg, programs):
    has_trg = True
    if len([p["program_name"] for p in programs if p["program_name"] == trg]) < 1:
        print("Missing {} program...continuing".format(trg))
        has_trg = False
    return has_trg
