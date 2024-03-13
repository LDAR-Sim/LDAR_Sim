"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_concat_output_data
Purpose: Testing the concat output data method.

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

import os
from pathlib import Path

import pandas as pd
from LDAR_Sim.src.file_processing.output_processing.output_constants import (
    EMIS_SUMMARY_FILENAME,
    TS_SUMMARY_FILENAME,
)

from src.file_processing.output_processing.multi_simulation_outputs import (  # noqa
    gen_ts_summary,
    TS_SUMMARY_COLUMNS_ACCESSORS as tsca,
    gen_emissions_summary,
    EMIS_SUMMARY_COLUMNS_ACCESSORS as esca,
    get_summary_file,
    clear_directory,
    mark_outputs_to_keep,
    concat_output_data,
    save_summary_file,
)


class MockDirEntry:
    def __init__(self, name):
        self.name = name
        self.path = name

    def is_dir(self) -> bool:
        return True


mock_legacy_ts_summary_csv = pd.DataFrame(
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

mock_legacy_emis_summary_csv = pd.DataFrame(
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

mock_current_ts_summary_csv = pd.DataFrame(
    {
        tsca.PROG_NAME: ["test", "test", "test"],
        tsca.SIM: ["3", "4", "5"],
        tsca.AVG_T_DAILY_EMIS: [2.5, 6.5, 10.5],
        tsca.T_DAILY_EMIS_95: [4.0, 8.0, 12.0],
        tsca.T_DAILY_EMIS_5: [1.0, 5.0, 9.0],
        tsca.AVG_DAILY_COST: [8.5, 4.5, 1.5],
        tsca.DAILY_COST_95: [10.0, 6.0, 3.0],
        tsca.DAILY_COST_5: [7.0, 3.0, 0.0],
    }
)

mock_current_emis_summary_csv = pd.DataFrame(
    {
        esca.PROG_NAME: ["test", "test", "test"],
        esca.SIM: ["3", "4", "5"],
        esca.T_TOTAL_EMIS: [10, 26, 42],
        esca.AVG_T_EMIS_RATE: [8.5, 4.5, 1.5],
        esca.T_EMIS_RATE_95: [10.0, 6.0, 3.0],
        esca.T_EMIS_RATE_5: [7.0, 3.0, 0.0],
        esca.T_AVG_EMIS_AMOUNT: [2.5, 6.5, 10.5],
        esca.T_EMIS_AMOUNT_95: [4.0, 8.0, 12.0],
        esca.T_EMIS_AMOUNT_5: [1.0, 5.0, 9.0],
    }
)


class results_holder:
    def __init__(self):
        self.results = {TS_SUMMARY_FILENAME: None, EMIS_SUMMARY_FILENAME: None}


expected_results_for_concat = {
    TS_SUMMARY_FILENAME: pd.DataFrame(
        {
            tsca.PROG_NAME: ["test", "test", "test", "test", "test", "test"],
            tsca.SIM: ["0", "1", "2", "3", "4", "5"],
            tsca.AVG_T_DAILY_EMIS: [2.5, 6.5, 10.5, 2.5, 6.5, 10.5],
            tsca.T_DAILY_EMIS_95: [4.0, 8.0, 12.0, 4.0, 8.0, 12.0],
            tsca.T_DAILY_EMIS_5: [1.0, 5.0, 9.0, 1.0, 5.0, 9.0],
            tsca.AVG_DAILY_COST: [8.5, 4.5, 1.5, 8.5, 4.5, 1.5],
            tsca.DAILY_COST_95: [10.0, 6.0, 3.0, 10.0, 6.0, 3.0],
            tsca.DAILY_COST_5: [7.0, 3.0, 0.0, 7.0, 3.0, 0.0],
        }
    ),
    EMIS_SUMMARY_FILENAME: pd.DataFrame(
        {
            esca.PROG_NAME: ["test", "test", "test", "test", "test", "test"],
            esca.SIM: ["0", "1", "2", "3", "4", "5"],
            esca.T_TOTAL_EMIS: [10, 26, 42, 10, 26, 42],
            esca.AVG_T_EMIS_RATE: [8.5, 4.5, 1.5, 8.5, 4.5, 1.5],
            esca.T_EMIS_RATE_95: [10.0, 6.0, 3.0, 10.0, 6.0, 3.0],
            esca.T_EMIS_RATE_5: [7.0, 3.0, 0.0, 7.0, 3.0, 0.0],
            esca.T_AVG_EMIS_AMOUNT: [2.5, 6.5, 10.5, 2.5, 6.5, 10.5],
            esca.T_EMIS_AMOUNT_95: [4.0, 8.0, 12.0, 4.0, 8.0, 12.0],
            esca.T_EMIS_AMOUNT_5: [1.0, 5.0, 9.0, 1.0, 5.0, 9.0],
        }
    ),
}

expected_results_no_concat = {
    TS_SUMMARY_FILENAME: pd.DataFrame(
        {
            tsca.PROG_NAME: ["test", "test", "test"],
            tsca.SIM: ["3", "4", "5"],
            tsca.AVG_T_DAILY_EMIS: [2.5, 6.5, 10.5],
            tsca.T_DAILY_EMIS_95: [4.0, 8.0, 12.0],
            tsca.T_DAILY_EMIS_5: [1.0, 5.0, 9.0],
            tsca.AVG_DAILY_COST: [8.5, 4.5, 1.5],
            tsca.DAILY_COST_95: [10.0, 6.0, 3.0],
            tsca.DAILY_COST_5: [7.0, 3.0, 0.0],
        }
    ),
    EMIS_SUMMARY_FILENAME: pd.DataFrame(
        {
            esca.PROG_NAME: ["test", "test", "test"],
            esca.SIM: ["3", "4", "5"],
            esca.T_TOTAL_EMIS: [10, 26, 42],
            esca.AVG_T_EMIS_RATE: [8.5, 4.5, 1.5],
            esca.T_EMIS_RATE_95: [10.0, 6.0, 3.0],
            esca.T_EMIS_RATE_5: [7.0, 3.0, 0.0],
            esca.T_AVG_EMIS_AMOUNT: [2.5, 6.5, 10.5],
            esca.T_EMIS_AMOUNT_95: [4.0, 8.0, 12.0],
            esca.T_EMIS_AMOUNT_5: [1.0, 5.0, 9.0],
        }
    ),
}


def mock_scandir(dir: Path):
    yield MockDirEntry(name="test")


def mock_gen_ts_summary(dir: Path):
    return mock_current_ts_summary_csv


def mock_gen_emis_summary(dir: Path):
    return mock_current_emis_summary_csv


def mock_get_summary_file_prev_files(dir: Path, filename: str):
    if filename == TS_SUMMARY_FILENAME:
        return mock_legacy_ts_summary_csv
    else:
        return mock_legacy_emis_summary_csv


def mock_get_summary_file_no_prev_files(dir: Path, filename: str):
    return pd.DataFrame()


def test_000_concat_output_data_concats_if_prev_data_exists(monkeypatch):
    monkeypatch.setattr(os, "scandir", mock_scandir)
    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.gen_ts_summary",
        mock_gen_ts_summary,
    )
    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.gen_emissions_summary",
        mock_gen_emis_summary,
    )
    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.get_summary_file",
        mock_get_summary_file_prev_files,
    )
    clear_dir_called: bool = False

    def mock_clear_directory(dir: Path):
        nonlocal clear_dir_called
        clear_dir_called = True

    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.clear_directory",
        mock_clear_directory,
    )

    results = results_holder()

    def mock_save_summary_file(dataframe: pd.DataFrame, path: Path, filename: str):
        nonlocal results
        results.results[filename] = dataframe

    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.save_summary_file",
        mock_save_summary_file,
    )

    concat_output_data("test", True)

    assert clear_dir_called
    for file, result in results.results.items():
        assert result.equals(expected_results_for_concat[file])


def test_000_concat_output_data_uses_current_if_no_prev_data(monkeypatch):
    monkeypatch.setattr(os, "scandir", mock_scandir)
    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.gen_ts_summary",
        mock_gen_ts_summary,
    )
    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.gen_emissions_summary",
        mock_gen_emis_summary,
    )
    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.get_summary_file",
        mock_get_summary_file_no_prev_files,
    )
    mark_outputs_to_keep_called: bool = False

    def mock_mark_outputs_to_keep(dir: Path):
        nonlocal mark_outputs_to_keep_called
        mark_outputs_to_keep_called = True

    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.mark_outputs_to_keep",
        mock_mark_outputs_to_keep,
    )

    results = results_holder()

    def mock_save_summary_file(dataframe: pd.DataFrame, path: Path, filename: str):
        nonlocal results
        results.results[filename] = dataframe

    monkeypatch.setattr(
        "src.file_processing.output_processing.multi_simulation_outputs.save_summary_file",
        mock_save_summary_file,
    )

    concat_output_data("test", False)

    assert mark_outputs_to_keep_called
    for file, result in results.results.items():
        assert result.equals(expected_results_no_concat[file])
