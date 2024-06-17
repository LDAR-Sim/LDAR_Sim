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

import pandas as pd
import json
import pickle
import yaml
import sys
import os
from pathlib import Path
from typing import Any
import logging
from constants.error_messages import Input_Processing_Messages as ipm
from constants.general_const import File_Extension_Constants as fc


def file_reader(input_file_path: Path) -> Any:
    """
    Calls the proper file reader
    """
    data = None
    if not os.path.exists(input_file_path):
        print(ipm.MISSING_FILE_PATH_ERROR.format(file_path=str(input_file_path)))
        sys.exit()
    try:
        if input_file_path.suffix == fc.CSV:
            data = csv_reader(input_file_path)
        elif input_file_path.suffix == fc.JSON:
            data = json_reader(input_file_path)
        elif input_file_path.suffix == fc.PICKLE:
            data = pickle_reader(input_file_path)
        elif input_file_path.suffix == fc.YAML or input_file_path.suffix == fc.YML:
            data = yaml_reader(input_file_path)
        else:
            raise FileNotFoundError
    except FileNotFoundError as e:
        print(ipm.MISSING_FILE_ERROR.format(file=e))
        logging.error(ipm.MISSING_FILE_ERROR.format(file=e))
        raise
        # TODO: add better exception catching later
    except Exception as e:
        logging.error(ipm.GENERAL_FILE_READING_ERROR.format(file=e))
        print(ipm.GENERAL_FILE_READING_ERROR.format(file=e))
        raise
    return data


def csv_reader(input_file_path: Path) -> pd.DataFrame:
    """
    Reads in csv input files
    The expected file extension of the file passed to this file reader is .csv
    """

    # Check if the file has a .csv extension
    if input_file_path.suffix.lower() != fc.CSV:
        raise ValueError(ipm.EXPECTED_FILE_ERROR.format(file_type=fc.CSV))

    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv(input_file_path)
        return df
    except Exception as e:
        # Handle any exceptions that may occur during reading
        print(ipm.SPEC_FILE_READING_ERROR.format(file_type=fc.CSV, file=e))
        return pd.DataFrame()


def json_reader(input_file_path: Path) -> dict:
    """
    Reads in json input files
    The expected file extension of the file passed to this file reader is .json
    """
    # Check if the file has a .json extension
    if input_file_path.suffix.lower() != fc.JSON:
        raise ValueError(ipm.EXPECTED_FILE_ERROR.format(file_type=fc.JSON))

    # Read the JSON file into a dictionary
    try:
        with open(input_file_path, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        # Handle any exceptions that may occur during reading
        print(ipm.SPEC_FILE_READING_ERROR.format(file_type=fc.JSON, file=e))
        return {}


def pickle_reader(input_file_path: Path) -> Any:
    """
    Reads in pickle input files
    The expected file extension of the file passed to this file reader is .p
    CAUTION: Pickle file can contain any type of data and so this method can return any data type.
    We recommend that this is used ONLY to read in file where the contents of the file is known.
    """

    # Check if the file has a .p extension
    if input_file_path.suffix.lower() != fc.PICKLE:
        raise ValueError(ipm.EXPECTED_FILE_ERROR.format(file_type=fc.PICKLE))

    # Read the pickle file
    try:
        with open(input_file_path, "rb") as file:
            data = pickle.load(file)
        return data
    except Exception as e:
        # Handle any exceptions that may occur during reading
        print(ipm.SPEC_FILE_READING_ERROR.format(file_type=fc.PICKLE, file=e))
        return None


def yaml_reader(input_file_path: Path) -> dict:
    """
    Reads in yaml input files
    The expected file extension of the file passed to this file reader is .yml or .yaml
    """
    # Check if the file has a .yml or .yaml extension
    if input_file_path.suffix.lower() not in {fc.YML, fc.YAML}:
        raise ValueError(ipm.EXPECTED_FILE_ERROR.format(file_type=fc.YAML + " or " + fc.YML))

    # Read the YAML file
    try:
        with open(input_file_path, "r") as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        # Handle any exceptions that may occur during reading
        print(ipm.SPEC_FILE_READING_ERROR.format(file_type=fc.YAML, file=e))
        return None
