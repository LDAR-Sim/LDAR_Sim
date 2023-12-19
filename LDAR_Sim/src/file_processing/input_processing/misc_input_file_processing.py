"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        misc_input_file_processing
Purpose: Module for processing user defined input files, mostly used for sampled values

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

from pathlib import Path
from src.file_processing.input_processing.file_reader import file_reader


def save_repair_cost(file_loc: Path) -> list[float]:
    """
    Function to parse out repair cost if values are provided in file

    Arg:
        File location

    Returns:
        list[floats]: a list of repair cost values as floats
    """
    repair_costs = file_reader(file_loc)
    return None


def save_time_between_sites(file_loc: Path) -> list[float]:
    """
    Function to parse out possible time between site values, if provided as file

    Arg:
        File location :

    Returns:
        list[floats]: a list of possible time between site values
    """
    t_btw_sites = file_reader(file_loc)
    return None


def save_home_base_location(params: dict) -> list[tuple[float, float]]:
    """
    Function to parse out potential home base locations, when provided

    Arg:
        File location

    Returns:
        list[tuple[float,float]]: a list of lat,lon home base locations
    """
    # TODO: to fill out and use when routing is implemented.
    return None
