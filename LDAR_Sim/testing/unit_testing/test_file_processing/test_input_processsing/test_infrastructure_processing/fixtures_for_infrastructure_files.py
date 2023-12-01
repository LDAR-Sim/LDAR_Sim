"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        fixtures_for_infrastructure_files
Purpose: Fixtures for testing read in infrastructure files

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
import pytest
from pathlib import Path


@pytest.fixture(name="virtual_world")
def virtual_world_fix():
    return {
        "infrastructure": {
            "sites_file": "sites.csv",
            "site_type_file": "site_types.csv",
            "equipment_group_file": "equipment_groups.csv",
            "sources_file": "sources.csv",
        }
    }


@pytest.fixture(name="in_dir")
def in_dir_fix(tmp_path):
    # TODO: Use a temporary directory for testing
    return tmp_path
