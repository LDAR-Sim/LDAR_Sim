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

from pandas import DataFrame
from file_processing.input_processing.file_reader import file_reader


def read_in_infrastructure_files(virtual_world, in_dir: Path) -> dict[str, DataFrame]:
    input_dict = {}
    input_dict["sites"] = file_reader(
        in_dir / virtual_world["infrastructure"]["sites_file"]
    )

    if virtual_world["infrastructure"]["site_type_file"]:
        input_dict["site_types"] = file_reader(
            in_dir / virtual_world["infrastructure"]["site_type_file"]
        )

    if virtual_world["infrastructure"]["equipment_group_file"]:
        input_dict["equipment_groups"] = file_reader(
            in_dir / virtual_world["infrastructure"]["equipment_group_file"]
        )

    if virtual_world["infrastructure"]["sources_file"]:
        input_dict["sources"] = file_reader(
            in_dir / virtual_world["infrastructure"]["sources_file"]
        )

    return input_dict
