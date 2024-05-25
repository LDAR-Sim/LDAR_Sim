from typing import Any
import pytest
from constants.param_default_const import Virtual_World_Params, Program_Params, Method_Params
from sensitivity_analysis.sensitivity_processing import unpack_parameter_variations


@pytest.fixture(name="vw_parameter_variations_1")
def vw_parameter_variations_1():
    return {
        Virtual_World_Params.EMIS: {
            Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: [0.000275, 0.0065, 0.013]}
        }
    }, 3


@pytest.fixture(name="expected_vw_parameter_variations_1")
def expected_vw_parameter_variations_1():
    return {
        Virtual_World_Params.EMIS: [
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.000275}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.0065}},
            {Virtual_World_Params.REPAIRABLE: {Virtual_World_Params.PR: 0.013}},
        ]
    }


@pytest.fixture(name="program_parameter_variations_1")
def program_parameter_variations_1():
    return {Program_Params.DURATION_ESTIMATE: {Program_Params.DURATION_FACTOR: [0.1, 0.5, 1.0]}}, 3


@pytest.fixture(name="expected_program_parameter_variations_1")
def expected_program_parameter_variations_1():
    return {
        Program_Params.DURATION_ESTIMATE: [
            {Program_Params.DURATION_FACTOR: 0.1},
            {Program_Params.DURATION_FACTOR: 0.5},
            {Program_Params.DURATION_FACTOR: 1.0},
        ]
    }


@pytest.fixture(name="method_parameter_variations_1")
def method_parameter_variations_1():
    return {Method_Params.RS: [1, 2, 3, 4, 5]}, 5


@pytest.fixture(name="expected_method_parameter_variations_1")
def expected_method_parameter_variations_1():
    return {Method_Params.RS: [1, 2, 3, 4, 5]}


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("vw_parameter_variations_1", "expected_vw_parameter_variations_1"),
        ("program_parameter_variations_1", "expected_program_parameter_variations_1"),
        ("method_parameter_variations_1", "expected_method_parameter_variations_1"),
    ],
)
def test_unpack_parameter_variations_return_expected_unpacking_level(test_input, expected, request):
    parameter_variations, variation_count = request.getfixturevalue(test_input)
    expected_parameter_variations: dict = request.getfixturevalue(expected)
    unpacked_variations: dict[str, Any] = unpack_parameter_variations(
        parameter_variations, variation_count
    )
    assert unpacked_variations == expected_parameter_variations
