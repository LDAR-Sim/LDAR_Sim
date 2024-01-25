"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        repair_delay_processing
Purpose: Module for processing User defined repair delay sources from a file

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


import sys
from pandas import DataFrame, read_csv
from pathlib import WindowsPath

REPAIR = "repairs"
DELAY = "delay"
VALID_REPAIR_DELAY_TYPE_ERROR = (
    "Error: Double check the contents of the repair delay file."
    " A numerical value was provided as a repair delay"
)


def read_in_repair_delay_sources_file(
    inputs_path: WindowsPath,
    virtual_world: dict,
) -> None | DataFrame:
    """Get the location for the repair delay source file and read the file into a pandas DataFrame

    Args

    Returns

    """
    filename: str = virtual_world[REPAIR][DELAY]["file"]
    if filename is not None:
        filepath: WindowsPath = inputs_path / filename
        repair_delay_file: DataFrame = read_csv(filepath)
        valid_repair_delay_type = "int64"
        all_repair_types_valid = all(repair_delay_file.dtypes == valid_repair_delay_type)
        if not all_repair_types_valid:
            print(VALID_REPAIR_DELAY_TYPE_ERROR)
            sys.exit()
        return repair_delay_file
    return None
