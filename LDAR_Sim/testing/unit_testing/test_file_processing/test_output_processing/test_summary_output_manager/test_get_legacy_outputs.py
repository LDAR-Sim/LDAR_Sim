from pathlib import Path

import pandas as pd
from constants import file_name_constants
from file_processing.output_processing.summary_output_manager import SummaryOutputManager


def mock_summary_output_manager_init(self):
    self._summary_outputs_to_make = [
        file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY,
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY,
    ]
    self._output_path = Path("test")


def mock_get_summary_file_files_exist(file_path: str, summary_output: str):
    if summary_output == file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY:
        return "ts_summary"
    elif summary_output == file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY:
        return "emis_summary"


def test_get_legacy_outputs_returns_all_files_when_exist(monkeypatch):
    monkeypatch.setattr(
        "file_processing.output_processing.summary_output_manager.SummaryOutputManager.__init__",
        mock_summary_output_manager_init,
    )
    monkeypatch.setattr(
        ("file_processing.output_processing.summary_output_helpers.get_summary_file"),
        mock_get_summary_file_files_exist,
    )
    expected_leg_outputs = {
        file_name_constants.Output_Files.SummaryFileNames.TS_SUMMARY: "ts_summary",
        file_name_constants.Output_Files.SummaryFileNames.EMIS_SUMMARY: "emis_summary",
    }
    summary_output_manager: SummaryOutputManager = SummaryOutputManager()
    leg_outputs = summary_output_manager.get_legacy_outputs()
    assert leg_outputs == expected_leg_outputs


def test_get_legacy_outputs_return_empty_dataframes_when_no_files_exist(monkeypatch):
    monkeypatch.setattr(
        "file_processing.output_processing.summary_output_manager.SummaryOutputManager.__init__",
        mock_summary_output_manager_init,
    )
    monkeypatch.setattr(
        ("file_processing.output_processing.summary_output_helpers.get_summary_file"),
        lambda x, y: pd.DataFrame(),
    )
    summary_output_manager: SummaryOutputManager = SummaryOutputManager()
    leg_outputs = summary_output_manager.get_legacy_outputs()
    for key in leg_outputs.keys():
        assert leg_outputs[key].empty
