"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        error_messages.py
Purpose:     Holds error messages used throughout the program


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


class Input_Processing_Messages:
    INVALID_EMISSIONS_SOURCE_ERROR = (
        "Error, invalid emissions source information for source {source_name}"
    )

    MISSING_EMISSIONS_FILE_ERROR = (
        "Emissions file parameter is missing for the virtual world. "
        "Please provide a valid emissions file"
    )
    INVALID_EMISSIONS_SOURCE_FILE_VALUE_ERROR = (
        "Error: LDAR-Sim could not parse source file value: {value} from source:{source}."
        " Encountered exception: {exception}"
    )
    INVALID_EMISSIONS_VALUE: dict[str, str] = {
        "data": "Data Usage",
        "dist": "Distribution Type",
        "max_emis": "Maximum Emission Rate",
        "unit_amt": "Units (amount)",
        "unit_time": "Units (time)",
        "source": "Data source values",
    }

    MISSING_FILE_PATH_ERROR = "File {file_path} does not exist"
    MISSING_FILE_ERROR = "FileNotFoundError reading in file: {file}"
    GENERAL_FILE_READING_ERROR = "Error reading in file: {file}"
    EXPECTED_FILE_ERROR = "Expected file type: {file_type}"
    SPEC_FILE_READING_ERROR = "Error reading {file_type} file: {file}"

    MISSING_SITES_FILE_HEADER_ERROR = "The sites file is missing the column: {header}"

    NO_PERSISTENT_FIELD_FOR_SOURCES_WARNING = (
        "WARNING: The persistent field has not been provided for sources."
        "Assuming all sources are persistent."
    )

    ERR_MSG_UNKNOWN_SENS_TYPE = (
        "ERROR: LDAR-Sim could not resolve the provided sensor type for method: {method}."
        " Please enter a valid sensor type and try again."
    )

    VALID_REPAIR_DELAY_TYPE_ERROR = (
        "Error: Double check the contents of the repair delay file."
        " A numerical value was provided as a repair delay"
    )


class Output_Processing_Messages:
    OPERAND_ADDITION_ERROR = "Unsupported operand type for addition"
    OPERAND_INPLACE_ADDITION_ERROR = "Unsupported operand type for in-place addition"
