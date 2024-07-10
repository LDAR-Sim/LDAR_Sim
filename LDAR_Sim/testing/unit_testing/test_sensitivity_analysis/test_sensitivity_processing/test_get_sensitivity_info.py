# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        test_get_sensitivity_info.py
# Purpose:     To test the get_sensitivity_info function in the sensitivity_processing module.
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

from pathlib import Path
from sensitivity_analysis import sensitivity_processing
from constants.sensitivity_analysis_constants import (
    SensitivityAnalysisMapping,
    SensitivityAnalysisOutputs,
)


def mock_process_parameter_variations(
    param_variations: dict, param_level: str, num_variations: int
):
    return param_variations


def mock_read_in_sens_parameters(root_dir: Path, sens_info_file_path: str, parameter_files: list):
    return mock_sensitivity_info()


def mock_sensitivity_info():
    return {
        SensitivityAnalysisMapping.SENS_PARAM_LEVEL: "test",
        SensitivityAnalysisMapping.SENS_SET_COUNT: 1,
        SensitivityAnalysisMapping.SENS_SETS: "test",
        SensitivityAnalysisMapping.SENS_SUMMARY_INFO: {
            SensitivityAnalysisOutputs.SensitivityTrueVsEstimatedCIs: "test"
        },
    }


def get_expected_sensitivity_info():
    return {
        SensitivityAnalysisMapping.SENS_PARAM_MAPPING[
            SensitivityAnalysisMapping.SENS_PARAM_LEVEL
        ]: "test",
        SensitivityAnalysisMapping.SENS_PARAM_MAPPING[SensitivityAnalysisMapping.SENS_SET_COUNT]: 1,
        SensitivityAnalysisMapping.SENS_PARAM_MAPPING[SensitivityAnalysisMapping.SENS_SETS]: "test",
        SensitivityAnalysisMapping.SENS_PARAM_MAPPING[
            SensitivityAnalysisMapping.SENS_SUMMARY_INFO
        ]: {SensitivityAnalysisOutputs.SensitivityTrueVsEstimatedCIs: "test"},
    }


def test_get_sensitivity_info(monkeypatch):
    monkeypatch.setattr(
        sensitivity_processing, "process_parameter_variations", mock_process_parameter_variations
    )

    monkeypatch.setattr(
        sensitivity_processing, "read_in_sensitivity_parameters", mock_read_in_sens_parameters
    )
    sensitivity_info: dict = sensitivity_processing.get_sensitivity_info(
        "LDAR-Sim test folder", "test", "test_parameter_file"
    )
    assert sensitivity_info == get_expected_sensitivity_info()
