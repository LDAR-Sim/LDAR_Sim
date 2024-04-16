from file_processing.output_processing.summary_output_manager import SummaryOutputManager
from constants import output_file_constants, file_name_constants
import pandas as pd
from pathlib import Path

import os
from file_processing.output_processing.summary_output_mapper import SummaryOutputMapper
from constants.output_file_constants import (
    EMIS_SUMMARY_COLUMNS_ACCESSORS as esca,
    TS_SUMMARY_COLUMNS_ACCESSORS as tsca,
)
from file_processing.output_processing import summary_output_helpers


def mock_summary_output_manager_init(self):
    self._summary_outputs_to_make = [
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY,
        file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY,
    ]
    self._output_path = Path("test")
    self._output_config = output_config = {
        output_file_constants.OutputConfigCategories.SUMMARY_OUTPUTS: {
            output_file_constants.OutputConfigCategories.SummaryOutputCatageories.SUMMARY_STATS: {
                "Timeseries Summary": {
                    'Average "True" Daily Emissions (Kg Methane)': True,
                    'Average "True" Mitigable Daily Emissions (Kg Methane)': True,
                    'Average "True" Non-Mitigable Daily Emissions (Kg Methane)': True,
                    '95th Percentile "True" Daily Emissions (Kg Methane)': True,
                    '95th Percentile "True" Mitigable Daily Emissions (Kg Methane)': True,
                    '95th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)': True,
                    '5th Percentile "True" Daily Emissions (Kg Methane)': True,
                    '5th Percentile "True" Mitigable Daily Emissions (Kg Methane)': True,
                    '5th Percentile "True" Non-Mitigable Daily Emissions (Kg Methane)': True,
                    "Average Daily Cost ($)": True,
                    "95th Percentile Daily Cost ($)": True,
                    "5th Percentile Daily Cost ($)": True,
                },
                "Emissions Summary": {
                    'Total "True" Emissions (Kg Methane)': True,
                    'Total "Estimated" Emissions (Kg Methane)': True,
                    'Total "True" Mitigable Emissions (Kg Methane)': True,
                    'Total "True" Non-Mitigable Emissions (Kg Methane)': True,
                    'Average "True" Emissions Rate (g/s)': True,
                    '95th Percentile "True" Emissions Rate (g/s)': True,
                    '5th Percentile "True" Emissions Rate (g/s)': True,
                    'Average "True" Emissions Amount (Kg Methane)': True,
                    '95th Percentile "True" Emissions Amount (Kg Methane)': True,
                    '5th Percentile "True" Emissions Amount (Kg Methane)': True,
                },
            }
        }
    }
    self._outputs_mapper = SummaryOutputMapper(
        output_config[output_file_constants.OutputConfigCategories.SUMMARY_OUTPUTS][
            output_file_constants.OutputConfigCategories.SummaryOutputCatageories.SUMMARY_STATS
        ],
        [2024, 2025],
    )
    return


class MockDirEntry:
    def __init__(self, name):
        self.name = name
        self.path = name

    def is_dir(self):
        return True

    def is_file(self) -> bool:
        return True


mock_legacy_outputs: dict[str, pd.DataFrame] = {
    file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY: pd.DataFrame(
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
    ),
    file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY: pd.DataFrame(
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
    ),
}

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

expected_results_for_concat = {
    file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY: pd.DataFrame(
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
    file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY: pd.DataFrame(
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
    file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY: pd.DataFrame(
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
    file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY: pd.DataFrame(
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


def mock_gen_ts_summary(dir: Path, outputs_mapper: SummaryOutputMapper):
    return mock_current_ts_summary_csv


def mock_gen_emis_summary(dir: Path, outputs_mapper: SummaryOutputMapper):
    return mock_current_emis_summary_csv


def mock_scandir(dir: Path):
    yield MockDirEntry(name="test")


def mock_get_legacy_outputs(self):
    return mock_legacy_outputs


def mock_get_legacy_outputs_no_files(self):
    return {
        file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY: pd.DataFrame(),
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY: pd.DataFrame(),
    }


class results_holder:
    def __init__(self):
        self.results = {
            file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY: None,
            file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY: None,
        }


def test_000_correct_outputs_when_previous_outputs_exist_and_clear_outputs(monkeypatch):
    monkeypatch.setattr(os, "scandir", mock_scandir)

    monkeypatch.setattr(SummaryOutputManager, "get_legacy_outputs", mock_get_legacy_outputs)

    clear_dir_called: bool = False

    def mock_clear_directory(dir: Path):
        nonlocal clear_dir_called
        clear_dir_called = True

    monkeypatch.setattr(
        summary_output_helpers,
        "clear_directory",
        mock_clear_directory,
    )

    results = results_holder()

    def mock_save_summary_file(dataframe: pd.DataFrame, path: Path, filename: str):
        nonlocal results
        results.results[filename] = dataframe

    monkeypatch.setattr(
        summary_output_helpers,
        "save_summary_file",
        mock_save_summary_file,
    )

    monkeypatch.setattr(SummaryOutputManager, "__init__", mock_summary_output_manager_init)
    output_manager: SummaryOutputManager = SummaryOutputManager()
    output_manager.OUTPUT_FUNCTIONS_MAP[
        file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY
    ] = mock_gen_ts_summary
    output_manager.OUTPUT_FUNCTIONS_MAP[
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    ] = mock_gen_emis_summary
    output_manager.gen_summary_outputs(True)
    assert clear_dir_called
    for file, result in results.results.items():
        assert result.equals(expected_results_for_concat[file])


def test_000_correct_outputs_no_prev_outputs_and_clear_outputs(monkeypatch):
    monkeypatch.setattr(os, "scandir", mock_scandir)

    monkeypatch.setattr(
        SummaryOutputManager, "get_legacy_outputs", mock_get_legacy_outputs_no_files
    )

    clear_dir_called: bool = False

    def mock_clear_directory(dir: Path):
        nonlocal clear_dir_called
        clear_dir_called = True

    monkeypatch.setattr(
        summary_output_helpers,
        "clear_directory",
        mock_clear_directory,
    )

    results = results_holder()

    def mock_save_summary_file(dataframe: pd.DataFrame, path: Path, filename: str):
        nonlocal results
        results.results[filename] = dataframe

    monkeypatch.setattr(
        summary_output_helpers,
        "save_summary_file",
        mock_save_summary_file,
    )

    monkeypatch.setattr(SummaryOutputManager, "__init__", mock_summary_output_manager_init)
    output_manager: SummaryOutputManager = SummaryOutputManager()
    output_manager.OUTPUT_FUNCTIONS_MAP[
        file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY
    ] = mock_gen_ts_summary
    output_manager.OUTPUT_FUNCTIONS_MAP[
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY
    ] = mock_gen_emis_summary
    output_manager.gen_summary_outputs(True)
    assert clear_dir_called
    for file, result in results.results.items():
        assert result.equals(expected_results_no_concat[file])
