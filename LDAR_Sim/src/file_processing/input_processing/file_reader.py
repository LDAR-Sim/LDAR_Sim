"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        file_reader
Purpose: Module for file reading

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
from typing import Any
from pandas import DataFrame


def file_reader(input_file_path: Path) -> dict or DataFrame:
    """
    Calls the proper file reader
    """
    data = None
    try:
        if ".csv" in input_file_path:
            data = csv_reader(input_file_path)
        elif ".json" in input_file_path:
            data = json_reader(input_file_path)
        elif ".p" in input_file_path:
            data = pickle_reader()(input_file_path)
        elif ".yml" or ".yaml" in input_file_path:
            data = yaml_reader(input_file_path)
    except Exception as e:
        print(f"Error reading in file: {e}")
        # TODO: add better exception catching later
    return data


def csv_reader(input_file_path: Path) -> DataFrame:
    """
    Reads in csv input files
    The expected file extension of the file passed to this file reader is .csv
    """

    return None


def json_reader(input_file_path: Path) -> dict:
    """
    Reads in json input files
    The expected file extension of the file passed to this file reader is .json
    """
    return None


def pickle_reader(input_file_path: Path) -> Any:
    """
    Reads in pickle input files
    The expected file extension of the file passed to this file reader is .p
    CAUTION: Pickle file can contain any type of data and so this method can return any data type.
    We recommend that this is used ONLY to read in file where the contents of the file is known.
    """

    return None


def yaml_reader(input_file_path: Path) -> dict:
    """
    Reads in yaml input files
    The expected file extension of the file passed to this file reader is .yml or .yaml
    """

    return None
