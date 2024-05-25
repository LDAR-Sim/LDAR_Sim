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


def mock_sensitivity_info():
    return {
        SensitivityAnalysisMapping.SENS_PARAM_LEVEL: "test",
        SensitivityAnalysisMapping.SENS_PERMUTATIONS: 1,
        SensitivityAnalysisMapping.SENS_PARAM_VARIATIONS: "test",
        SensitivityAnalysisMapping.SENS_SUMMARY_INFO: {
            SensitivityAnalysisOutputs.SensitivityTrueVsEstimatedCIs: "test"
        },
    }


def get_expected_sensitivity_info():
    return {
        SensitivityAnalysisMapping.SENS_PARAM_MAPPING[
            SensitivityAnalysisMapping.SENS_PARAM_LEVEL
        ]: "test",
        SensitivityAnalysisMapping.SENS_PARAM_MAPPING[
            SensitivityAnalysisMapping.SENS_PERMUTATIONS
        ]: 1,
        SensitivityAnalysisMapping.SENS_PARAM_MAPPING[
            SensitivityAnalysisMapping.SENS_PARAM_VARIATIONS
        ]: "test",
        SensitivityAnalysisMapping.SENS_PARAM_MAPPING[
            SensitivityAnalysisMapping.SENS_SUMMARY_INFO
        ]: {SensitivityAnalysisOutputs.SensitivityTrueVsEstimatedCIs: "test"},
    }


def test_get_sensitivity_info(monkeypatch):
    monkeypatch.setattr(
        sensitivity_processing, "process_parameter_variations", mock_process_parameter_variations
    )

    def mock_read_in_sens_parameters(
        root_dir: Path, sens_info_file_path: str, parameter_files: list
    ):
        return mock_sensitivity_info()

    monkeypatch.setattr(
        sensitivity_processing, "read_in_sensitivity_parameters", mock_read_in_sens_parameters
    )
    sensitivity_info: dict = sensitivity_processing.get_sensitivity_info(
        "LDAR-Sim test folder", "test", "test_parameter_file"
    )
    assert sensitivity_info == get_expected_sensitivity_info()
