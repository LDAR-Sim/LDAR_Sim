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

from constants.infrastructure_const import Infrastructure_Constants as ic
from constants.error_messages import Input_Processing_Messages as ipm
from constants.param_default_const import Virtual_World_Params as VP


def read_in_infrastructure_files(virtual_world, in_dir: Path) -> dict[str, DataFrame]:
    input_dict: dict[str, DataFrame] = {}
    input_dict[ic.Virtual_World_Constants.SITES] = file_reader(
        in_dir / virtual_world[VP.INFRA][VP.SITE]
    )

    if virtual_world[VP.INFRA][VP.SITE_TYPE]:
        input_dict[ic.Virtual_World_Constants.SITE_TYPE] = file_reader(
            in_dir / virtual_world[VP.INFRA][VP.SITE_TYPE]
        )

    if virtual_world[VP.INFRA][VP.EQUIP]:
        input_dict[ic.Virtual_World_Constants.EQG] = file_reader(
            in_dir / virtual_world[VP.INFRA][VP.EQUIP]
        )

    if virtual_world[VP.INFRA][VP.SOURCE]:
        source_df: DataFrame = file_reader(in_dir / virtual_world[VP.INFRA][VP.SOURCE])
        if ic.Sources_File_Constants.PERSISTENT not in source_df.columns:
            source_df[ic.Sources_File_Constants.PERSISTENT] = True
            source_df[ic.Sources_File_Constants.ACTIVE_DUR] = 1
            source_df[ic.Sources_File_Constants.INACTIVE_DUR] = 0
            print(ipm.NO_PERSISTENT_FIELD_FOR_SOURCES_WARNING)
        input_dict[ic.Virtual_World_Constants.SOURCES] = source_df

    return input_dict


def check_site_file(input_dict):
    for header in ic.Sites_File_Constants.REQUIRED_HEADERS:
        if header not in input_dict[ic.Virtual_World_Constants.SITES]:
            print(ipm.MISSING_SITES_FILE_HEADER_ERROR.format(header=header))
            sys.exit()


def get_equip(row: Series, site_types_df: DataFrame):
    return site_types_df.loc[
        site_types_df[ic.Virtual_World_Constants.SITE_TYPE]
        == row[ic.Virtual_World_Constants.SITE_TYPE],
        ic.Virtual_World_Constants.EQG,
    ].iloc[0]
