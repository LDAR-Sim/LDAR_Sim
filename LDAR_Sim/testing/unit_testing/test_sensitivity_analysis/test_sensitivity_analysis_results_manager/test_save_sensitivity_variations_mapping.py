# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        test_save_sensitivity_variations_mapping.py
# Purpose:     To test the save_sensitivity_variations_mapping method
#              in the SensitivityAnalysisResultsManager class.
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published
# by the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# MIT License for more details.


# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.
#
# ------------------------------------------------------------------------------

from typing import Any
from constants.param_default_const import (
    Virtual_World_Params,
    Levels,
    Method_Params,
    Program_Params,
)
from sensitivity_analysis.sensitivity_analysis_results_manager import (
    SensitivityAnalysisResultsManager,
)
import pandas as pd

from constants.sensitivity_analysis_constants import SensitivityAnalysisOutputs

import sys


def mock_init_sensitivity_analysis_results_manager(
    self, param_sens_mappings: dict[str, Any], sens_level: str
):
    self._parameter_variations = param_sens_mappings
    self._sens_level = sens_level
    self._out_dir = "test"


def get_vw_params_mapping1():
    return {
        Virtual_World_Params.EMIS: [
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.000275}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.0065}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.013}},
        ]
    }, 3


def get_expected_vw_Sens_mappings_1():
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FIXED_COLUMN_NAMES[0]: [
                0,
                1,
                2,
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=0): [
                Virtual_World_Params.EMIS
                + "."
                + Virtual_World_Params.REPAIRABLE
                + "."
                + Virtual_World_Params.PR
            ]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=0): [0.000275, 0.0065, 0.013],
        }
    )


def get_vw_params_mapping2():
    return {
        Virtual_World_Params.EMIS: [
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.ERS: "test1"}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.000275}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.ERS: "test2"}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.0065}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.ERS: "test3"}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.013}},
        ]
    }, 3


def get_expected_vw_Sens_mappings_2():
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FIXED_COLUMN_NAMES[0]: [
                0,
                1,
                2,
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=0): [
                Virtual_World_Params.EMIS
                + "."
                + Virtual_World_Params.REPAIRABLE
                + "."
                + Virtual_World_Params.ERS
            ]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=0): ["test1", "test2", "test3"],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=1): [
                Virtual_World_Params.EMIS
                + "."
                + Virtual_World_Params.REPAIRABLE
                + "."
                + Virtual_World_Params.PR
            ]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=1): [0.000275, 0.0065, 0.013],
        }
    )


def get_vw_params_mapping3():
    return {
        Virtual_World_Params.WEATHER_FILE: [
            "test_weather_file1",
            "test_weather_file2",
            "test_weather_file3",
        ],
        Virtual_World_Params.CONSIDER_WEATHER: [
            False,
            True,
            False,
        ],
    }, 3


def get_expected_vw_Sens_mappings_3():
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FIXED_COLUMN_NAMES[0]: [
                0,
                1,
                2,
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=0): [Virtual_World_Params.WEATHER_FILE]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=0): [
                "test_weather_file1",
                "test_weather_file2",
                "test_weather_file3",
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=1): [Virtual_World_Params.CONSIDER_WEATHER]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=1): [False, True, False],
        }
    )


def get_program_params_mapping_1():
    return (
        {
            "test_prog1": {
                Program_Params.DURATION_ESTIMATE: [
                    {Program_Params.DURATION_FACTOR: 0.1},
                    {Program_Params.DURATION_FACTOR: 0.5},
                    {Program_Params.DURATION_FACTOR: 1.0},
                ]
            },
        },
        3,
    )


def get_expected_program_Sens_mappings_1() -> pd.DataFrame:
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FIXED_COLUMN_NAMES[0]: [
                0,
                1,
                2,
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=0): [
                "test_prog1."
                + Program_Params.DURATION_ESTIMATE
                + "."
                + Program_Params.DURATION_FACTOR
            ]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=0): [0.1, 0.5, 1.0],
        }
    )


def get_program_params_mapping_2():
    return (
        {
            "test_prog1": {
                Program_Params.DURATION_ESTIMATE: [
                    {Program_Params.DURATION_FACTOR: 0.1},
                    {Program_Params.DURATION_FACTOR: 0.5},
                    {Program_Params.DURATION_FACTOR: 1.0},
                ],
                Program_Params.ECONOMICS: [
                    {Program_Params.TCO2E: 10},
                    {Program_Params.TCO2E: 20},
                    {Program_Params.TCO2E: 30},
                ],
            },
            "test_prog2": {
                Program_Params.DURATION_ESTIMATE: [
                    {Program_Params.DURATION_FACTOR: 0.1},
                    {Program_Params.DURATION_FACTOR: 0.2},
                    {Program_Params.DURATION_FACTOR: 0.3},
                ],
                Program_Params.ECONOMICS: [
                    {Program_Params.TCO2E: 20},
                    {Program_Params.TCO2E: 40},
                    {Program_Params.TCO2E: 60},
                ],
            },
        },
        3,
    )


def get_expected_program_Sens_mappings_2() -> pd.DataFrame:
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FIXED_COLUMN_NAMES[0]: [
                0,
                1,
                2,
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=0): [
                "test_prog1."
                + Program_Params.DURATION_ESTIMATE
                + "."
                + Program_Params.DURATION_FACTOR
            ]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=0): [0.1, 0.5, 1.0],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=1): ["test_prog1." + Program_Params.ECONOMICS + "." + Program_Params.TCO2E]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=1): [10, 20, 30],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=2): [
                "test_prog2."
                + Program_Params.DURATION_ESTIMATE
                + "."
                + Program_Params.DURATION_FACTOR
            ]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=2): [0.1, 0.2, 0.3],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=3): ["test_prog2." + Program_Params.ECONOMICS + "." + Program_Params.TCO2E]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=3): [20, 40, 60],
        }
    )


def get_method_params_mapping_1():
    return {
        "test_method3": {
            Method_Params.COVERAGE: [
                {Method_Params.SPATIAL: 0.1},
                {Method_Params.TEMPORAL: 0.3},
                {Method_Params.SPATIAL: 0.2},
                {Method_Params.TEMPORAL: 0.5},
                {Method_Params.SPATIAL: 0.3},
                {Method_Params.TEMPORAL: 0.7},
            ]
        }
    }, 3


def get_expected_method_Sens_mappings_1():
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FIXED_COLUMN_NAMES[0]: [
                0,
                1,
                2,
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=0): ["test_method3." + Method_Params.COVERAGE + "." + Method_Params.SPATIAL]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=0): [0.1, 0.2, 0.3],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=1): ["test_method3." + Method_Params.COVERAGE + "." + Method_Params.TEMPORAL]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=1): [0.3, 0.5, 0.7],
        }
    )


def get_method_params_mapping_2():
    return {
        "test_method3": {Method_Params.RS: [1, 2, 3, 4, 5]},
        "test_method4": {Method_Params.RS: [2, 4, 6, 8, 10]},
    }, 5


def get_expected_method_Sens_mappings_2():
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FIXED_COLUMN_NAMES[0]: [
                0,
                1,
                2,
                3,
                4,
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=0): ["test_method3." + Method_Params.RS]
            * 5,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=0): [1, 2, 3, 4, 5],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=1): ["test_method4." + Method_Params.RS]
            * 5,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=1): [2, 4, 6, 8, 10],
        }
    )


def get_method_params_mapping_3():
    return {
        "test_method3": {
            Method_Params.RS: [1, 2, 3],
            Method_Params.COVERAGE: [
                {Method_Params.SPATIAL: 0.1},
                {Method_Params.SPATIAL: 0.2},
                {Method_Params.SPATIAL: 0.3},
            ],
        },
    }, 3


def get_expected_method_Sens_mappings_3():
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FIXED_COLUMN_NAMES[0]: [
                0,
                1,
                2,
            ],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=0): ["test_method3." + Method_Params.RS]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=0): [1, 2, 3],
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                0
            ].format(x=1): ["test_method3." + Method_Params.COVERAGE + "." + Method_Params.SPATIAL]
            * 3,
            SensitivityAnalysisOutputs.SensitivityVariationsMapping.FLEXIBLE_COLUMNS_NAMES[
                1
            ].format(x=1): [0.1, 0.2, 0.3],
        }
    )


def test_save_sensitivity_variations_mapping_vw(monkeypatch):
    param_variations, num_variations = get_vw_params_mapping1()
    monkeypatch.setattr(
        SensitivityAnalysisResultsManager,
        "__init__",
        mock_init_sensitivity_analysis_results_manager,
    )
    manager: SensitivityAnalysisResultsManager = SensitivityAnalysisResultsManager(
        param_variations, Levels.VIRTUAL
    )

    results_holder = {}

    def mock_to_csv(self, path, **kwargs):
        results_holder[path] = self

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    manager.save_sensitivity_variations_mapping(num_variations)

    if sys.platform.startswith("win"):
        assert results_holder[
            "test\\" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(get_expected_vw_Sens_mappings_1())
    else:
        assert results_holder[
            "test/" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(get_expected_vw_Sens_mappings_1())


def test_save_sensitivity_variations_mapping_vw_2(monkeypatch):
    param_variations, num_variations = get_vw_params_mapping2()
    monkeypatch.setattr(
        SensitivityAnalysisResultsManager,
        "__init__",
        mock_init_sensitivity_analysis_results_manager,
    )
    manager: SensitivityAnalysisResultsManager = SensitivityAnalysisResultsManager(
        param_variations, Levels.VIRTUAL
    )

    results_holder = {}

    def mock_to_csv(self, path, **kwargs):
        results_holder[path] = self

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    manager.save_sensitivity_variations_mapping(num_variations)

    if sys.platform.startswith("win"):
        assert results_holder[
            "test\\" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(get_expected_vw_Sens_mappings_2())
    else:
        assert results_holder[
            "test/" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(get_expected_vw_Sens_mappings_2())


def test_save_sensitivity_variations_mapping_vw_3(monkeypatch):
    param_variations, num_variations = get_vw_params_mapping3()
    monkeypatch.setattr(
        SensitivityAnalysisResultsManager,
        "__init__",
        mock_init_sensitivity_analysis_results_manager,
    )
    manager: SensitivityAnalysisResultsManager = SensitivityAnalysisResultsManager(
        param_variations, Levels.VIRTUAL
    )

    results_holder = {}

    def mock_to_csv(self, path, **kwargs):
        results_holder[path] = self

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    manager.save_sensitivity_variations_mapping(num_variations)

    if sys.platform.startswith("win"):
        assert results_holder[
            "test\\" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(get_expected_vw_Sens_mappings_3())
    else:
        assert results_holder[
            "test/" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(get_expected_vw_Sens_mappings_3())


def test_save_sensitivity_variations_mapping_program_1(monkeypatch):
    param_variations, num_variations = get_program_params_mapping_1()
    monkeypatch.setattr(
        SensitivityAnalysisResultsManager,
        "__init__",
        mock_init_sensitivity_analysis_results_manager,
    )
    manager: SensitivityAnalysisResultsManager = SensitivityAnalysisResultsManager(
        param_variations, Levels.PROGRAM
    )

    results_holder = {}

    def mock_to_csv(self, path, **kwargs):
        results_holder[path] = self

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    manager.save_sensitivity_variations_mapping(num_variations)

    expected_df: pd.DataFrame = get_expected_program_Sens_mappings_1()

    if sys.platform.startswith("win"):
        assert results_holder[
            "test\\" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)
    else:
        assert results_holder[
            "test/" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)


def test_save_sensitivity_variations_mapping_program_2(monkeypatch):
    param_variations, num_variations = get_program_params_mapping_2()
    monkeypatch.setattr(
        SensitivityAnalysisResultsManager,
        "__init__",
        mock_init_sensitivity_analysis_results_manager,
    )
    manager: SensitivityAnalysisResultsManager = SensitivityAnalysisResultsManager(
        param_variations, Levels.PROGRAM
    )

    results_holder = {}

    def mock_to_csv(self, path, **kwargs):
        results_holder[path] = self

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    manager.save_sensitivity_variations_mapping(num_variations)

    expected_df: pd.DataFrame = get_expected_program_Sens_mappings_2()

    if sys.platform.startswith("win"):
        assert results_holder[
            "test\\" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)
    else:
        assert results_holder[
            "test/" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)


def test_save_sensitivity_variations_mapping_method_1(monkeypatch):
    param_variations, num_variations = get_method_params_mapping_1()
    monkeypatch.setattr(
        SensitivityAnalysisResultsManager,
        "__init__",
        mock_init_sensitivity_analysis_results_manager,
    )
    manager: SensitivityAnalysisResultsManager = SensitivityAnalysisResultsManager(
        param_variations, Levels.METHOD
    )

    results_holder = {}

    def mock_to_csv(self, path, **kwargs):
        results_holder[path] = self

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    manager.save_sensitivity_variations_mapping(num_variations)

    expected_df: pd.DataFrame = get_expected_method_Sens_mappings_1()

    if sys.platform.startswith("win"):
        assert results_holder[
            "test\\" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)
    else:
        assert results_holder[
            "test/" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)


def test_save_sensitivity_variations_mapping_method_2(monkeypatch):
    param_variations, num_variations = get_method_params_mapping_2()
    monkeypatch.setattr(
        SensitivityAnalysisResultsManager,
        "__init__",
        mock_init_sensitivity_analysis_results_manager,
    )
    manager: SensitivityAnalysisResultsManager = SensitivityAnalysisResultsManager(
        param_variations, Levels.METHOD
    )

    results_holder = {}

    def mock_to_csv(self, path, **kwargs):
        results_holder[path] = self

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    manager.save_sensitivity_variations_mapping(num_variations)

    expected_df: pd.DataFrame = get_expected_method_Sens_mappings_2()

    if sys.platform.startswith("win"):
        assert results_holder[
            "test\\" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)
    else:
        assert results_holder[
            "test/" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)


def test_save_sensitivity_variations_mapping_method_3(monkeypatch):
    param_variations, num_variations = get_method_params_mapping_3()
    monkeypatch.setattr(
        SensitivityAnalysisResultsManager,
        "__init__",
        mock_init_sensitivity_analysis_results_manager,
    )
    manager: SensitivityAnalysisResultsManager = SensitivityAnalysisResultsManager(
        param_variations, Levels.METHOD
    )

    results_holder = {}

    def mock_to_csv(self, path, **kwargs):
        results_holder[path] = self

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    manager.save_sensitivity_variations_mapping(num_variations)

    expected_df: pd.DataFrame = get_expected_method_Sens_mappings_3()

    if sys.platform.startswith("win"):
        assert results_holder[
            "test\\" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)
    else:
        assert results_holder[
            "test/" + SensitivityAnalysisOutputs.SENSITIVITY_VARIATIONS_MAPPING + ".csv"
        ].equals(expected_df)
