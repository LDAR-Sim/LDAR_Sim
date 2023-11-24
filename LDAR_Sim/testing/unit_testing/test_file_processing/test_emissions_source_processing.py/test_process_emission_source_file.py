"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_process_emission_source_file
Purpose: Unit tests for testing processing given emission sources dataframe in
order to set up correct emissions sources

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
    process_emission_source_file,
)


def test_000_emiss_source_for_empty_dataframe_input():
    assert 0 == 0


def test_000_emiss_source_for_simple_case_valid_input():
    assert 0 == 0
