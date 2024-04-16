import pandas as pd
from contextlib import contextmanager
from pathlib import Path

import os
from constants import param_default_const
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper
from file_processing.output_processing.summary_outputs import (
    generate_emissions_summary,
    generate_timeseries_summary,
)
from src.constants.output_file_constants import (
    EMIS_DATA_COL_ACCESSORS as eca,
    EMIS_SUMMARY_COLUMNS_ACCESSORS as esca,
    TIMESERIES_COL_ACCESSORS as tca,
    TS_SUMMARY_COLUMNS_ACCESSORS as tsca,
)


def get_mock_summary_output_mapper():
    SummaryOutputsMapper: SummaryOutputMapper = SummaryOutputMapper(
        {
            param_default_const.Output_Params.TIMESERIES_SUMMARY: {
                param_default_const.Output_Params.AVERAGE_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.AVERAGE_MITIGABLE_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.AVERAGE_NON_MITIGABLE_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.PERCENTILE_95_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.PERCENTILE_95_MITIGABLE_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.PERCENTILE_95_NON_MITIGABLE_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.PERCENTILE_5_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.PERCENTILE_5_MITIGABLE_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.PERCENTILE_5_NON_MITIGABLE_DAILY_EMISSIONS: True,
                param_default_const.Output_Params.AVERAGE_DAILY_COST: True,
                param_default_const.Output_Params.PERCENTILE_95_DAILY_COST: True,
                param_default_const.Output_Params.PERCENTILE_5_DAILY_COST: True,
            },
            param_default_const.Output_Params.EMISSIONS_SUMMARY: {
                param_default_const.Output_Params.EMISSIONS_SUMMARY_TOTAL_TRUE: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_TOTAL_ESTIMATED: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_TOTAL_MITIGABLE: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_TOTAL_NON_MITIGABLE: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_AVERAGE_RATE: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_PERCENTILE_95_RATE: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_PERCENTILE_5_RATE: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_AVERAGE_AMOUNT: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_PERCENTILE_95_AMOUNT: True,
                param_default_const.Output_Params.EMISSIONS_SUMMARY_PERCENTILE_5_AMOUNT: True,
            },
        },
        [2024, 2025],
    )
    return SummaryOutputsMapper


class MockDirEntry:
    def __init__(self, name):
        self.name = name
        self.path = name

    def is_dir(self):
        return True

    def is_file(self) -> bool:
        return True


@contextmanager
def mock_scandir_emis_sum(dir: Path):
    yield [
        MockDirEntry(name="test_0_emissions_summary.csv"),
        MockDirEntry(name="test_1_emissions_summary.csv"),
        MockDirEntry(name="test_2_emissions_summary.csv"),
    ]


def mock_read_csv_emis_sum(file_path: str):
    return mock_emis_csv_data[file_path]


mock_emis_csv_data = {
    "test_0_emissions_summary.csv": pd.DataFrame(
        {
            eca.T_VOL_EMIT: [1, 2, 3, 4],
            eca.EST_VOL_EMIT: [0, 1, 2, 3],
            eca.T_RATE: [10, 9, 8, 7],
            eca.M_RATE: [9, 8, 7, 6],
            eca.REPAIRABLE: [True, True, True, False],
            eca.DATE_BEG: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.DATE_REP_EXP: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
    "test_1_emissions_summary.csv": pd.DataFrame(
        {
            eca.T_VOL_EMIT: [5, 6, 7, 8],
            eca.EST_VOL_EMIT: [4, 5, 6, 7],
            eca.T_RATE: [6, 5, 4, 3],
            eca.M_RATE: [5, 4, 3, 2],
            eca.REPAIRABLE: [True, True, True, False],
            eca.DATE_BEG: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.DATE_REP_EXP: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
    "test_2_emissions_summary.csv": pd.DataFrame(
        {
            eca.T_VOL_EMIT: [9, 10, 11, 12],
            eca.EST_VOL_EMIT: [8, 9, 10, 11],
            eca.T_RATE: [3, 2, 1, 0],
            eca.M_RATE: [2, 1, 0, 0],
            eca.REPAIRABLE: [True, True, True, False],
            eca.DATE_BEG: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.DATE_REP_EXP: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
}

expected_emis_summary_csv = pd.DataFrame(
    {
        esca.PROG_NAME: ["test", "test", "test"],
        esca.SIM: ["0", "1", "2"],
        esca.T_TOTAL_EMIS: [10, 26, 42],
        esca.EST_TOTAL_EMIS: [6, 22, 38],
        esca.T_TOTAL_MIT_EMIS: [6, 18, 30],
        esca.T_TOTAL_NON_MIT_EMIS: [4, 8, 12],
        esca.AVG_T_EMIS_RATE: [8.5, 4.5, 1.5],
        esca.T_EMIS_RATE_95: [10.0, 6.0, 3.0],
        esca.T_EMIS_RATE_5: [7.0, 3.0, 0.0],
        esca.T_AVG_EMIS_AMOUNT: [2.5, 6.5, 10.5],
        esca.T_EMIS_AMOUNT_95: [4.0, 8.0, 12.0],
        esca.T_EMIS_AMOUNT_5: [1.0, 5.0, 9.0],
        esca.T_ANN_EMIS.format(2024): [3.0, 11.0, 19.0],
        esca.T_ANN_EMIS.format(2025): [7.0, 15.0, 23.0],
        esca.EST_ANN_EMIS.format(2024): [1.0, 9.0, 17.0],
        esca.EST_ANN_EMIS.format(2025): [5.0, 13.0, 21.0],
    }
)


@contextmanager
def mock_scandir_ts_sum(dir: Path):
    yield [
        MockDirEntry(name="test_0_timeseries.csv"),
        MockDirEntry(name="test_1_timeseries.csv"),
        MockDirEntry(name="test_2_timeseries.csv"),
    ]


def mock_read_csv_ts_sum(file_path: str):
    return mock_ts_csv_data[file_path]


mock_ts_csv_data = {
    "test_0_timeseries.csv": pd.DataFrame(
        {
            tca.EMIS: [1, 2, 3, 4],
            tca.COST: [10, 9, 8, 7],
            tca.EMIS_MIT: [1, 2, 2, 2],
            tca.EMIS_NON_MIT: [0, 0, 1, 2],
        }
    ),
    "test_1_timeseries.csv": pd.DataFrame(
        {
            tca.EMIS: [5, 6, 7, 8],
            tca.COST: [6, 5, 4, 3],
            tca.EMIS_MIT: [5, 6, 6, 6],
            tca.EMIS_NON_MIT: [0, 0, 1, 2],
        }
    ),
    "test_2_timeseries.csv": pd.DataFrame(
        {
            tca.EMIS: [9, 10, 11, 12],
            tca.COST: [3, 2, 1, 0],
            tca.EMIS_MIT: [9, 10, 10, 10],
            tca.EMIS_NON_MIT: [0, 0, 1, 2],
        }
    ),
}

expected_ts_summary_csv = pd.DataFrame(
    {
        tsca.PROG_NAME: ["test", "test", "test"],
        tsca.SIM: ["0", "1", "2"],
        tsca.AVG_T_DAILY_EMIS: [2.5, 6.5, 10.5],
        tsca.AVG_T_MIT_DAILY_EMIS: [1.75, 5.75, 9.75],
        tsca.AVG_T_NON_MIT_DAILY_EMIS: [0.75, 0.75, 0.75],
        tsca.T_DAILY_EMIS_95: [4.0, 8.0, 12.0],
        tsca.T_MIT_DAILY_EMIS_95: [2.0, 6.0, 10.0],
        tsca.T_NON_MIT_DAILY_EMIS_95: [2.0, 2.0, 2.0],
        tsca.T_DAILY_EMIS_5: [1.0, 5.0, 9.0],
        tsca.T_MIT_DAILT_EMIS_5: [1.0, 5.0, 9.0],
        tsca.T_NON_MIT_DAILY_EMIS_5: [0.0, 0.0, 0.0],
        tsca.AVG_DAILY_COST: [8.5, 4.5, 1.5],
        tsca.DAILY_COST_95: [10.0, 6.0, 3.0],
        tsca.DAILY_COST_5: [7.0, 3.0, 0.0],
    }
)


def test_000_correct_emissions_summary_generated_from_3_es(monkeypatch):
    monkeypatch.setattr(os, "scandir", mock_scandir_emis_sum)
    monkeypatch.setattr(pd, "read_csv", mock_read_csv_emis_sum)

    test_es_summary: pd.DataFrame = generate_emissions_summary(
        "test", get_mock_summary_output_mapper()
    )
    assert isinstance(test_es_summary, pd.DataFrame)
    assert test_es_summary.equals(expected_emis_summary_csv)


def test_000_correct_timeseries_summary_generated_from_3_ts(monkeypatch):
    monkeypatch.setattr(os, "scandir", mock_scandir_ts_sum)
    monkeypatch.setattr(pd, "read_csv", mock_read_csv_ts_sum)
    test_ts_summary: pd.DataFrame = generate_timeseries_summary(
        "test", get_mock_summary_output_mapper()
    )
    assert isinstance(test_ts_summary, pd.DataFrame)
    assert test_ts_summary.equals(expected_ts_summary_csv)
