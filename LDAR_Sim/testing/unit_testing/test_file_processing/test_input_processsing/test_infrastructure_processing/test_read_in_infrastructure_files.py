# """
# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        test_read_in_infrastructure_files
# Purpose: Unit test for reading in infrastructure files

# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.
# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.

# ------------------------------------------------------------------------------
# """
# import pytest
# from unittest.mock import Mock
# from pandas import DataFrame
# from testing.unit_testing.test_file_processing.test_input_processsing.test_infrastructure_processing.fixtures_for_infrastructure_files import (
#     virtual_world_fix,
#     in_dir_fix,
# )
# from src.file_processing.input_processing.infrastructure_processing import (
#     read_in_infrastructure_files,
# )
# from src.file_processing.input_processing.file_reader import file_reader


# def test_read_in_infrastructure_files_with_all_files(virtual_world, in_dir):
#     # Mocking file_reader to return a DataFrame
#     mock_file_reader = Mock(return_value=DataFrame({"col1": [1, 2], "col2": [3, 4]}))

#     with pytest.MonkeyPatch().context() as m:
#         m.setattr("src.file_processing.input_processing.file_reader", mock_file_reader)

#         result = read_in_infrastructure_files(virtual_world, in_dir)

#     assert "sites" in result
#     assert "site_types" in result
#     assert "equipment_groups" in result
#     assert "sources" in result

#     assert isinstance(result["sites"], DataFrame)
#     assert isinstance(result["site_types"], DataFrame)
#     assert isinstance(result["equipment_groups"], DataFrame)
#     assert isinstance(result["sources"], DataFrame)

#     # Make assertions about the call arguments for each file_reader
#     mock_file_reader.assert_any_call(in_dir / "sites.csv")
#     mock_file_reader.assert_any_call(in_dir / "site_types.csv")
#     mock_file_reader.assert_any_call(in_dir / "equipment_groups.csv")
#     mock_file_reader.assert_any_call(in_dir / "sources.csv")


# def test_read_in_infrastructure_files_with_optional_files(virtual_world, in_dir):
#     # Mocking file_reader to return a DataFrame
#     mock_file_reader = Mock(return_value=DataFrame({"col1": [1, 2], "col2": [3, 4]}))

#     with pytest.MonkeyPatch().context() as m:
#         m.setattr("src.file_processing.input_processing.file_reader", mock_file_reader)

#         # Set optional files to None
#         virtual_world["infrastructure"]["site_type_file"] = None
#         virtual_world["infrastructure"]["equipment_group_file"] = None
#         virtual_world["infrastructure"]["sources_file"] = None

#         result = read_in_infrastructure_files(virtual_world, in_dir)

#     assert "sites" in result
#     assert "site_types" not in result
#     assert "equipment_groups" not in result
#     assert "sources" not in result

#     assert isinstance(result["sites"], DataFrame)

#     # Make assertions about the call arguments for each file_reader
#     mock_file_reader.assert_any_call(in_dir / "sites.csv")
#     mock_file_reader.assert_not_called()  # Ensure optional file_readers were not called
