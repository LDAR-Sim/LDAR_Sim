"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_filter_df_by_relevant_method.py
Purpose: Contains unit tests related to filtering the true/false deployment data
frame for the relevant program, based on the provided method.

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
from src.ldar_sim_run import filter_deployment_tf_by_program_methods
from src.constants.infrastructure_const import Deployment_TF_Sites_Constants as DTSC


def simple_fixture():
    data_ori = {
        DTSC.SITE_ID: [1, 2, 3, 4, 5],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="A"): [False, True, False, True, False],
        DTSC.REQUIRED_SURVEY.format(method="B"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="B"): [False, True, False, True, False],
        DTSC.REQUIRED_SURVEY.format(method="C"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="C"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="C"): [False, True, False, True, False],
        DTSC.REQUIRED_SURVEY.format(method="D"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="D"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="D"): [False, True, False, True, False],
    }
    prog_method = ["A", "B"]
    data_filtered_result = {
        DTSC.SITE_ID: [1, 2, 3, 4, 5],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.MEASURED: [False, True, False, True, False],
    }
    return (pd.DataFrame(data_ori), prog_method, pd.DataFrame(data_filtered_result))


def complex_fixture():
    data_ori = {
        DTSC.SITE_ID: [1, 2, 3, 4, 5],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="A"): [False, True, False, True, False],
        DTSC.REQUIRED_SURVEY.format(method="B"): [True, False, True, False, True],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [True, False, True, False, True],
        DTSC.METHOD_MEASURED.format(method="B"): [True, False, True, False, True],
        DTSC.REQUIRED_SURVEY.format(method="C"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="C"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="C"): [False, True, False, True, False],
        DTSC.REQUIRED_SURVEY.format(method="D"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="D"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="D"): [False, True, False, True, False],
    }
    prog_method = ["A", "B"]
    data_filtered_result = {
        DTSC.SITE_ID: [1, 2, 3, 4, 5],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.MEASURED: [True, True, True, True, True],
    }
    return (pd.DataFrame(data_ori), prog_method, pd.DataFrame(data_filtered_result))


def three_method_fixture():
    data_ori = {
        DTSC.SITE_ID: [1, 2, 3, 4, 5],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.REQUIRED_SURVEY.format(method="A"): [True, True, True, False, True],
        DTSC.SITE_DEPLOYMENT.format(method="A"): [True, True, False, False, False],
        DTSC.METHOD_MEASURED.format(method="A"): [True, True, False, False, False],
        DTSC.REQUIRED_SURVEY.format(method="B"): [False, False, True, False, True],
        DTSC.SITE_DEPLOYMENT.format(method="B"): [False, False, True, False, True],
        DTSC.METHOD_MEASURED.format(method="B"): [False, False, True, False, True],
        DTSC.REQUIRED_SURVEY.format(method="C"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="C"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="C"): [False, True, False, True, False],
        DTSC.REQUIRED_SURVEY.format(method="D"): [True, True, True, True, True],
        DTSC.SITE_DEPLOYMENT.format(method="D"): [False, True, False, True, False],
        DTSC.METHOD_MEASURED.format(method="D"): [False, True, False, True, False],
    }
    prog_method = ["A", "B", "C"]
    data_filtered_result = {
        DTSC.SITE_ID: [1, 2, 3, 4, 5],
        DTSC.SITE_TYPE: ["A", "A", "A", "A", "A"],
        DTSC.MEASURED: [True, True, True, True, True],
    }
    return (pd.DataFrame(data_ori), prog_method, pd.DataFrame(data_filtered_result))


@pytest.mark.parametrize("fixture", [simple_fixture(), complex_fixture(), three_method_fixture()])
def test_filter_df_by_relevant_method(fixture):
    truefalse_df, prog_method, expected = fixture

    result = filter_deployment_tf_by_program_methods(truefalse_df, prog_method)

    assert list(result.columns) == list(expected.columns)
    assert len(result) == len(expected)
    assert result.equals(expected)
