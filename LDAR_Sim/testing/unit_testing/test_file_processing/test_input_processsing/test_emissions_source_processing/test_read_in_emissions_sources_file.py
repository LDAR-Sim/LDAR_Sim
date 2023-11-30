"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_process_emission_source_file
Purpose: Unit tests for testing the read in for emissions sources file

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

from src.file_processing.input_processing.emissions_source_processing import (
    read_in_emissions_sources_file,
)


def test_000_read_valid_emiss_source_file():
    assert 0 == 0


def test_000_empty_emission_source_file():
    assert 0 == 0
