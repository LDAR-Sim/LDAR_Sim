"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        input_processing_const.py
Purpose:     Holds constants used in input processing


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

import re


class Emissions_Source_Processing_Const:
    EMISSION_FILE = "emissions_file"
    EMISSION = "emissions"

    SAMPLE_MATCH = r"\s*sample\s*"
    DIST_MATCH = r"\s*dist\s*"

    SAMPLE_REGEX = re.compile(SAMPLE_MATCH, re.IGNORECASE)
    DIST_REGEX = re.compile(DIST_MATCH, re.IGNORECASE)
