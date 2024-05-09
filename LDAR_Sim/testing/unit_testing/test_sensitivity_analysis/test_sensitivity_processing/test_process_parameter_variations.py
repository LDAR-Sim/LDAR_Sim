from typing import Any

import pytest

from constants.param_default_const import (
    Levels,
    Virtual_World_Params,
    Program_Params,
    Method_Params,
    Common_Params,
)
from constants.sensitivity_analysis_constants import SensitivityAnalysisMapping
from sensitivity_analysis.sensitivity_processing import process_parameter_variations
from constants.error_messages import SensitivityAnalysisMessages


@pytest.fixture(name="vw_parameter_variations_1")
def vw_parameter_variations_1():
    return {Virtual_World_Params.EMIS: {Virtual_World_Params.LPR: [0.000275, 0.0065, 0.013]}}


@pytest.fixture(name="expected_vw_parameter_variations_1")
def expected_vw_parameter_variations_1():
    return {
        Virtual_World_Params.EMIS: [
            {Virtual_World_Params.LPR: 0.000275},
            {Virtual_World_Params.LPR: 0.0065},
            {Virtual_World_Params.LPR: 0.013},
        ]
    }


@pytest.fixture(name="vw_parameter_variations_2")
def vw_parameter_variations_2():
    return {Virtual_World_Params.EMIS: {Virtual_World_Params.ERS: ["test1", "test2"]}}


@pytest.fixture(name="expected_vw_parameter_variations_2")
def expected_vw_parameter_variations_2():
    return {
        Virtual_World_Params.EMIS: [
            {Virtual_World_Params.ERS: "test1"},
            {Virtual_World_Params.ERS: "test2"},
        ]
    }


@pytest.fixture(name="vw_parameter_variations_3")
def vw_parameter_variations_3():
    return {
        Virtual_World_Params.REPAIR: {
            Virtual_World_Params.REPAIR_COST: [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]]
        }
    }


@pytest.fixture(name="expected_vw_parameter_variations_3")
def expected_vw_parameter_variations_3():
    return {
        Virtual_World_Params.REPAIR: [
            {Virtual_World_Params.REPAIR_COST: [0.1, 0.2]},
            {Virtual_World_Params.REPAIR_COST: [0.3, 0.4]},
            {Virtual_World_Params.REPAIR_COST: [0.5, 0.6]},
        ]
    }


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("vw_parameter_variations_1", "expected_vw_parameter_variations_1"),
        ("vw_parameter_variations_2", "expected_vw_parameter_variations_2"),
        ("vw_parameter_variations_3", "expected_vw_parameter_variations_3"),
    ],
)
def test_process_parameter_variations_vw_level(test_input, expected, request):
    parameter_variations: dict = request.getfixturevalue(test_input)
    expected_parameter_variations: dict = request.getfixturevalue(expected)
    unpacked_variations: dict[str, Any] = process_parameter_variations(
        parameter_variations, Levels.VIRTUAL
    )
    assert unpacked_variations == expected_parameter_variations


@pytest.fixture(name="program_parameter_variations_1")
def program_parameter_variations_1():
    return [
        {
            SensitivityAnalysisMapping.PROGRAM_NAME: "test",
            SensitivityAnalysisMapping.PROGRAM_SENS_PARAMS: {
                Program_Params.DURATION_ESTIMATE: {Program_Params.DURATION_FACTOR: [0.1, 0.5, 1.0]}
            },
        }
    ]


@pytest.fixture(name="expected_program_parameter_variations_1")
def expected_program_parameter_variations_1():
    return {
        "test": {
            Program_Params.DURATION_ESTIMATE: [
                {Program_Params.DURATION_FACTOR: 0.1},
                {Program_Params.DURATION_FACTOR: 0.5},
                {Program_Params.DURATION_FACTOR: 1.0},
            ]
        }
    }


@pytest.fixture(name="program_parameter_variations_2")
def program_parameter_variations_2():
    return [
        {
            SensitivityAnalysisMapping.PROGRAM_NAME: "test",
            SensitivityAnalysisMapping.PROGRAM_SENS_PARAMS: {
                Program_Params.ECONOMICS: {Program_Params.VERIFICATION: [100, 200]}
            },
        }
    ]


@pytest.fixture(name="expected_program_parameter_variations_2")
def expected_program_parameter_variations_2():
    return {
        "test": {
            Program_Params.ECONOMICS: [
                {Program_Params.VERIFICATION: 100},
                {Program_Params.VERIFICATION: 200},
            ]
        },
    }


@pytest.fixture(name="program_parameter_variations_3")
def program_parameter_variations_3():
    return [
        {
            SensitivityAnalysisMapping.PROGRAM_NAME: "test1",
            SensitivityAnalysisMapping.PROGRAM_SENS_PARAMS: {
                Program_Params.DURATION_ESTIMATE: {Program_Params.DURATION_FACTOR: [0.1, 0.5, 1.0]}
            },
        },
        {
            SensitivityAnalysisMapping.PROGRAM_NAME: "test2",
            SensitivityAnalysisMapping.PROGRAM_SENS_PARAMS: {
                Program_Params.DURATION_ESTIMATE: {Program_Params.DURATION_FACTOR: [0.1, 0.2, 0.3]}
            },
        },
    ]


@pytest.fixture(name="expected_program_parameter_variations_3")
def expected_program_parameter_variations_3():
    return {
        "test1": {
            Program_Params.DURATION_ESTIMATE: [
                {Program_Params.DURATION_FACTOR: 0.1},
                {Program_Params.DURATION_FACTOR: 0.5},
                {Program_Params.DURATION_FACTOR: 1.0},
            ]
        },
        "test2": {
            Program_Params.DURATION_ESTIMATE: [
                {Program_Params.DURATION_FACTOR: 0.1},
                {Program_Params.DURATION_FACTOR: 0.2},
                {Program_Params.DURATION_FACTOR: 0.3},
            ]
        },
    }


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("program_parameter_variations_1", "expected_program_parameter_variations_1"),
        ("program_parameter_variations_2", "expected_program_parameter_variations_2"),
    ],
)
def test_process_parameter_variations_program_level(test_input, expected, request):
    parameter_variations: dict = request.getfixturevalue(test_input)
    expected_parameter_variations: dict = request.getfixturevalue(expected)
    unpacked_variations: dict[str, Any] = process_parameter_variations(
        parameter_variations, Levels.PROGRAM
    )
    assert unpacked_variations == expected_parameter_variations


@pytest.fixture(name="method_parameter_variations_1")
def method_parameter_variations_1():
    return [
        {
            SensitivityAnalysisMapping.METHOD_NAME: "test1",
            SensitivityAnalysisMapping.Method_SENS_PARAMS: {Method_Params.RS: [1, 2, 3, 4, 5]},
        }
    ]


@pytest.fixture(name="expected_method_parameter_variations_1")
def expected_method_parameter_variations_1():
    return {"test1": {Method_Params.RS: [1, 2, 3, 4, 5]}}


@pytest.fixture(name="method_parameter_variations_2")
def method_parameter_variations_2():
    return [
        {
            SensitivityAnalysisMapping.METHOD_NAME: "test2",
            SensitivityAnalysisMapping.Method_SENS_PARAMS: {
                Method_Params.T_BW_SITES: {Common_Params.VAL: [[8, 10, 12], [20, 30, 40]]}
            },
        }
    ]


@pytest.fixture(name="expected_method_parameter_variations_2")
def expected_method_parameter_variations_2():
    return {
        "test2": {
            Method_Params.T_BW_SITES: [
                {Common_Params.VAL: [8, 10, 12]},
                {Common_Params.VAL: [20, 30, 40]},
            ]
        }
    }


@pytest.fixture(name="method_parameter_variations_3")
def method_parameter_variations_3():
    return [
        {
            SensitivityAnalysisMapping.METHOD_NAME: "test1",
            SensitivityAnalysisMapping.Method_SENS_PARAMS: {Method_Params.RS: [1, 2, 3, 4, 5]},
        },
        {
            SensitivityAnalysisMapping.METHOD_NAME: "test2",
            SensitivityAnalysisMapping.Method_SENS_PARAMS: {Method_Params.RS: [10, 20, 30, 40, 50]},
        },
    ]


@pytest.fixture(name="expected_method_parameter_variations_3")
def expected_method_parameter_variations_3():
    return {
        "test1": {Method_Params.RS: [1, 2, 3, 4, 5]},
        "test2": {Method_Params.RS: [10, 20, 30, 40, 50]},
    }


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("method_parameter_variations_1", "expected_method_parameter_variations_1"),
        ("method_parameter_variations_2", "expected_method_parameter_variations_2"),
        ("method_parameter_variations_3", "expected_method_parameter_variations_3"),
    ],
)
def test_process_parameter_variations_method_level(test_input, expected, request):
    parameter_variations: dict = request.getfixturevalue(test_input)
    expected_parameter_variations: dict = request.getfixturevalue(expected)
    unpacked_variations: dict[str, Any] = process_parameter_variations(
        parameter_variations, Levels.METHOD
    )
    assert unpacked_variations == expected_parameter_variations


@pytest.fixture(name="invalid_method_parameter_variations_1")
def invalid_method_parameter_variations_1():
    return {Method_Params.RS: [1, 2, 3, 4, 5]}


@pytest.fixture(name="invalid_method_parameter_variations_2")
def invalid_method_parameter_variations_2():
    return "test1"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("invalid_method_parameter_variations_1", None),
        ("invalid_method_parameter_variations_2", None),
    ],
)
def test_invalid_method_parameter_variations(test_input, expected, request, capfd):
    parameter_variations: dict = request.getfixturevalue(test_input)
    with pytest.raises(SystemExit):
        _ = process_parameter_variations(parameter_variations, Levels.METHOD)
    out, err = capfd.readouterr()
    assert SensitivityAnalysisMessages.INVALID_SENSITIVITY_VARIATIONS_ERROR in out


@pytest.fixture(name="invalid_program_parameter_variations_1")
def invalid_program_parameter_variations_1():
    return {Program_Params.DURATION_ESTIMATE: {Program_Params.DURATION_FACTOR: [0.1, 0.5, 1.0]}}


@pytest.fixture(name="invalid_program_parameter_variations_2")
def invalid_program_parameter_variations_2():
    return "test1"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("invalid_program_parameter_variations_1", None),
        ("invalid_program_parameter_variations_2", None),
    ],
)
def test_invalid_program_parameter_variations(test_input, expected, request, capfd):
    parameter_variations: dict = request.getfixturevalue(test_input)
    with pytest.raises(SystemExit):
        _ = process_parameter_variations(parameter_variations, Levels.PROGRAM)
    out, err = capfd.readouterr()
    assert SensitivityAnalysisMessages.INVALID_SENSITIVITY_VARIATIONS_ERROR in out
