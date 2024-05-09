from pathlib import Path
import pandas as pd
from constants import sensitivity_analysis_constants
from file_processing.output_processing import summary_output_helpers


def process_confidence_interval(ci: list[float] | float) -> tuple[float, float]:
    if isinstance(ci, float):
        lower_ci = (100 - ci) / 2
        upper_ci = ci + lower_ci
    elif len(ci) == 1:
        lower_ci = (100 - ci[0]) / 2
        upper_ci = ci[0] + lower_ci
    elif len(ci) == 2:
        lower_ci = ci[0]
        upper_ci = ci[1]
    else:
        raise ValueError("Confidence interval must be a list of length 1 or 2")
    return {
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).SensitivityTrueVsEstimatedCIs.LOWER_CI_ACCESSOR: lower_ci,
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).SensitivityTrueVsEstimatedCIs.UPPER_CI_ACCESSOR: upper_ci,
    }


def gen_true_vs_est_sens_cis(output_dir: str, data_source: str, **kwargs) -> pd.DataFrame:
    # Get upper and lower ci percentiles from kwargs if present
    confidence_interval_info: dict = kwargs.get(
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).SensitivityTrueVsEstimatedCIs.CONFIDENCE_INTERVAL,
        {},
    )
    upper_ci = confidence_interval_info.get(
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).SensitivityTrueVsEstimatedCIs.UPPER_CI_ACCESSOR,
        97.5,
    )
    lower_ci = confidence_interval_info.get(
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).SensitivityTrueVsEstimatedCIs.LOWER_CI_ACCESSOR,
        2.5,
    )

    constants: (
        sensitivity_analysis_constants.SensitivityAnalysisOutputs.SensitivityTrueVsEstimatedCIs
    ) = sensitivity_analysis_constants.SensitivityAnalysisOutputs.SensitivityTrueVsEstimatedCIs(
        upper_ci, lower_ci
    )
    sens_data: pd.DataFrame = pd.read_csv(Path(output_dir) / (data_source + ".csv"))
    # Get the unique sensitivity sets
    sensitivity_sets: pd.Series = sens_data[
        (
            sensitivity_analysis_constants.SensitivityAnalysisOutputs
        ).TrueEstimatedEmisionsSens.SENSITIVITY_SET
    ].unique()

    # Initialize the dataframe to store the confidence intervals
    cis_df: pd.DataFrame = pd.DataFrame(columns=[constants.COLUMNS])

    # Iterate over the sensitivity sets and calculate the confidence intervals
    for sensitivity_set in sensitivity_sets:
        # Get the data for the sensitivity set
        sens_set_data: pd.DataFrame = sens_data.loc[
            sens_data[
                (
                    sensitivity_analysis_constants.SensitivityAnalysisOutputs
                ).TrueEstimatedEmisionsSens.SENSITIVITY_SET
            ]
            == sensitivity_set
        ]

        # Calculate the confidence intervals
        lower_ci_val: float = summary_output_helpers.get_nth_percentile(
            sens_set_data,
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmisionsSens.PERCENT_DIFFERENCE,
            lower_ci,
        )
        upper_ci_val: float = summary_output_helpers.get_nth_percentile(
            sens_set_data,
            (
                sensitivity_analysis_constants.SensitivityAnalysisOutputs
            ).TrueEstimatedEmisionsSens.PERCENT_DIFFERENCE,
            upper_ci,
        )

        # Add the confidence intervals to the dataframe
        cis_df.loc[len(cis_df)] = [sensitivity_set, lower_ci_val, upper_ci_val]

    return cis_df
