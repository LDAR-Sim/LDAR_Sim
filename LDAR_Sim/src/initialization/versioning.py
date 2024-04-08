# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        initialization.versioning
# Purpose:     Checks for the versions of the parameter files
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


def check_major_version(version_string, major_version):
    try:
        major_part, _ = map(int, version_string.split("."))
        major_version = int(major_version)

        if major_part < major_version:
            return -1
        elif major_part == major_version:
            return 0
        else:
            return 1
    except ValueError:
        return False


CURRENT_MAJOR_VERSION = "4"

CURRENT_MINOR_VERSION = "0"

CURRENT_FULL_VERSION = "4.0"
