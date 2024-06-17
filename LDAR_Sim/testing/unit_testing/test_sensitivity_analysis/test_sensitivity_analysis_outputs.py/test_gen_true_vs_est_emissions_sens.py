import pandas as pd
from sensitivity_analysis.sensitivity_analysis_outputs import gen_true_vs_est_emissions_sens
from constants.sensitivity_analysis_constants import (
    SensitivityAnalysisOutputs,
    output_file_constants,
)


class MockDirEntry:
    def __init__(self, path):
        self.path = path


def get_expected_output():
    return pd.DataFrame(
        {
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.SENSITIVITY_SET: [
                0,
                0,
                1,
                1,
                2,
                2,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.SIMULATION: [0, 1, 0, 1, 0, 1],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.YEAR: [
                "2020",
                "2020",
                "2020",
                "2020",
                "2020",
                "2020",
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.TRUE_EMISSIONS: [
                10,
                20,
                30,
                40,
                50,
                60,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.ESTIMATED_EMISSIONS: [
                15,
                30,
                45,
                60,
                75,
                90,
            ],
            SensitivityAnalysisOutputs.TrueEstimatedEmisionsSens.PERCENT_DIFFERENCE: [
                40.0,
                40.0,
                40.0,
                40.0,
                40.0,
                40.0,
            ],
        }
    )


def mock_read_csv(path):
    return pd.DataFrame(
        {
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME: [
                "test_program_0",
                "test_program_0",
                "test_program_1",
                "test_program_1",
                "test_program_2",
                "test_program_2",
            ],
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.SIM: [0, 1, 0, 1, 0, 1],
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.T_ANN_EMIS.format(2020): [
                10,
                20,
                30,
                40,
                50,
                60,
            ],
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.EST_ANN_EMIS.format(2020): [
                15,
                30,
                45,
                60,
                75,
                90,
            ],
        }
    )


def test_gen_true_vs_est_emissions_sens_basic_example(monkeypatch):

    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

    data: pd.DataFrame = gen_true_vs_est_emissions_sens(
        dir=MockDirEntry("test_Dir"), program="test_program", index=0, varied_progs=True
    )
    expected_output: pd.DataFrame = get_expected_output()

    assert data.equals(expected_output)
