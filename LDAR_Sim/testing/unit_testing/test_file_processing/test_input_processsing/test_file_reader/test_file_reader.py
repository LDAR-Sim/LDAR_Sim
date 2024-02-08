# """
# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        test_file_reader
# Purpose: Unit test for file_reader

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
# from pandas import DataFrame
# from file_processing.input_processing.file_reader import file_reader


# def test_file_reader_csv(mocker):
#     # Mocking the csv_reader function
#     mocker.patch(
#         "file_processing.input_processing.file_reader.csv_reader",
#         return_value=DataFrame({"col1": [1, 2], "col2": [3, 4]}),
#     )

#     # Running the file_reader function with a mocked csv_reader
#     result = file_reader("test.csv")

#     # Asserting that the result is a dictionary
#     assert isinstance(result, DataFrame)


# def test_file_reader_json(mocker):
#     # Mocking the json_reader function
#     mocker.patch(
#         "file_processing.input_processing.file_reader.json_reader",
#         return_value={"key1": "value1", "key2": "value2"},
#     )

#     # Running the file_reader function with a mocked json_reader
#     result = file_reader("test.json")

#     # Asserting that the result is a dictionary
#     assert isinstance(result, dict)


# def test_000_file_reader_pickle(mocker):
#     mocker.patch(
#         "file_processing.input_processing.file_reader.pickle_reader",
#         return_value={"key1": "value1", "key2": "value2"},
#     )
#     result = file_reader("test.p")
#     assert isinstance(result, dict)


# def test_000_file_reader_yaml(mocker):
#     mocker.patch(
#         "file_processing.input_processing.file_reader.yaml_reader",
#         return_value={"yaml_key": "yaml_value"},
#     )
#     result = file_reader("test.yml")
#     assert isinstance(result, dict)


# def test_file_reader_excepts_invalid_filetype_error_with_unsupported_file_type():
#     with pytest.raises(FileNotFoundError):
#         result = file_reader("test.txt")
