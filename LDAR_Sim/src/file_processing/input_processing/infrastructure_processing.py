"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        infrastructure_processing.py
Purpose: Module for processing user defined simulation infrastructure

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
import sys
from pandas import DataFrame, Series
from file_processing.input_processing.file_reader import file_reader

from virtual_world.infrastructure_const import Infrastructure_Constants as ic

MISSING_SITES_FILE_HEADER_ERROR = "The sites file is missing the column: {}"

NO_PERSISTENT_FIELD_FOR_SOURCES_WARNING = (
    "WARNING: The persistent field has not been provided for sources."
    "Assuming all sources are persistent."
)


def read_in_infrastructure_files(virtual_world, in_dir: Path) -> dict[str, DataFrame]:
    input_dict: dict[str, DataFrame] = {}
    input_dict["sites"] = file_reader(in_dir / virtual_world["infrastructure"]["sites_file"])

    if virtual_world["infrastructure"]["site_type_file"]:
        input_dict["site_types"] = file_reader(
            in_dir / virtual_world["infrastructure"]["site_type_file"]
        )

    if virtual_world["infrastructure"]["equipment_group_file"]:
        input_dict["equipment"] = file_reader(
            in_dir / virtual_world["infrastructure"]["equipment_group_file"]
        )

    if virtual_world["infrastructure"]["sources_file"]:
        source_df: DataFrame = file_reader(in_dir / virtual_world["infrastructure"]["sources_file"])
        if ic.Sources_File_Constants.PERSISTENT not in source_df.columns:
            source_df[ic.Sources_File_Constants.PERSISTENT] = True
            source_df[ic.Sources_File_Constants.ACTIVE_DUR] = 1
            source_df[ic.Sources_File_Constants.INACTIVE_DUR] = 0
            print(NO_PERSISTENT_FIELD_FOR_SOURCES_WARNING)
        input_dict["sources"] = source_df

    return input_dict


def check_site_file(input_dict):
    for header in ic.Sites_File_Constants.REQUIRED_HEADERS:
        if header not in input_dict["sites"]:
            print(MISSING_SITES_FILE_HEADER_ERROR.format(header=header))
            sys.exit()


def get_equip(row: Series, site_types_df: DataFrame):
    return site_types_df.loc[
        site_types_df[ic.Site_Type_File_Constants.TYPE] == row[ic.Sites_File_Constants.TYPE],
        ic.Site_Type_File_Constants.EQG,
    ].iloc[0]


# def get_equip(row: Series, site_types_df: DataFrame):
#     site_type = row[ic.Sites_File_Constants.TYPE]
#     filtered_df = site_types_df.loc[
#         site_types_df[ic.Site_Type_File_Constants.TYPE] == site_type,
#         ic.Site_Type_File_Constants.EQG,
#     ]
#     if not filtered_df.empty:
#         return filtered_df.iloc[0].item()
#     return None
