# ------------------------------------------------------------------------------
# Program:     The LDAR Simulator (LDAR-Sim)
# File:        test_extract_sensitivity_data.py
# Purpose:     Test the extract_sensitivity_data function in sensitivity_visualization_helpers.py
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

import pandas as pd
from sensitivity_analysis.sensitivity_visualization_helpers import extract_sensitivity_data
from constants.sensitivity_analysis_constants import SensitivityAnalysisOutputs


def get_simple_test_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.SENSITIVITY_SET: [
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.YEAR: [
                2020,
                2020,
                2021,
                2021,
                2020,
                2020,
                2021,
                2021,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.SIMULATION: [
                0,
                1,
                0,
                1,
                0,
                1,
                0,
                1,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.TRUE_EMISSIONS: [
                100,
                200,
                300,
                400,
                500,
                600,
                700,
                800,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS: [
                150,
                250,
                350,
                450,
                550,
                650,
                750,
                850,
            ],
        }
    )


def get_expected_simple_sensitivity_data() -> dict[str, dict[str, list[float]]]:
    return {
        0: {
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.TRUE_EMISSIONS: [
                100,
                200,
                300,
                400,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS: [
                150,
                250,
                350,
                450,
            ],
        },
        1: {
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.TRUE_EMISSIONS: [
                500,
                600,
                700,
                800,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS: [
                550,
                650,
                750,
                850,
            ],
        },
    }


def test_extract_sensitivity_data_simple_case():

    test_metrics = [
        SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.TRUE_EMISSIONS,
        SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS,
    ]
    sensitivity_data: dict[str, dict[str, list[float]]] = extract_sensitivity_data(
        get_simple_test_data(), metrics=test_metrics
    )

    assert sensitivity_data == get_expected_simple_sensitivity_data()
