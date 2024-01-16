"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        sensor_constant_mapping.py
Purpose: Contains constants that are used for sensors

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
SENS_TYPE = "type"
SENS_QE = "QE"
SENS_MDL = "MDL"
SENS_MOD_LOC = "mod_loc"

ERR_MSG_UNKNOWN_SENS_TYPE = (
    "ERROR: LDAR-Sim could not resolve the provided sensor type for method: {method}."
    " Please enter a valid sensor type and try again."
)
