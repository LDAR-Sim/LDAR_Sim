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


class Multi_Sim_Output_Const:
    TS_PATTERN = re.compile(r".*timeseries\.csv$")
    EMIS_PATTERN = re.compile(r".*emissions_summary\.csv$")

    OUTPUTS_NAME_SIM_EXTRACTION_REGEX = re.compile(r"^(.*?)_(\d+)_.+.csv$")

    OUTPUT_KEEP_STR = "kept"
    OUTPUT_KEEP_REGEX = re.compile(re.escape(OUTPUT_KEEP_STR))

    PERCENTILE_95 = 95
    PERCENTILE_5 = 5
