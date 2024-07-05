"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_clean_propagating_parameters_from_equipment_info.py
Purpose:     Tests the cleaning of propagating parameters from equipment info


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
import pytest
from pytest_mock import MockerFixture
from virtual_world.equipment_groups import Equipment_Group
from constants.infrastructure_const import Infrastructure_Constants as IC


@pytest.mark.parametrize(
    "fixture_name",
    [
        "testing_data_equipment_info_with_propagating_parameters",
        "testing_data_equipment_info_without_propagating_parameters",
        "testing_data_equipment_info_with_method_specific_propagating_parameters",
        "testing_data_equipment_info_propagating_parameters_only",
    ],
)
def test_info_cleaned_as_expected(
    mocker: MockerFixture, request: pytest.FixtureRequest, fixture_name: str
):
    equipment_info, expected_cleaned_info = request.getfixturevalue(fixture_name)
    equipment_info: pd.Series
    expected_cleaned_info: pd.Series

    mocker.patch.object(Equipment_Group, "__init__", return_value=None)
    test_equipment: Equipment_Group = Equipment_Group()
    cleaned_info: pd.Series = test_equipment._clean_propagating_parameters_from_equipment_info(
        equipment_info
    )
    assert cleaned_info.equals(expected_cleaned_info)


@pytest.fixture(name="testing_data_equipment_info_with_propagating_parameters")
def testing_data_equipment_info_with_propagating_parameters_fixture():
    info_dict: dict = {
        "Test Comp1": 1,
        "Test Comp2": 2,
    }
    for val in IC.Equipment_Group_File_Constants.PROPAGATING_PARAMETER_COLUMNS:
        info_dict[val] = 0

    expected_cleaned_info_dict: dict = {
        "Test Comp1": 1,
        "Test Comp2": 2,
    }
    return (pd.Series(info_dict), pd.Series(expected_cleaned_info_dict))


@pytest.fixture(name="testing_data_equipment_info_without_propagating_parameters")
def testing_data_equipment_info_without_propagating_parameters_fixture():
    info_dict: dict = {
        "Test Comp1": 1,
        "Test Comp2": 2,
    }

    expected_cleaned_info_dict: dict = {
        "Test Comp1": 1,
        "Test Comp2": 2,
    }
    return (pd.Series(info_dict), pd.Series(expected_cleaned_info_dict))


@pytest.fixture(name="testing_data_equipment_info_with_method_specific_propagating_parameters")
def testing_data_equipment_info_with_method_specific_propagating_parameters_fixture():
    info_dict: dict = {
        "Test Comp1": 1,
        "Test Comp2": 2,
    }

    methods: list[str] = ["Method1", "Method2"]

    for method in methods:
        for (
            method_specific_param
        ) in IC.Equipment_Group_File_Constants.METHOD_SPECIFIC_PROPAGATING_PARAMETERS:
            info_dict[method + method_specific_param] = 0

    expected_cleaned_info_dict: dict = {
        "Test Comp1": 1,
        "Test Comp2": 2,
    }
    return (pd.Series(info_dict), pd.Series(expected_cleaned_info_dict))


@pytest.fixture(name="testing_data_equipment_info_propagating_parameters_only")
def testing_data_equipment_info_propagating_parameters_only_fixture():
    info_dict: dict = {}

    for val in IC.Equipment_Group_File_Constants.PROPAGATING_PARAMETER_COLUMNS:
        info_dict[val] = 0

    expected_cleaned_info_dict: dict = {}
    return (pd.Series(info_dict), pd.Series(expected_cleaned_info_dict, dtype="int64"))
