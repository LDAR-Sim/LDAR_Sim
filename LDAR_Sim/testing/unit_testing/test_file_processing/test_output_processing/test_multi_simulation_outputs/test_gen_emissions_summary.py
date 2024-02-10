from contextlib import contextmanager
from pathlib import Path

import pandas as pd
from src.file_processing.output_processing.multi_simulation_outputs import (
    gen_emissions_summary,
    EMIS_SUMMARY_COLUMNS_ACCESSORS as esca,
)
import os
from src.file_processing.output_processing.output_utils import EMIS_DATA_COL_ACCESSORS as eca


class MockDirEntry:
    def __init__(self, name):
        self.name = name
        self.path = name

    def is_file(self) -> bool:
        return True


@contextmanager
def mock_scandir(dir: Path):
    yield [
        MockDirEntry(name="test_0_emissions_summary.csv"),
        MockDirEntry(name="test_1_emissions_summary.csv"),
        MockDirEntry(name="test_2_emissions_summary.csv"),
    ]


def mock_read_csv(file_path: str):
    return mock_csv_data[file_path]


mock_csv_data = {
    "test_0_emissions_summary.csv": pd.DataFrame(
        {eca.T_VOL_EMIT: [1, 2, 3, 4], eca.T_RATE: [10, 9, 8, 7]}
    ),
    "test_1_emissions_summary.csv": pd.DataFrame(
        {eca.T_VOL_EMIT: [5, 6, 7, 8], eca.T_RATE: [6, 5, 4, 3]}
    ),
    "test_2_emissions_summary.csv": pd.DataFrame(
        {eca.T_VOL_EMIT: [9, 10, 11, 12], eca.T_RATE: [3, 2, 1, 0]}
    ),
}

expected_summary_csv = pd.DataFrame(
    {
        esca.PROG_NAME: ["test", "test", "test"],
        esca.SIM: ["0", "1", "2"],
        esca.T_TOTAL_EMIS: [10, 26, 42],
        esca.AVG_T_EMIS_RATE: [8.5, 4.5, 1.5],
        esca.T_EMIS_RATE_95: [10.0, 6.0, 3.0],
        esca.T_EMIS_RATE_5: [7.0, 3.0, 0.0],
        esca.T_AVG_EMIS_AMOUNT: [2.5, 6.5, 10.5],
        esca.T_EMIS_AMOUNT_95: [4.0, 8.0, 12.0],
        esca.T_EMIS_AMOUNT_5: [1.0, 5.0, 9.0],
    }
)


def test_000_correct_summary_generated_from_3_es(monkeypatch):
    monkeypatch.setattr(os, "scandir", mock_scandir)
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)
    test_es_summary: pd.DataFrame = gen_emissions_summary("test")
    assert isinstance(test_es_summary, pd.DataFrame)
    assert test_es_summary.equals(expected_summary_csv)
