import nt
import os
import re
from typing import Any

import pandas as pd
from constants import sensitivity_analysis_constants, file_name_constants, output_file_constants
from file_processing.output_processing import output_utils


def gen_true_vs_est_emissions_sens(
    dir: nt.DirEntry, program: str, index: int, varied_progs: bool = False
) -> pd.DataFrame:
    result: pd.DataFrame = pd.DataFrame(
        columns=(
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).TrueEstimatedEmisionsSens.COLUMNS
    )
    emis_data: pd.DataFrame = pd.read_csv(
        os.path.join(
            dir.path, file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY + ".csv"
        )
    )

    if varied_progs:
        filtered_emis_data: pd.DataFrame = emis_data.loc[
            emis_data[output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME].str.contains(
                rf"{program}_\d+", regex=True
            )
        ]
    else:
        filtered_emis_data: pd.DataFrame = emis_data.loc[
            emis_data[output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME].str.contains(
                program, regex=True
            )
        ]

    years = sorted(
        list(
            set(
                [
                    re.search(
                        (
                            (
                                sensitivity_analysis_constants
                            ).SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens
                        ).YEAR_EXTRACTION_REGEX,
                        col,
                    ).group(1)
                    for col in filtered_emis_data.columns
                    if re.search(
                        (
                            (
                                sensitivity_analysis_constants
                            ).SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens
                        ).YEARLY_EMIS_MATCH_REGEX,
                        col,
                    )
                ]
            )
        )
    )

    for i, row in filtered_emis_data.iterrows():
        for year in years:
            new_row: dict[str, Any] = {}
            data_map: dict = (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmisionsSens.DATA_SOURCE_MAPPING
            for key, value in data_map.items():
                new_row[key] = row[value]

            if varied_progs:
                new_row[
                    (
                        sensitivity_analysis_constants.SensitivityAnalysisOutputs
                    ).TrueEstimatedEmisionsSens.SENSITIVITY_SET
                ] = int(
                    re.search(
                        rf"{program}_(\d+)",
                        row[output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME],
                    ).group(1)
                )
            else:
                new_row[
                    (
                        sensitivity_analysis_constants.SensitivityAnalysisOutputs
                    ).TrueEstimatedEmisionsSens.SENSITIVITY_SET
                ] = index
            new_row[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.YEAR
            ] = year
            new_row[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.TRUE_EMISSIONS
            ] = row[(output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS).format(year)]
            new_row[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS
            ] = row[
                (output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS).format(year)
            ]
            result.loc[len(result)] = new_row
    # Calculate the percent difference between the true and estimated emissions
    result[
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).TrueEstimatedEmisionsSens.PERCENT_DIFFERENCE
    ] = result.apply(
        lambda row: output_utils.percent_difference(
            row[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.TRUE_EMISSIONS
            ],
            row[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS
            ],
        ),
        axis=1,
    )

    return result
