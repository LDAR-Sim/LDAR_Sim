"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_gen_emissions_estimate_summary.py
Purpose: Contains unit tests for testing gen_emissions_estimate_summary functions.

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
from contextlib import contextmanager
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal
from file_processing.output_processing.summary_outputs import (
    generate_emissions_estimation_summary,
)

from src.constants.output_file_constants import (
    EMIS_DATA_COL_ACCESSORS as eca,
    EMIS_SUMMARY_COLUMNS_ACCESSORS as esca,
)


from testing.unit_testing.test_file_processing.test_output_processing.test_summary_outputs.test_summarize_program_outputs import (
    get_mock_summary_output_mapper,
)


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
        MockDirEntry(name="test_0_estimated_emissions.csv"),
        MockDirEntry(name="test_1_estimated_emissions.csv"),
        MockDirEntry(name="test_2_estimated_emissions.csv"),
        MockDirEntry(name="test_0_estimated_repaired_emissions_to_remove.csv"),
        MockDirEntry(name="test_1_estimated_repaired_emissions_to_remove.csv"),
        MockDirEntry(name="test_2_estimated_repaired_emissions_to_remove.csv"),
    ]


mock_emis_csv_data = {
    "test_0_estimated_emissions.csv": pd.DataFrame(
        {
            eca.SITE_ID: [1, 1, 1, 1],
            eca.SITE_TYPE: ["A", "A", "A", "A"],
            eca.SITE_MEASURED: [True, True, True, True],
            eca.EST_VOL_EMIT: [0, 1, 2, 3],
            eca.M_RATE: [9, 8, 7, 6],
            eca.REPAIRABLE: [True, True, True, False],
            eca.START_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.END_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
    "test_1_estimated_emissions.csv": pd.DataFrame(
        {
            eca.SITE_ID: [1, 1, 1, 1],
            eca.SITE_TYPE: ["A", "A", "A", "A"],
            eca.SITE_MEASURED: [True, True, True, True],
            eca.EST_VOL_EMIT: [4, 5, 6, 7],
            eca.M_RATE: [5, 4, 3, 2],
            eca.START_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.END_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
    "test_2_estimated_emissions.csv": pd.DataFrame(
        {
            eca.SITE_ID: [1, 1, 1, 1],
            eca.SITE_TYPE: ["A", "A", "A", "A"],
            eca.SITE_MEASURED: [True, True, True, True],
            eca.EST_VOL_EMIT: [8, 9, 10, 11],
            eca.M_RATE: [2, 1, 0, 0],
            eca.START_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.END_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
}


mock_emis_to_remove_csv_data = {
    "test_0_estimated_repaired_emissions_to_remove.csv": pd.DataFrame(
        {
            eca.EST_VOL_EMIT: [0, 1, 1, 1],
            eca.M_RATE: [9, 8, 7, 6],
            eca.START_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.END_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
    "test_1_estimated_repaired_emissions_to_remove.csv": pd.DataFrame(
        {
            eca.EST_VOL_EMIT: [1, 1, 1, 1],
            eca.M_RATE: [5, 4, 3, 2],
            eca.START_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.END_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
    "test_2_estimated_repaired_emissions_to_remove.csv": pd.DataFrame(
        {
            eca.EST_VOL_EMIT: [2, 2, 2, 2],
            eca.M_RATE: [2, 1, 0, 0],
            eca.START_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
            eca.END_DATE: ["2024-01-01", "2024-01-01", "2025-01-01", "2025-01-01"],
        }
    ),
}

expected_emis_summary_csv = pd.DataFrame(
    {
        esca.PROG_NAME: ["test", "test", "test"],
        esca.SIM: ["0", "1", "2"],
        esca.EST_ANN_EMIS.format(2024): [0.0, 7.0, 13.0],
        esca.EST_ANN_EMIS.format(2025): [3.0, 11.0, 17.0],
    }
)


def test_001_generate_emissions_estimate_summary(monkeypatch, mocker):
    monkeypatch.setattr(os, "scandir", mock_scandir_emis_sum)
    # Create a mock for pd.read_csv with a side_effect
    read_csv_mock = mocker.Mock(
        side_effect=[
            mock_emis_csv_data["test_0_estimated_emissions.csv"],
            mock_emis_csv_data["test_1_estimated_emissions.csv"],
            mock_emis_csv_data["test_2_estimated_emissions.csv"],
            mock_emis_to_remove_csv_data["test_0_estimated_repaired_emissions_to_remove.csv"],
            mock_emis_to_remove_csv_data["test_1_estimated_repaired_emissions_to_remove.csv"],
            mock_emis_to_remove_csv_data["test_2_estimated_repaired_emissions_to_remove.csv"],
        ]
    )

    monkeypatch.setattr(pd, "read_csv", read_csv_mock)
    result = generate_emissions_estimation_summary("test", get_mock_summary_output_mapper())
    assert_frame_equal(expected_emis_summary_csv, result)
