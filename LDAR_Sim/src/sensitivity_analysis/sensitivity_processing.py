# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        sensitivity_processing.py
# Purpose:     Logic to process sensitivity analysis parameters from the
#              sensitivity info file into a useful format
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

import logging
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

    try:
        with open(real_sensitive_info_filepath, "r") as file:
            sens_parameters: dict = yaml.load(file.read(), Loader=yaml.FullLoader)
    except FileNotFoundError:
        logger: logging.Logger = logging.getLogger(__name__)
        logger.error(
            sensitivity_analysis_constants.SensitivityParameterParsingConstants.MISSING_SENS_FILE
        )
        sys.exit()
    except Exception as e:
        logger: logging.Logger = logging.getLogger(__name__)
        logger.error(
            (
                sensitivity_analysis_constants.SensitivityParameterParsingConstants
            ).FILE_READ_ERROR.format(real_sensitive_info_filepath),
            str(e),
        )
        sys.exit()

    return sens_parameters


def process_parameter_variations(
    parameter_variations: dict[str, Any] | list[dict[str, Any]],
    parameter_level: str,
    num_variations: int,
) -> dict[str, Any]:
    if parameter_level == param_default_const.Levels.METHOD:
        if isinstance(parameter_variations, list):
            return {
                method[
                    sensitivity_analysis_constants.SensitivityAnalysisMapping.METHOD_NAME
                ]: unpack_parameter_variations(
                    method[
                        sensitivity_analysis_constants.SensitivityAnalysisMapping.Method_SENS_PARAMS
                    ],
                    num_variations,
                )
                for method in parameter_variations
            }
        else:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(
                error_messages.SensitivityAnalysisMessages.INVALID_SENSITIVITY_VARIATIONS_ERROR
            )
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
                    ],
                    num_variations,
                )
                for program in parameter_variations
            }
        else:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(
                error_messages.SensitivityAnalysisMessages.INVALID_SENSITIVITY_VARIATIONS_ERROR
            )
            sys.exit()
    elif parameter_level == param_default_const.Levels.VIRTUAL:
        return unpack_parameter_variations(parameter_variations, num_variations)
    else:
        logger: logging.Logger = logging.getLogger(__name__)
        logger.error(error_messages.SensitivityAnalysisMessages.INVALID_PARAMETER_LEVEL_ERROR)
        sys.exit()


def unpack_parameter_variations(
    parameter_variations: dict[str, Any], num_variations: int
) -> dict[str, Any]:
    """
    Unpack the parameter variations to get the actual values

    Returns
    -------
    dict[str, Any]
        The unpacked parameter variations
    """
    unpacked_variations: dict[str, list[dict]] = {}
    for key, value in parameter_variations.items():
        unpacked_variations[key] = []
        if isinstance(value, dict):
            for variation in range(num_variations):
                unpacked_variations[key].extend(
                    unpack_nested_parameter_variations(value, variation)
                )
        elif isinstance(value, list):
            unpacked_variations[key] = value
    return unpacked_variations


def unpack_nested_parameter_variations(
    parameter_variations: dict[str, Any], variation_index: int
) -> dict[str, Any]:
    unpacked_variations: list = []
    for key, value in parameter_variations.items():
        if isinstance(value, dict):
            unpacked_sub_variations: list = unpack_nested_parameter_variations(
                value, variation_index
            )
            unpacked_variations.extend(
                [{key: sub_variation} for sub_variation in unpacked_sub_variations]
            )
        elif isinstance(value, list):
            unpacked_variations.append({key: value[variation_index]})
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
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(
                error_messages.SensitivityAnalysisMessages.MISSING_SENSITIVITY_INFO.format(key)
            )
            sys.exit()

    sens_info_dict[sensitivity_analysis_constants.SensitivityAnalysisMapping.PARAM_VARIATIONS] = (
        process_parameter_variations(
            sens_info_dict[
                sensitivity_analysis_constants.SensitivityAnalysisMapping.PARAM_VARIATIONS
            ],
            sens_info_dict[sensitivity_analysis_constants.SensitivityAnalysisMapping.PARAM_LEVEL],
            sens_info_dict[sensitivity_analysis_constants.SensitivityAnalysisMapping.NUM_SENS_SETS],
        )
    )
    return sens_info_dict
