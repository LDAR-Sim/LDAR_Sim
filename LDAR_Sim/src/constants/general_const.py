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

from dataclasses import dataclass


@dataclass
class Version_Constants:
    CURRENT_MAJOR_VERSION = "4"

    CURRENT_MINOR_VERSION = "0"

    CURRENT_FULL_VERSION = "4.0"


@dataclass
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


@dataclass
class Conversion_Constants:
    GRAMS_PER_SECOND_TO_KG_PER_DAY = 86.4
    GS_TO_GH = 3600
    DAYS_IN_MONTH = 30.437
    GS_TO_KGHR = 3.6
    KG_TO_MMBTU = 0.0543121421


@dataclass
class Dist_Constants:
    LOGNORM = "lognorm"


@dataclass
class File_Extension_Constants:
    PICKLE = ".p"
    YML = ".yml"
    YAML = ".yaml"
    JSON = ".json"
    CSV = ".csv"


@dataclass
class Emission_Constants:
    REPAIRABLE = "repairable"
    NON_REPAIRABLE = "non-repairable"
    REP_PREFIX = "repairable_"
    NON_REP_PREFIX = "non_repairable_"
    EXPIRE = "expired"
    ACTIVE = "active"
    INACTIVE = "inactive"
    REPAIRED = "repaired"
    NATURAL = "natural"


@dataclass
class Placeholder_Constants:
    PLACEHOLDER_EQUIPMENT = "Placeholder_Equipment"
    PLACEHOLDER_REP_EQUIPMENT = "Placeholder_Rep_Equipment"
    PLACEHOLDER_NON_EQUIPMENT = "Placeholder_NonRep_Equipment"
    PLACEHOLDER_INT = "_placeholder_int_"
    PLACEHOLDER_FLOAT = "_placeholder_float_"
    PLACEHOLDER_STR = "_placeholder_str_"
