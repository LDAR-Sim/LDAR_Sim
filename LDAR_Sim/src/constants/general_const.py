"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        general_const.py
Purpose:     Holds general constants used in the program, such as units, file
extensions, etc.


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


class Version_Constants:
    CURRENT_MAJOR_VERSION = "4"

    CURRENT_MINOR_VERSION = "0"

    CURRENT_FULL_VERSION = "4.0"


class Unit_Constants:
    GRAM = "gram"
    KG = "kilogram"

    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class Dist_Constants:
    LOGNORM = "lognorm"


class File_Extension_Constants:
    PICKLE = ".p"
    YML = ".yml"
    YAML = ".yaml"
    JSON = ".json"
    CSV = ".csv"
