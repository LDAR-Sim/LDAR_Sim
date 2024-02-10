from contextlib import contextmanager
from pathlib import Path

import pandas as pd
from src.file_processing.output_processing.multi_simulation_outputs import (
    gen_ts_summary,
    TS_SUMMARY_COLUMNS_ACCESSORS as tsca,
)
import os
from src.file_processing.output_processing.output_utils import TIMESERIES_COL_ACCESSORS as tca


class MockDirEntry:
    def __init__(self, name):
        self.name = name
        self.path = name

    def is_file(self) -> bool:
        return True


@contextmanager
def mock_scandir(dir: Path):
    yield [
        MockDirEntry(name="test_0_timeseries.csv"),
        MockDirEntry(name="test_1_timeseries.csv"),
        MockDirEntry(name="test_2_timeseries.csv"),
    ]


def mock_read_csv(file_path: str):
    return mock_csv_data[file_path]


mock_csv_data = {
    "test_0_timeseries.csv": pd.DataFrame({tca.EMIS: [1, 2, 3, 4], tca.COST: [10, 9, 8, 7]}),
    "test_1_timeseries.csv": pd.DataFrame({tca.EMIS: [5, 6, 7, 8], tca.COST: [6, 5, 4, 3]}),
    "test_2_timeseries.csv": pd.DataFrame({tca.EMIS: [9, 10, 11, 12], tca.COST: [3, 2, 1, 0]}),
}

expected_summary_csv = pd.DataFrame(
    {
        tsca.PROG_NAME: ["test", "test", "test"],
        tsca.SIM: ["0", "1", "2"],
        tsca.AVG_T_DAILY_EMIS: [2.5, 6.5, 10.5],
        tsca.T_DAILY_EMIS_95: [4.0, 8.0, 12.0],
        tsca.T_DAILY_EMIS_5: [1.0, 5.0, 9.0],
        tsca.AVG_DAILY_COST: [8.5, 4.5, 1.5],
        tsca.DAILY_COST_95: [10.0, 6.0, 3.0],
        tsca.DAILY_COST_5: [7.0, 3.0, 0.0],
    }
)


def test_000_correct_summary_generated_from_3_ts(monkeypatch):
    monkeypatch.setattr(os, "scandir", mock_scandir)
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    test_ts_summary: pd.DataFrame = gen_ts_summary("test")
    assert isinstance(test_ts_summary, pd.DataFrame)
    assert test_ts_summary.equals(expected_summary_csv)
