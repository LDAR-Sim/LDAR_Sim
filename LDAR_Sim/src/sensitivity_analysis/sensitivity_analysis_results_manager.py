import os
from typing import Any

import pandas as pd
from constants import sensitivity_analysis_constants, param_default_const
from sensitivity_analysis import (
    sensitivity_analysis_summary_outputs,
    sensitivity_analysis_outputs,
    sensitivity_analysis_visualizations,
)
from file_processing.output_processing import summary_output_helpers


class SensitivityAnalysisResultsManager:
    SENSITIVITY_OUTPUTS_MAP = {
        (sensitivity_analysis_constants.SensitivityAnalysisOutputs).SENSITIVITY_TRUE_VS_ESTIMATED: (
            sensitivity_analysis_outputs.gen_true_vs_est_emissions_sens
        ),
    }
    SENSITIVITY_SUMMARY_OUTPUTS_MAP = {
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).SENSITIVITY_TRUE_VS_ESTIMATED_CIS: (
            sensitivity_analysis_summary_outputs.gen_true_vs_est_sens_cis
        )
    }
    SUMMARY_OUTPUT_DATA_SOURCE_MAPPING = {
        (sensitivity_analysis_constants.SensitivityAnalysisOutputs)
        .SENSITIVITY_TRUE_VS_ESTIMATED_CIS: (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        )
        .SENSITIVITY_TRUE_VS_ESTIMATED
    }
    SENSITIVITY_VISUALIZATIONS_FUNCS = [
        sensitivity_analysis_visualizations.gen_true_vs_est_emissions_percent_difference_sens_viz,
    ]

    SENS_SUMMARY_INFO_PROCESSING_MAP = {
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).SensitivityTrueVsEstimatedCIs.CONFIDENCE_INTERVAL: (
            sensitivity_analysis_summary_outputs.process_confidence_interval
        ),
    }

    def __init__(
        self,
        out_dir: str,
        parameter_variations: dict[str, Any],
        sens_level: str,
        sens_summary_info: dict[str, Any],
    ) -> None:
        self._out_dir: str = out_dir
        self._parameter_variations: dict[str, Any] = parameter_variations
        self._sens_level: str = sens_level
        self._sens_summary_info: dict[str, Any] = self.process_sens_summary_info(sens_summary_info)

    def gen_sensitivity_results(self, program: str, clear_simulation_sets: bool = False) -> None:
        sensitivity_outputs: dict[str, list[pd.DataFrame]] = {}
        with os.scandir(self._out_dir) as entries:
            for index, entry in enumerate(entries):
                if entry.is_dir():
                    for sens_output in self.SENSITIVITY_OUTPUTS_MAP.keys():
                        output_function = self.SENSITIVITY_OUTPUTS_MAP.get(sens_output)
                        output_list = sensitivity_outputs.get(sens_output, [])
                        output_list.append(
                            output_function(
                                entry,
                                program,
                                index,
                                varied_progs=not (
                                    self._sens_level == param_default_const.Levels.VIRTUAL
                                ),
                            )
                        )
                        sensitivity_outputs[sens_output] = output_list
                if clear_simulation_sets:
                    summary_output_helpers.clear_directory(entry)
        combined_outputs: dict[str, pd.DataFrame] = self.combine_outputs(sensitivity_outputs)
        self.save_sensitivity_outputs(combined_outputs)

    def gen_sensitivity_summary_results(self) -> None:
        sensitivity_summary_outputs: dict[str, list[pd.DataFrame]] = {}
        for sens_summary_output in self.SENSITIVITY_SUMMARY_OUTPUTS_MAP.keys():
            output_function = self.SENSITIVITY_SUMMARY_OUTPUTS_MAP.get(sens_summary_output)
            sensitivity_summary_outputs[sens_summary_output] = output_function(
                self._out_dir,
                self.SUMMARY_OUTPUT_DATA_SOURCE_MAPPING[sens_summary_output],
                **self._sens_summary_info,
            )
        self.save_sensitivity_outputs(sensitivity_summary_outputs)

    def gen_sensitivity_visualizations(self, program: str) -> None:
        for sens_viz_func in self.SENSITIVITY_VISUALIZATIONS_FUNCS:
            sens_viz_func(
                self._out_dir,
            )

    def combine_outputs(self, outputs: dict[str, list[pd.DataFrame]]) -> dict[str, pd.DataFrame]:
        combined_outputs: dict[str, pd.DataFrame] = {}
        for key, value in outputs.items():
            combined_outputs[key] = pd.concat(value, ignore_index=True)
        return combined_outputs

    def save_sensitivity_outputs(self, outputs: dict[str, pd.DataFrame]) -> None:
        for key, value in outputs.items():
            value.to_csv(os.path.join(self._out_dir, f"{key}.csv"), index=False)

    def save_sensitivity_variations_mapping(self, parameter_permutation_count: int) -> None:
        # Unpack the dictionary and create a list of rows
        rows = []

        def unpack_full_parameter_path(key: str, value: Any) -> tuple[str, Any]:
            if isinstance(value, dict):
                inner_key, inner_value = list(value.items())[0]
                return unpack_full_parameter_path(".".join([key, inner_key]), inner_value)
            else:
                return key, value

        if self._sens_level == param_default_const.Levels.METHOD:
            for method, variations in self._parameter_variations.items():
                for index in range(parameter_permutation_count):
                    for key, value in variations.items():
                        parameter, true_value = unpack_full_parameter_path(key, value[index])
                        rows.append(
                            [
                                index,
                                ".".join([method, parameter]),
                                true_value,
                            ]
                        )
        else:
            for index in range(parameter_permutation_count):
                for key, value in self._parameter_variations.items():
                    parameter, true_value = unpack_full_parameter_path(key, value[index])
                    rows.append([index, parameter, true_value])

        # Create a DataFrame from the list of rows
        df = pd.DataFrame(
            rows,
            columns=(
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).SensitivityVariationsMapping.COLUMN_NAMES
            ),
        )

        # Write the DataFrame to a CSV file
        df.to_csv(
            os.path.join(
                self._out_dir,
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).SENSITIVITY_VARIATIONS_MAPPING
                + ".csv",
            ),
            index=False,
        )

    def process_sens_summary_info(self, sens_summary_info: dict[str, Any]) -> dict[str, Any]:
        processed_sens_summary_info: dict[str, Any] = {}
        if sens_summary_info not in [None, {}]:
            for key, value in sens_summary_info.items():
                process_func = self.SENS_SUMMARY_INFO_PROCESSING_MAP.get(key)
                if process_func:
                    processed_sens_summary_info[key] = process_func(value)
                else:
                    processed_sens_summary_info[key] = value
        return processed_sens_summary_info
