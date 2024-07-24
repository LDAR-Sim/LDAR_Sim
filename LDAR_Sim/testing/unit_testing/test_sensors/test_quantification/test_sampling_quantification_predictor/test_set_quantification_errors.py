"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_set_quantification_errors.py
Purpose: To provide tests for _set_quantification_errors method in the SamplingQuantificationPredictor class

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

import pytest
from unittest.mock import patch
from pathlib import Path
import numpy as np
import pandas as pd
from sensors.quantification.sampling_quantification_predictor import SamplingQuantificationPredictor
import constants.error_messages as em


@pytest.fixture
def mock_df():
    return pd.DataFrame({"valid_column": [1, 2, 3, np.nan]})


def mock_SamplingQuantificationPredictor_init(self, quantification_file, quantification_column):
    return None


@pytest.fixture
def predictor_instance(monkeypatch):
    monkeypatch.setattr(
        SamplingQuantificationPredictor,
        "__init__",
        mock_SamplingQuantificationPredictor_init,
    )
    return SamplingQuantificationPredictor("test_file", "test_column")


@patch("pandas.read_csv")
def test_set_quantification_errors_handles_nan_values_correctly(
    mock_read_csv, mock_df, predictor_instance
):
    mock_read_csv.return_value = mock_df
    predictor_instance._set_quantification_errors("test_file", "valid_column", Path("test_dir"))

    # Assuming the method filters out NaN values, expect 3 non-NaN entries
    assert len(predictor_instance._quantification_errors) == 3


def test_set_quantification_errors_file_not_found(predictor_instance, tmp_path):
    """
    Test that FileNotFoundError is raised when the quantification file does not exist.
    """
    with pytest.raises(FileNotFoundError) as excinfo:
        predictor_instance._set_quantification_errors(
            quantification_file="nonexistent.csv",
            quantification_column="any_column",
            input_dir=tmp_path,
        )
    assert em.Input_Processing_Messages.QUANTIFICATION_FILE_NOT_FOUND.format(
        quantification_file="nonexistent.csv", input_dir=tmp_path
    ) in str(excinfo.value)


def test_set_quantification_errors_invalid_column(predictor_instance, tmp_path):
    """
    Test that ValueError is raised when the specified
        quantification column does not exist in the file.
    """
    # Setup a valid quantification file with an unexpected column
    quantification_file = tmp_path / "quantification.csv"
    df = pd.DataFrame({"unexpected_column": [1, 2, 3]})
    df.to_csv(quantification_file, index=False)

    with pytest.raises(ValueError) as excinfo:
        predictor_instance._set_quantification_errors(
            quantification_file=str(quantification_file),
            quantification_column="nonexistent_column",
            input_dir=tmp_path,
        )
    assert em.Input_Processing_Messages.QUANTIFICATION_INVALID_COLUMN.format(
        quantification_file=str(quantification_file),
        quantification_column="nonexistent_column",
    ) in str(excinfo.value)
