"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        sampling_quantification_predictor.py
Purpose: Provides an emissions quantification predictor that samples
         quantification errors from a file

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

from pathlib import Path
import numpy as np
import pandas as pd
import constants.error_messages as em


class SamplingQuantificationPredictor:
    """
    A class that predicts quantified rates based on sampling from a list of
    possible quantification errors.

    Attributes:
        _quantification_errors (numpy.ndarray): Array of quantification errors.

    Methods:
        __init__(quantification_file, quantification_column): Initializes the
        SamplingQuantificationPredictor object.
        predict(true_rate): Predicts the quantification shift based on the true rate.
    """

    def __init__(self, quantification_file: str, quantification_column: str, input_dir: Path):
        """
        Initializes the SamplingQuantificationPredictor object.

        Args:
            quantification_file (str): The path to the file containing quantification errors.
            quantification_column (str): The name of the column in the file
            containing quantification errors to sample from.
        """
        self._set_quantification_errors(quantification_file, quantification_column, input_dir)

    def _set_quantification_errors(
        self, quantification_file: str, quantification_column: str, input_dir: Path
    ):
        try:
            # Directly read the required column and drop NaN values, reducing memory usage
            self._quantification_errors = (
                pd.read_csv(input_dir / quantification_file, usecols=[quantification_column])
                .dropna()[quantification_column]
                .to_numpy()
            )
        except FileNotFoundError:
            raise FileNotFoundError(
                em.Input_Processing_Messages.QUANTIFICATION_FILE_NOT_FOUND.format(
                    quantification_file=quantification_file, input_dir=input_dir
                )
            )
        except ValueError:
            raise ValueError(
                em.Input_Processing_Messages.QUANTIFICATION_INVALID_COLUMN.format(
                    quantification_column=quantification_column,
                    quantification_file=quantification_file,
                )
            )

    def predict(self, true_rate: float) -> float:
        """
        Predicts the quantified rate based on the true rate.

        Args:
            true_rate (float): The true rate for which the quantified rate is predicted.

        Returns:
            float: The predicted quantified rate.
        """
        quantification_shift: float = np.random.choice(self._quantification_errors)
        return max(true_rate * (1 + (quantification_shift / 100)), 0)
