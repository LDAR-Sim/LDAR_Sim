from pathlib import Path
import sys
from typing import Any
import os

import yaml

from constants import sensitivity_analysis_constants, param_default_const, error_messages


def read_in_sensitivity_parameters(
    sens_info_file_path: str, root_dir: Path, parameter_files: list[Path]
):
    if os.path.isabs(sens_info_file_path):
        real_sensitive_info_filepath: Path = Path(sens_info_file_path)
    else:
        real_sensitive_info_filepath: Path = root_dir / sens_info_file_path
    for index, parameter_file in enumerate(parameter_files):
        if parameter_file == real_sensitive_info_filepath:
            del parameter_files[index]

    with open(real_sensitive_info_filepath, "r") as file:
        sens_parameters: dict = yaml.load(file.read(), Loader=yaml.FullLoader)
    return sens_parameters


def process_parameter_variations(
    parameter_variations: dict[str, Any] | list[dict[str, Any]], parameter_level: str
) -> dict[str, Any]:
    if parameter_level == param_default_const.Levels.METHOD:
        if isinstance(parameter_variations, list):
            return {
                method[
                    sensitivity_analysis_constants.SensitivityAnalysisMapping.METHOD_NAME
                ]: unpack_parameter_variations(
                    method[
                        sensitivity_analysis_constants.SensitivityAnalysisMapping.Method_SENS_PARAMS
                    ]
                )
                for method in parameter_variations
            }
        else:
            print(error_messages.SensitivityAnalysisMessages.INVALID_SENSITIVITY_VARIATIONS_ERROR)
            sys.exit()
    elif parameter_level == param_default_const.Levels.PROGRAM:
        if isinstance(parameter_variations, list):
            return {
                program[
                    sensitivity_analysis_constants.SensitivityAnalysisMapping.PROGRAM_NAME
                ]: unpack_parameter_variations(
                    program[
                        (
                            sensitivity_analysis_constants.SensitivityAnalysisMapping
                        ).PROGRAM_SENS_PARAMS
                    ]
                )
                for program in parameter_variations
            }
        else:
            print(error_messages.SensitivityAnalysisMessages.INVALID_SENSITIVITY_VARIATIONS_ERROR)
            sys.exit()
    else:
        return unpack_parameter_variations(parameter_variations)


def unpack_parameter_variations(parameter_variations: dict[str, Any]) -> dict[str, Any]:
    """
    Unpack the parameter variations to get the actual values

    Returns
    -------
    dict[str, Any]
        The unpacked parameter variations
    """
    unpacked_variations: dict[str, Any] = {}
    for key, value in parameter_variations.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                if isinstance(inner_value, list):
                    unpacked_variations[key] = [{inner_key: v} for v in inner_value]
                else:
                    unpacked_variations[key] = unpack_parameter_variations(value)
        else:
            unpacked_variations[key] = value
    return unpacked_variations


def get_sensitivity_info(
    root_dir: Path,
    sens_info_file_path: str,
    parameter_files: list,
) -> dict[str, Any]:
    """
    Get the sensitivity information for the simulation

    Returns
    -------
    dict[str, Any]
        The sensitivity information for the simulation
    """
    sens_parameters: dict = read_in_sensitivity_parameters(
        sens_info_file_path, root_dir, parameter_files
    )

    sens_info_dict: dict[str, Any] = {}

    for key in sensitivity_analysis_constants.SensitivityAnalysisMapping.SENS_PARAM_MAPPING:
        if key in sens_parameters:
            sens_info_dict[
                sensitivity_analysis_constants.SensitivityAnalysisMapping.SENS_PARAM_MAPPING[key]
            ] = sens_parameters.pop(key)
        else:
            sens_info_dict[
                sensitivity_analysis_constants.SensitivityAnalysisMapping.SENS_PARAM_MAPPING[key]
            ] = None

    sens_info_dict[sensitivity_analysis_constants.SensitivityAnalysisMapping.PARAM_VARIATIONS] = (
        process_parameter_variations(
            sens_info_dict[
                sensitivity_analysis_constants.SensitivityAnalysisMapping.PARAM_VARIATIONS
            ],
            sens_info_dict[sensitivity_analysis_constants.SensitivityAnalysisMapping.PARAM_LEVEL],
        )
    )
    return sens_info_dict
